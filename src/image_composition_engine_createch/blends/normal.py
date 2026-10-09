"""Normal RGB blending and modes that operate on RGBA transparency."""

import numpy as np

from ..contracts import AlphaBlendMode, BlendMode
from ._utils import check_opacity, prepare_images


def _source_over(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    """Composite validated straight-alpha arrays using the layer's alpha."""
    base_alpha = base[..., 3:4]
    layer_alpha = layer[..., 3:4]
    alpha = layer_alpha + base_alpha * (1 - layer_alpha)
    color = layer[..., :3] * layer_alpha + base[..., :3] * base_alpha * (1 - layer_alpha)
    rgb = np.divide(color, alpha, out=np.zeros_like(color), where=alpha > 0)
    return np.clip(np.concatenate((rgb, alpha), axis=-1), 0, 1)


class Normal(BlendMode):
    """Use the layer RGB values; the compositor handles transparency."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return an independent copy of the layer colors."""
        base, layer = prepare_images(base, layer)
        return layer.copy()


class Dissolve(AlphaBlendMode):
    """Randomly cover whole pixels with probability layer alpha times opacity.

    An optional seed makes direct use reproducible. Configuration-created
    instances use fresh randomness; RGB channels share the same pixel mask.
    """

    def __init__(self, seed: int | None = None) -> None:
        self.random = np.random.default_rng(seed)

    def compose(self, base: np.ndarray, layer: np.ndarray, opacity: float) -> np.ndarray:
        """Convert effective layer alpha to a binary mask, then composite."""
        base, layer = prepare_images(base, layer, channels=4)
        check_opacity(opacity)
        prepared = layer.copy()
        prepared[..., 3] = self.random.random(layer.shape[:2]) < layer[..., 3] * opacity
        return _source_over(base, prepared)


class Behind(AlphaBlendMode):
    """Paint beneath the base using destination-over composition.

    This engine interprets the layer alpha as paint coverage. Opaque base
    pixels are unchanged; transparent regions reveal the incoming layer.
    """

    def compose(self, base: np.ndarray, layer: np.ndarray, opacity: float) -> np.ndarray:
        """Place the incoming layer behind the existing RGBA image."""
        base, layer = prepare_images(base, layer, channels=4)
        check_opacity(opacity)
        prepared = layer.copy()
        prepared[..., 3] *= opacity
        return _source_over(prepared, base)


class Clear(AlphaBlendMode):
    """Erase base transparency using layer alpha times opacity as coverage.

    This is the engine's layer-mask interpretation of Adobe's painting mode.
    Layer RGB values do not affect erasing.
    """

    def compose(self, base: np.ndarray, layer: np.ndarray, opacity: float) -> np.ndarray:
        """Reduce base alpha and zero RGB only where the result is transparent."""
        base, layer = prepare_images(base, layer, channels=4)
        check_opacity(opacity)
        result = base.copy()
        result[..., 3] *= 1 - layer[..., 3] * opacity
        result[..., :3] = np.where(result[..., 3:4] > 0, base[..., :3], 0)
        return result
