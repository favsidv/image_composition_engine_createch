"""Shared validation and safe channel arithmetic for blending modes."""

import numpy as np

from ..validation import validate_normalized_image


def prepare_images(
    base: np.ndarray, layer: np.ndarray, channels: int = 3
) -> tuple[np.ndarray, np.ndarray]:
    """Validate normalized inputs and promote them to a common float dtype."""
    validate_normalized_image(base, channels=channels)
    validate_normalized_image(layer, channels=channels)
    if base.shape != layer.shape:
        raise ValueError("Layers must have the same dimensions.")
    dtype = np.result_type(base.dtype, layer.dtype)
    return base.astype(dtype, copy=False), layer.astype(dtype, copy=False)


def check_opacity(opacity: float) -> None:
    """Require a finite Python number in [0, 1]."""
    if type(opacity) not in (int, float) or not 0 <= opacity <= 1:
        raise ValueError("Opacity must be a number between 0 and 1.")


def color_burn(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    """Evaluate Color Burn, preserving white and handling a zero divisor."""
    ratio = np.divide(1 - base, layer, out=np.ones_like(base), where=layer > 1 - base)
    return np.where(base == 1, 1, 1 - np.minimum(1, ratio))


def color_dodge(base: np.ndarray, layer: np.ndarray) -> np.ndarray:
    """Evaluate Color Dodge, preserving black and handling a zero divisor."""
    ratio = np.divide(base, 1 - layer, out=np.ones_like(base), where=1 - layer > base)
    return np.where(base == 0, 0, np.minimum(1, ratio))
