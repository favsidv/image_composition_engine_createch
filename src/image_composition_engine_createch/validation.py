import numpy as np

def validate_image(image: np.ndarray, channels: int | None = None) -> None:
    """Check shape, floating-point dtype and finite values.

    Accept nonempty RGB or RGBA arrays using float32 or float64. Values outside [0, 1] are allowed; this function does not clip them. Raise TypeError for invalid types and ValueError for invalid data.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("Expected a NumPy array.")

    if image.dtype not in (np.float32, np.float64):
        raise TypeError("Expected float32 or float64 pixels")

    if image.ndim != 3 or image.shape[2] not in (3, 4) or image.size == 0:
        raise ValueError(
            "Expected a nonempty image with shape (height, width, 3 or 4)"
        )
    if channels is not None and image.shape[2] != channels:
        raise ValueError(f"Expected {channels} channels.")

    if not np.isfinite(image).all():
        raise ValueError("Pixels must contain only finite values.")