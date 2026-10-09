import numpy as np
from .base import Filter


class Glitch(Filter):
    """Apply a static horizontal glitch effect."""

    name = "glitch"

    def __init__(self, intensity: float = 1.0, slices: int = 10):
        """Initialize the glitch filter."""
        if not 0.0 <= intensity <= 1.0:
            raise ValueError("Glitch intensity must be between 0 and 1.")

        if slices <= 0:
            raise ValueError("Glitch slices must be greater than 0.")

        self.intensity = intensity
        self.slices = slices

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the glitch effect to an RGB image."""
        result = np.array(image, copy=True)

        height, width, _ = image.shape

        max_shift = int(width * 0.08 * self.intensity)
        slice_height = max(1, height // self.slices)

        rng = np.random.default_rng()

        for y in range(0, height, slice_height):
            shift = rng.integers(-max_shift, max_shift + 1)

            result[y:y + slice_height] = np.roll(
                image[y:y + slice_height],
                shift=shift,
                axis=1,
            )

        return result
