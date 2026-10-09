"""Comparative blend modes for normalized RGB image arrays."""

import numpy as np

from ..contracts import BlendMode
from ._utils import prepare_images


class Difference(BlendMode):
    """Return the absolute difference between corresponding channels."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.abs(base - layer)


class Exclusion(BlendMode):
    """Combine RGB values with lower contrast than Difference."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.clip(base + layer - 2 * base * layer, 0, 1)


class Subtract(BlendMode):
    """Subtract the layer RGB values and clip negative results to black."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.clip(base - layer, 0, 1)


class Divide(BlendMode):
    """Divide RGB values, saturating at white; define division by zero as one."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        result = np.divide(base, layer, out=np.ones_like(base), where=layer > base)
        return np.clip(result, 0, 1)
