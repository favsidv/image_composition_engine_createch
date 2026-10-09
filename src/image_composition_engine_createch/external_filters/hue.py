import colorsys
import numpy as np
from .base import Filter


class Hue(Filter):
    """Rotate the hue of an RGB image."""

    name = "hue"

    def __init__(self, angle: float):
        """Initialize the hue filter."""
        self.angle = angle

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply hue rotation to an RGB image."""
        result = np.array(image, copy=True)

        height, width, _ = image.shape

        for y in range(height):
            for x in range(width):
                r, g, b = image[y, x]

                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                h = (h + self.angle / 360.0) % 1.0

                result[y, x] = colorsys.hsv_to_rgb(h, s, v)

        return result
