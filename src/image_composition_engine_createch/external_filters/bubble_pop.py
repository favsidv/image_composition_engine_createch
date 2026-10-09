import numpy as np
from scipy.ndimage import map_coordinates
from .base import Filter


class BubblePop(Filter):
    """Add stylized soap-bubble effects across an image."""

    name = "bubble_pop"

    def __init__(
        self,
        amount: int = 20,
        average_size: int = 100,
        opacity: float = 0.5,
    ):
        """Initialize the bubble pop filter."""
        if amount <= 0:
            raise ValueError("Bubble amount must be greater than 0.")

        if average_size <= 0:
            raise ValueError("Bubble average size must be greater than 0.")

        if not 0.0 <= opacity <= 1.0:
            raise ValueError("Bubble opacity must be between 0 and 1.")

        self.amount = amount
        self.average_size = average_size
        self.opacity = opacity

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply stylized soap bubbles to an image."""
        result = np.array(image, copy=True)

        height, width, channels = image.shape
        color_channels = min(3, channels)

        rng = np.random.default_rng()

        y, x = np.indices((height, width))

        for _ in range(self.amount):
            size = self.average_size * rng.uniform(0.7, 1.3)
            radius = max(8.0, size / 2)

            center_x = rng.uniform(0, width)
            center_y = rng.uniform(0, height)

            bubble_opacity = np.clip(
                self.opacity * rng.uniform(0.75, 1.15),
                0.0,
                1.0,
            )

            dx = x - center_x
            dy = y - center_y
            distance = np.sqrt(dx**2 + dy**2)
            normalized = distance / radius

            bubble_mask = normalized <= 1.0

            # -----------------------------
            # 1) Slight lens distortion
            # -----------------------------
            source_x = x.astype(float).copy()
            source_y = y.astype(float).copy()

            magnification = 1.0 - 0.18 * (1.0 - normalized)
            magnification[~bubble_mask] = 1.0

            source_x[bubble_mask] = center_x + dx[bubble_mask] * magnification[bubble_mask]
            source_y[bubble_mask] = center_y + dy[bubble_mask] * magnification[bubble_mask]

            distorted = np.zeros_like(result[:, :, :color_channels])

            for channel in range(color_channels):
                distorted[:, :, channel] = map_coordinates(
                    image[:, :, channel],
                    [source_y, source_x],
                    order=1,
                    mode="reflect",
                )

            interior_blend = bubble_opacity * 0.45

            for channel in range(color_channels):
                result[:, :, channel][bubble_mask] = (
                    result[:, :, channel][bubble_mask] * (1.0 - interior_blend)
                    + distorted[:, :, channel][bubble_mask] * interior_blend
                )

            # -----------------------------
            # 2) Soft inner bluish fill
            # -----------------------------
            fill_strength = bubble_opacity * 0.10 * (1.0 - normalized)
            fill_strength[~bubble_mask] = 0.0

            bluish_tint = np.array([0.92, 0.97, 1.00])

            for channel in range(color_channels):
                result[:, :, channel] = (
                    result[:, :, channel] * (1.0 - fill_strength)
                    + bluish_tint[channel] * fill_strength
                )

            # -----------------------------
            # 3) Main soft white border
            # -----------------------------
            border_mask = (normalized >= 0.84) & (normalized <= 1.0)
            border_strength = np.clip((normalized - 0.84) / 0.16, 0.0, 1.0)
            border_strength = (1.0 - border_strength) * bubble_opacity * 0.45
            border_strength[~border_mask] = 0.0

            for channel in range(color_channels):
                result[:, :, channel] += border_strength

            # -----------------------------
            # 4) Iridescent rainbow edge
            # -----------------------------
            rainbow_mask = (normalized >= 0.78) & (normalized <= 0.96)

            angle = np.arctan2(dy, dx)

            rainbow_r = 0.5 + 0.5 * np.cos(angle)
            rainbow_g = 0.5 + 0.5 * np.cos(angle + 2 * np.pi / 3)
            rainbow_b = 0.5 + 0.5 * np.cos(angle + 4 * np.pi / 3)

            rainbow_strength = np.clip((normalized - 0.78) / 0.18, 0.0, 1.0)
            rainbow_strength = (1.0 - rainbow_strength) * bubble_opacity * 0.18
            rainbow_strength[~rainbow_mask] = 0.0

            rainbow_colors = [rainbow_r, rainbow_g, rainbow_b]

            for channel in range(color_channels):
                result[:, :, channel] += rainbow_colors[channel] * rainbow_strength

            # -----------------------------
            # 5) Main highlight
            # -----------------------------
            highlight_x = center_x - radius * 0.28
            highlight_y = center_y - radius * 0.28
            highlight_radius = radius * 0.22

            hdx = x - highlight_x
            hdy = y - highlight_y
            hdist = np.sqrt(hdx**2 + hdy**2)

            highlight_mask = hdist <= highlight_radius
            highlight_strength = np.clip(1.0 - hdist / highlight_radius, 0.0, 1.0)
            highlight_strength *= bubble_opacity * 0.65
            highlight_strength[~highlight_mask] = 0.0

            for channel in range(color_channels):
                result[:, :, channel] += highlight_strength

            # -----------------------------
            # 6) Secondary small highlight
            # -----------------------------
            small_x = center_x - radius * 0.05
            small_y = center_y - radius * 0.42
            small_radius = radius * 0.08

            sdx = x - small_x
            sdy = y - small_y
            sdist = np.sqrt(sdx**2 + sdy**2)

            small_mask = sdist <= small_radius
            small_strength = np.clip(1.0 - sdist / small_radius, 0.0, 1.0)
            small_strength *= bubble_opacity * 0.55
            small_strength[~small_mask] = 0.0

            for channel in range(color_channels):
                result[:, :, channel] += small_strength

        return np.clip(result, 0.0, 1.0)
