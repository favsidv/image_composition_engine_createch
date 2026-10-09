"""Contrast blend modes for normalized RGB image arrays."""

import numpy as np

from ..contracts import BlendMode
from ._utils import prepare_images, color_burn, color_dodge


class Overlay(BlendMode):
    """Multiply dark base channels and screen light base channels."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.where(base <= 0.5, 2 * base * layer, 1 - 2 * (1 - base) * (1 - layer))


class SoftLight(BlendMode):
    """Apply the W3C Soft Light curve, including its dark-color polynomial."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        curve = np.where(base <= 0.25, ((16 * base - 12) * base + 4) * base, np.sqrt(base))
        return np.clip(np.where(
            layer <= 0.5,
            base - (1 - 2 * layer) * base * (1 - base),
            base + (2 * layer - 1) * (curve - base),
        ), 0, 1)


class HardLight(BlendMode):
    """Multiply dark layer channels and screen light layer channels."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.where(layer <= 0.5, 2 * base * layer, 1 - 2 * (1 - base) * (1 - layer))


class VividLight(BlendMode):
    """Use Color Burn below middle gray and Color Dodge above it."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        dark = color_burn(base, np.minimum(2 * layer, 1))
        light = color_dodge(base, np.maximum(2 * layer - 1, 0))
        return np.where(layer <= 0.5, dark, light)


class LinearLight(BlendMode):
    """Add twice the layer value minus one and clip to [0, 1]."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.clip(base + 2 * layer - 1, 0, 1)


class PinLight(BlendMode):
    """Replace channels with a darker or lighter threshold from the layer."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return np.where(layer <= 0.5, np.minimum(base, 2 * layer), np.maximum(base, 2 * layer - 1))


class HardMix(BlendMode):
    """Threshold each channel sum at one, returning floating-point zeros or ones."""

    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return independent normalized RGB pixels in the common float dtype."""
        base, layer = prepare_images(base, layer)
        return (base + layer >= 1).astype(base.dtype)
