"""Hue, saturation, color and luminosity using W3C nonseparable blending.

These modes use weighted luminosity rather than the lightness of HSL color
conversion. Reference: https://www.w3.org/TR/compositing-1/#blendingnonseparable
"""

import numpy as np

from ..contracts import BlendMode
from ._utils import prepare_images


def luminosity(image: np.ndarray) -> np.ndarray:
    """Return weighted RGB luminosity with shape (height, width, 1)."""
    weights = np.array([0.3, 0.59, 0.11], dtype=image.dtype)
    return np.sum(image * weights, axis=-1, keepdims=True)


def saturation(image: np.ndarray) -> np.ndarray:
    """Return the channel range of each pixel, keeping the last dimension."""
    return np.max(image, axis=-1, keepdims=True) - np.min(image, axis=-1, keepdims=True)


def set_saturation(image: np.ndarray, value: np.ndarray) -> np.ndarray:
    """Scale channel differences to value; grayscale pixels stay achromatic."""
    minimum = np.min(image, axis=-1, keepdims=True)
    span = saturation(image)
    scaled = np.divide(image - minimum, span, out=np.zeros_like(image), where=span > 0)
    return scaled * value


def set_luminosity(image: np.ndarray, value: np.ndarray) -> np.ndarray:
    """Set weighted luminosity and bring colors into gamut without changing it."""
    result = image + value - luminosity(image)
    minimum = np.min(result, axis=-1, keepdims=True)
    scale = np.divide(value, value - minimum, out=np.ones_like(value), where=value > minimum)
    result = np.where(minimum < 0, value + (result - value) * scale, result)
    maximum = np.max(result, axis=-1, keepdims=True)
    scale = np.divide(1 - value, maximum - value, out=np.ones_like(value), where=maximum > value)
    result = np.where(maximum > 1, value + (result - value) * scale, result)
    return np.clip(result, 0, 1)


class Hue(BlendMode):
    """Take layer hue while retaining base saturation and luminosity."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return normalized RGB colors without modifying either input."""
        base, layer = prepare_images(base, layer)
        return set_luminosity(set_saturation(layer, saturation(base)), luminosity(base))


class Saturation(BlendMode):
    """Take layer saturation while retaining base hue and luminosity."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return normalized RGB colors without modifying either input."""
        base, layer = prepare_images(base, layer)
        return set_luminosity(set_saturation(base, saturation(layer)), luminosity(base))


class Color(BlendMode):
    """Take layer hue and saturation while retaining base luminosity."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return normalized RGB colors without modifying either input."""
        base, layer = prepare_images(base, layer)
        return set_luminosity(layer, luminosity(base))


class Luminosity(BlendMode):
    """Take layer luminosity while retaining base hue and saturation."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return normalized RGB colors without modifying either input."""
        base, layer = prepare_images(base, layer)
        return set_luminosity(base, luminosity(layer))
