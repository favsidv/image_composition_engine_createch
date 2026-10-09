"""Lighten blend modes for normalized RGB image arrays."""

import numpy as np

from ..contracts import BlendMode
from ._utils import prepare_images, color_dodge


class Lighten(BlendMode):
    """Keep the higher value of each RGB channel."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.maximum(base, layer)


class Screen(BlendMode):
    """Multiply inverse colors and invert the result."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return 1 - (1 - base) * (1 - layer)


class ColorDodge(BlendMode):
    """Lighten through Color Dodge with defined black and white endpoints."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return color_dodge(base, layer)


class LinearDodge(BlendMode):
    """Add corresponding RGB values and clip at white."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.clip(base + layer, 0, 1)


class LighterColor(BlendMode):
    """Select the whole RGB pixel with the higher channel sum; ties keep base."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        choose_base = base.sum(axis=-1, keepdims=True) >= layer.sum(axis=-1, keepdims=True)
        return np.where(choose_base, base, layer)
