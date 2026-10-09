"""RGB filters returning independent, normalized floating-point arrays."""

import math

import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter

from .contracts import Filter
from .validation import validate_normalized_image


def _finite_number(value: float, name: str) -> None:
    """Reject booleans and nonfinite filter parameters."""
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number.")


def _radius(value: int) -> None:
    """Check the radius of a spatial filter."""
    if type(value) is not int or value < 0:
        raise ValueError("radius must be a nonnegative integer.")


class Brightness(Filter):
    """Add level to RGB values; zero leaves the image unchanged."""

    def __init__(self, level: float) -> None:
        _finite_number(level, "level")
        self.level = level

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return brighter or darker RGB pixels, clipped to [0, 1]."""
        validate_normalized_image(image, channels=3)
        level = max(-1.0, min(1.0, self.level))
        return np.clip(image + level, 0, 1)


class Contrast(Filter):
    """Scale RGB distances from middle gray; level one preserves colors."""

    def __init__(self, level: float) -> None:
        _finite_number(level, "level")
        if level < 0:
            raise ValueError("Contrast level must be nonnegative.")
        self.level = level

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return contrast-adjusted RGB pixels, clipped to [0, 1]."""
        validate_normalized_image(image, channels=3)
        level = min(self.level, float(np.finfo(image.dtype).max))
        return np.clip((image - 0.5) * level + 0.5, 0, 1)


class Invert(Filter):
    """Replace each RGB value with its complement."""

    def __init__(self) -> None:
        super().__init__({})

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return one minus each RGB channel without modifying the input."""
        validate_normalized_image(image, channels=3)
        return 1 - image


class Blur(Filter):
    """Average a square neighborhood of width 2 * radius + 1.

    At image edges, average only existing pixels. Channels are never mixed.
    """

    def __init__(self, radius: int) -> None:
        _radius(radius)
        self.radius = radius

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return a box blur with cropped, renormalized edge neighborhoods."""
        validate_normalized_image(image, channels=3)
        size = 2 * self.radius + 1
        colors = uniform_filter(image, size=(size, size, 1), mode="constant")
        weights = uniform_filter(
            np.ones(image.shape[:2], dtype=image.dtype), size=size, mode="constant"
        )
        return np.clip(colors / weights[..., None], 0, 1)


class GaussianBlur(Filter):
    """Apply Gaussian weights within a specified pixel radius.

    Renormalize the kernel at image edges and process RGB independently.
    """

    def __init__(self, radius: int, sigma: float) -> None:
        _radius(radius)
        _finite_number(sigma, "sigma")
        if sigma <= 0:
            raise ValueError("sigma must be positive.")
        self.radius = radius
        self.sigma = sigma

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return a Gaussian blur with the input shape and floating dtype."""
        validate_normalized_image(image, channels=3)
        colors = gaussian_filter(
            image, sigma=(self.sigma, self.sigma, 0),
            radius=(self.radius, self.radius, 0), mode="constant",
        )
        weights = gaussian_filter(
            np.ones(image.shape[:2], dtype=image.dtype),
            sigma=self.sigma, radius=self.radius, mode="constant",
        )
        return np.clip(colors / weights[..., None], 0, 1)
