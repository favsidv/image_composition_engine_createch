import numpy as np

from .registry import create_filter
from .validation import validate_image

def apply_filters(image: np.ndarray, filters: list[dict]) -> np.ndarray:
    """Apply filters in order to RGB, keeping alpha unchanged.

    Return an independent RGBA array with the input shape and dtype. clip finite filter results to [0, 1] after each operation.
    """
    validate_image(image, channels=4)
    result = image.copy()

    for settings in filters:
        name = settings["name"]

        try:
            operation = create_filter(name, settings.get("params", {}))
            rgb = operation.apply(result[..., :3].copy())

            validate_image(rgb, channels=3)
            if rgb.shape != result[..., :3].shape:
                raise ValueError("A filter must preserve the image dimensions.")

            result[..., :3] = np.clip(rgb, 0, 1)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Filter {name!r}: {error}.") from error
    return result
    