from pathlib import Path
import numpy as np

from .image_io import load_image
from .pipeline import apply_filters
from .compositing import compose_layer

def prepare_layer(layer: dict, base_directory: str | Path) -> np.ndarray:
    """Load and filter one validated layer as RGBa pixels.

    Relative image paths are resolved from base_directory. Absolute image paths are accepted unchanged.
    """

    image_path = Path(base_directory)/ layer["image"]
    image = load_image(image_path)

    return apply_filters(image, layer.get("filters",[]))

def compose_layers(layers: list[dict], base_directory: str | Path) -> np.ndarray:
    """Compose validated layers in order, starting from a transparent canvas.
    All images must have matching dimensions. THe first layer also uses its configured opacity. Errors identify the one-based layer number.
"""
    if not layers:
        raise ValueError("At least one layer is required.")

    result = None

    for number, layer in enumerate(layers, start=1):
        try:
            image = prepare_layer(layer, base_directory)
            if result is None:
                result = np.zeros_like(image)
            result = compose_layer(
                result,
                image,
                blend=layer.get("blend", "normal"),
                opacity=layer.get("opacity", 1.0),
            )

        except (OSError, TypeError, ValueError) as error:
            raise ValueError(f"Layer {number}: {error}") from error

    return result
