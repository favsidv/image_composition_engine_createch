"""Verify the unchanged filters received from Paul LAMOUR and Ryan Fihr HULTON."""

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np

from image_composition_engine_createch.application import compose_from_file
from image_composition_engine_createch.config import load_config
from image_composition_engine_createch import external_filters
from image_composition_engine_createch.external_filters.hue import Hue
from image_composition_engine_createch.external_filters.pixelate import Pixelate
from image_composition_engine_createch.image_io import load_image
from image_composition_engine_createch.pipeline import apply_filters
from image_composition_engine_createch.registry import create_filter


PROJECT = Path(__file__).resolve().parents[1]
CONFIGURATIONS = PROJECT / "configurations/filter_exchange"
RECEIVED_HASHES = {
    "pixelate": "7ca353a5f09108e0cfa22db0032693570d63b46975ad9063f4a0d6bb899f6280",
    "glitch": "5f607318a2bfb99a25d4f6d4e6fc922cce088f0da09cafd87144c271287303bc",
    "hue": "f98301de09198a9c0ac7c0e7e72fe2eda1a92d258d6f1d6035da2c793666385a",
    "bubble_pop": "2c48e3bcaf07bb188d0e2c7634fea5a2d318f09f62affb9c5ce24d93578ea5dc",
}


class FilterExchangeTests(unittest.TestCase):
    def test_received_sources_are_byte_for_byte_unchanged(self):
        directory = Path(external_filters.__file__).parent
        for name, expected in RECEIVED_HASHES.items():
            with self.subTest(filter=name):
                actual = hashlib.sha256((directory / f"{name}.py").read_bytes()).hexdigest()
                self.assertEqual(actual, expected)

    def test_registered_filters_preserve_image_contract(self):
        photo = load_image(PROJECT / "images/layers/0_photo.jpg")[:29, :37]
        for name in RECEIVED_HASHES:
            config = load_config(CONFIGURATIONS / f"{name}.json")
            settings = config["layers"][0]["filters"][0]
            for dtype in (np.float32, np.float64):
                with self.subTest(filter=name, dtype=dtype):
                    image = photo.astype(dtype)
                    image[..., 3] = np.linspace(0, 1, image.shape[1], dtype=dtype)
                    before = image.copy()
                    rgb = image[..., :3].copy()
                    operation = create_filter(name, settings["params"])
                    filtered = operation.apply(rgb)
                    self.assertEqual(filtered.shape, rgb.shape)
                    self.assertEqual(filtered.dtype, dtype)
                    self.assertFalse(np.shares_memory(filtered, rgb))
                    np.testing.assert_array_equal(rgb, before[..., :3])
                    self.assertTrue(np.isfinite(filtered).all())
                    self.assertTrue(((filtered >= 0) & (filtered <= 1)).all())
                    result = apply_filters(image, [settings])
                    self.assertEqual(result.shape, image.shape)
                    self.assertEqual(result.dtype, dtype)
                    self.assertFalse(np.shares_memory(result, image))
                    np.testing.assert_array_equal(result[..., 3], before[..., 3])
                    np.testing.assert_array_equal(image, before)

    def test_pixelate_edges_and_hue_rotation(self):
        image = np.arange(5 * 7 * 3, dtype=np.float64).reshape(5, 7, 3) / 104
        result = Pixelate(size=3).apply(image)
        expected = np.broadcast_to(image[3:, 6:].mean(axis=(0, 1)), (2, 1, 3))
        np.testing.assert_allclose(result[3:, 6:], expected)
        red = np.array([[[1, 0, 0]]], dtype=np.float32)
        np.testing.assert_allclose(Hue(angle=120).apply(red), [[[0, 1, 0]]], atol=1e-6)

    def test_random_effects_with_controlled_test_rng(self):
        image = np.random.default_rng(1).random((29, 37, 3)).astype(np.float32)
        for name in ("glitch", "bubble_pop"):
            settings = load_config(CONFIGURATIONS / f"{name}.json")["layers"][0]["filters"][0]
            results = []
            for _ in range(2):
                rng = np.random.Generator(np.random.PCG64(12))
                with patch("numpy.random.default_rng", return_value=rng):
                    results.append(create_filter(name, settings["params"]).apply(image))
            np.testing.assert_array_equal(results[0], results[1])
            self.assertFalse(np.array_equal(results[0], image))
        np.testing.assert_array_equal(create_filter("glitch", {"intensity": 0}).apply(image), image)
        np.testing.assert_array_equal(
            create_filter("bubble_pop", {"amount": 2, "opacity": 0}).apply(image), image
        )

    def test_received_filter_runs_through_existing_application(self):
        with TemporaryDirectory() as directory:
            output = compose_from_file(
                CONFIGURATIONS / "pixelate.json", Path(directory) / "pixelate.png"
            )
            result = load_image(output)
        self.assertEqual(result.shape, (1272, 1908, 4))
        self.assertEqual(result.dtype, np.float32)
        self.assertTrue(np.isfinite(result).all())
        np.testing.assert_array_equal(result[..., 3], 1)


if __name__ == "__main__":
    unittest.main()
