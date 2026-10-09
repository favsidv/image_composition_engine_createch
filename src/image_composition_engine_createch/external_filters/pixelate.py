import numpy as np
from .base import Filter


class Pixelate(Filter):
    """Pixelate an image by replacing each block with its average color."""

    name = "pixelate"

    def __init__(self, size: int):
        """Initialize the pixelation filter."""
        if size <= 0:
            raise ValueError("Pixelate size must be greater than 0.")

        self.size = size

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply pixelation to an RGB image."""
        result = np.array(image, copy=True)
        height, width, _ = image.shape

        for y in range(0, height, self.size):
            for x in range(0, width, self.size):
                block = image[y:y + self.size, x:x + self.size]
                mean_color = block.mean(axis=(0, 1))
                result[y:y + self.size, x:x + self.size] = mean_color

        return result
