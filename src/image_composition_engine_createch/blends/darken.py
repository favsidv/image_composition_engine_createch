"""Darken blend modes for normalized RGB image arrays."""

import numpy as np

from ..contracts import BlendMode
from ._utils import prepare_images, color_burn


class Darken(BlendMode):
    """Keep the lower value of each RGB channel."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.minimum(base, layer)


class Multiply(BlendMode):
    """Multiply corresponding RGB channels."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return base * layer


class ColorBurn(BlendMode):
    """Darken through Color Burn with defined black and white endpoints."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return color_burn(base, layer)


class LinearBurn(BlendMode):
    """Add RGB values and subtract one, clipping at black."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.clip(base + layer - 1, 0, 1)


class DarkerColor(BlendMode):
    """Select the whole RGB pixel with the lower channel sum; ties keep base."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        choose_base = base.sum(axis=-1, keepdims=True) <= layer.sum(axis=-1, keepdims=True)
        return np.where(choose_base, base, layer)
