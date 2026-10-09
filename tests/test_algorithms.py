"""Regression checks for RGB formulas, spatial filters and alpha modes."""

import unittest

import numpy as np

from image_composition_engine_createch.blends.hsl import luminosity
from image_composition_engine_createch.blends.normal import Dissolve
from image_composition_engine_createch.compositing import compose_layer
from image_composition_engine_createch.contracts import AlphaBlendMode, BlendMode, Filter
from image_composition_engine_createch.filters import Blur, Brightness, Contrast, GaussianBlur, Invert
from image_composition_engine_createch.pipeline import apply_filters
from image_composition_engine_createch.registry import BLENDS, create_blend, create_filter


class BlendTests(unittest.TestCase):
    def test_known_rgb_results(self):
        base = np.array([[[0.2, 0.6, 0.9]]])
        layer = np.array([[[0.3, 0.7, 0.1]]])
        expected = {
            'normal': [.3, .7, .1],
            'darken': [.2, .6, .1],
            'multiply': [.06, .42, .09],
            'color_burn': [0, 3 / 7, 0],
            'linear_burn': [0, .3, 0],
            'darker_color': [.3, .7, .1],
            'lighten': [.3, .7, .9],
            'screen': [.44, .88, .91],
            'color_dodge': [2 / 7, 1, 1],
            'linear_dodge': [.5, 1, 1],
            'lighter_color': [.2, .6, .9],
            'overlay': [.12, .76, .82],
            'soft_light': [.136, .6 + .4 * (np.sqrt(.6) - .6), .828],
            'hard_light': [.12, .76, .18],
            'vivid_light': [0, 1, .5],
            'linear_light': [0, 1, .1],
            'pin_light': [.2, .6, .2],
            'hard_mix': [0, 1, 1],
            'difference': [.1, .1, .8],
            'exclusion': [.38, .46, .82],
            'subtract': [0, 0, .8],
            'divide': [2 / 3, 6 / 7, 1],
            'hue': [79 / 300, .73, .03],
            'saturation': [1713 / 7000, 4113 / 7000, 5913 / 7000],
            'color': [.299, .699, .099],
            'luminosity': [.201, .601, .901],
        }
        for name, rgb in expected.items():
            with self.subTest(mode=name):
                np.testing.assert_allclose(create_blend(name).apply(base, layer), [[rgb]], atol=1e-12)

    def test_all_modes_shape_dtype_range_and_ownership(self):
        self.assertEqual(len(BLENDS), 29)
        for dtype in (np.float32, np.float64):
            base = np.random.default_rng(1).random((4, 5, 4)).astype(dtype)
            layer = np.random.default_rng(2).random((4, 5, 4)).astype(dtype)
            base[0, 0] = 0
            layer[0, 0] = 1
            before_base, before_layer = base.copy(), layer.copy()
            for name in BLENDS:
                with self.subTest(mode=name, dtype=dtype), np.errstate(divide='raise', invalid='raise', over='raise'):
                    result = compose_layer(base, layer, name, opacity=.4)
                    self.assertEqual(result.dtype, dtype)
                    self.assertEqual(result.shape, base.shape)
                    self.assertTrue(np.isfinite(result).all())
                    self.assertTrue(((result >= 0) & (result <= 1)).all())
                    self.assertFalse(np.shares_memory(result, base))
                    self.assertFalse(np.shares_memory(result, layer))
                    np.testing.assert_array_equal(base, before_base)
                    np.testing.assert_array_equal(layer, before_layer)
                    mode = create_blend(name)
                    if isinstance(mode, BlendMode):
                        rgb = mode.apply(base[..., :3], layer[..., :3])
                        self.assertEqual(rgb.dtype, dtype)
                        self.assertFalse(np.shares_memory(rgb, base))
                        self.assertFalse(np.shares_memory(rgb, layer))
                    else:
                        self.assertIsInstance(mode, AlphaBlendMode)

    def test_division_endpoints_and_small_divisors(self):
        for dtype in (np.float32, np.float64):
            tiny = np.nextafter(dtype(0), dtype(1))
            base = np.array([[[0, 1, .5], [0, 1, .5]]], dtype=dtype)
            layer = np.array([[[0, 0, tiny], [1, 1, 1]]], dtype=dtype)
            expected = {
                'color_burn': [[[0, 1, 0], [0, 1, .5]]],
                'color_dodge': [[[0, 1, .5], [0, 1, 1]]],
                'divide': [[[1, 1, 1], [0, 1, .5]]],
            }
            for name, pixels in expected.items():
                with self.subTest(mode=name, dtype=dtype), np.errstate(divide='raise', invalid='raise', over='raise'):
                    np.testing.assert_allclose(create_blend(name).apply(base, layer), pixels)

    def test_whole_color_selection_is_per_pixel(self):
        base = np.array([[[.9, 0, 0], [0, .2, 0], [.3, .3, .3]]])
        layer = np.array([[[0, .2, 0], [.9, 0, 0], [.3, .3, .3]]])
        np.testing.assert_array_equal(create_blend('darker_color').apply(base, layer), [[[0, .2, 0], [0, .2, 0], [.3, .3, .3]]])
        np.testing.assert_array_equal(create_blend('lighter_color').apply(base, layer), [[[.9, 0, 0], [.9, 0, 0], [.3, .3, .3]]])

    def test_hsl_luminosity_and_gray_pixels(self):
        base = np.random.default_rng(3).random((10, 12, 3))
        layer = np.random.default_rng(4).random((10, 12, 3))
        base[0] = .5
        layer[1] = 0
        layer[2] = 1
        for name in ('hue', 'saturation', 'color', 'luminosity'):
            with self.subTest(mode=name):
                result = create_blend(name).apply(base, layer)
                target = layer if name == 'luminosity' else base
                np.testing.assert_allclose(luminosity(result), luminosity(target), atol=1e-12)
        np.testing.assert_allclose(create_blend('saturation').apply(base, layer)[0], .5)

    def test_soft_light_dark_polynomial_and_midgray(self):
        base = np.array([[[.04, .25, .81]]])
        np.testing.assert_allclose(create_blend('soft_light').apply(base, np.ones_like(base)), [[[.141824, .5, .9]]])
        for name in ('soft_light', 'hard_light', 'vivid_light', 'linear_light', 'pin_light'):
            np.testing.assert_allclose(create_blend(name).apply(base, np.full_like(base, .5)), base)

    def test_behind_and_clear_partial_alpha(self):
        base = np.array([[[1, 0, 0, .5]]])
        layer = np.array([[[0, 0, 1, .5]]])
        np.testing.assert_allclose(compose_layer(base, layer, 'behind'), [[[2 / 3, 0, 1 / 3, .75]]])
        np.testing.assert_allclose(compose_layer(base, layer, 'clear', .4), [[[1, 0, 0, .4]]])
        layer[..., 3] = 1
        np.testing.assert_array_equal(compose_layer(base, layer, 'clear'), np.zeros_like(base))
        base[..., 3] = 1
        np.testing.assert_array_equal(compose_layer(base, layer, 'behind'), base)

    def test_dissolve_pixel_mask_probability_and_seed(self):
        base = np.zeros((64, 64, 4))
        layer = np.empty_like(base)
        layer[:] = [1, .25, .75, .8]
        first = Dissolve(seed=42).compose(base, layer, .5)
        second = Dissolve(seed=42).compose(base, layer, .5)
        np.testing.assert_array_equal(first, second)
        mask = first[..., 3].astype(bool)
        self.assertLess(abs(mask.mean() - .4), .03)
        self.assertTrue(np.isin(first[..., 3], [0, 1]).all())
        np.testing.assert_allclose(first[mask, :3], np.broadcast_to([1, .25, .75], first[mask, :3].shape))
        np.testing.assert_array_equal(first[~mask], 0)
        np.testing.assert_array_equal(Dissolve().compose(base, layer, 0), base)
        layer[..., 3] = 1
        np.testing.assert_array_equal(Dissolve().compose(base, layer, 1), layer)

    def test_input_validation_and_mixed_dtypes(self):
        rgb = np.ones((1, 1, 3), dtype=np.float32)
        for name in BLENDS:
            mode = create_blend(name)
            if isinstance(mode, BlendMode):
                with self.subTest(mode=name):
                    self.assertEqual(mode.apply(rgb, rgb.astype(np.float64)).dtype, np.float64)
                    with self.assertRaises(ValueError):
                        mode.apply(rgb, np.ones((2, 1, 3)))
                    with self.assertRaises(ValueError):
                        mode.apply(rgb, rgb * 2)
                    with self.assertRaises(TypeError):
                        mode.apply(rgb, rgb.astype(np.uint8))


class FilterTests(unittest.TestCase):
    def test_filters_preserve_contract_and_pipeline_alpha(self):
        for dtype in (np.float32, np.float64):
            image = np.random.default_rng(5).random((4, 5, 3)).astype(dtype)
            before = image.copy()
            for operation in (Brightness(.2), Contrast(1.4), Invert(), Blur(1), GaussianBlur(2, 1.3)):
                with self.subTest(filter=type(operation).__name__, dtype=dtype):
                    self.assertIsInstance(operation, Filter)
                    result = operation.apply(image)
                    self.assertEqual(result.dtype, dtype)
                    self.assertEqual(result.shape, image.shape)
                    self.assertFalse(np.shares_memory(result, image))
                    self.assertTrue(((result >= 0) & (result <= 1)).all())
                    np.testing.assert_array_equal(image, before)
            rgba = np.concatenate((image, np.full((4, 5, 1), .3, dtype=dtype)), axis=2)
            result = apply_filters(rgba, [{'name': 'invert'}, {'name': 'brightness', 'params': {'level': .1}}])
            np.testing.assert_array_equal(result[..., 3], rgba[..., 3])

    def test_blurs_match_cropped_neighborhood_reference(self):
        image = np.random.default_rng(7).random((4, 5, 3))
        for radius in (0, 1, 6):
            for sigma in (None, .7, 2.):
                expected = np.empty_like(image)
                for y in range(image.shape[0]):
                    for x in range(image.shape[1]):
                        ys = np.arange(max(0, y - radius), min(image.shape[0], y + radius + 1))
                        xs = np.arange(max(0, x - radius), min(image.shape[1], x + radius + 1))
                        weights = np.ones((len(ys), len(xs)))
                        if sigma is not None:
                            weights = np.exp(-((ys[:, None] - y) ** 2 + (xs[None, :] - x) ** 2) / (2 * sigma ** 2))
                        patch = image[ys[:, None], xs[None, :]]
                        expected[y, x] = (patch * weights[..., None]).sum(axis=(0, 1)) / weights.sum()
                operation = Blur(radius) if sigma is None else GaussianBlur(radius, sigma)
                with self.subTest(radius=radius, sigma=sigma):
                    np.testing.assert_allclose(operation.apply(image), expected, atol=1e-12)

    def test_parameter_validation_without_registry(self):
        for invalid in (True, float('nan'), float('inf'), '1'):
            with self.assertRaises(ValueError):
                Brightness(invalid)
            with self.assertRaises(ValueError):
                Contrast(invalid)
        for invalid in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                Blur(invalid)
            with self.assertRaises(ValueError):
                GaussianBlur(invalid, 1)
        for invalid in (0, -1, float('nan'), True):
            with self.assertRaises(ValueError):
                GaussianBlur(1, invalid)
        with self.assertRaises(ValueError):
            Contrast(-1)
        self.assertEqual(create_filter('gaussianblur', {'window': 2, 'sigma': 1}).radius, 2)

    def test_large_levels_saturate_without_overflow(self):
        for dtype in (np.float32, np.float64):
            image = np.array([[[.2, .5, .8]]], dtype=dtype)
            with np.errstate(over='raise', invalid='raise'):
                np.testing.assert_array_equal(Brightness(1e300).apply(image), np.ones_like(image))
                np.testing.assert_array_equal(Brightness(-1e300).apply(image), np.zeros_like(image))
                np.testing.assert_array_equal(Contrast(1e300).apply(image), [[[0, .5, 1]]])


if __name__ == '__main__':
    unittest.main()
