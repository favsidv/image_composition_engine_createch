from pathlib import Path
import numpy as np

from .image_io import load_image
from .pipeline import apply_filters

def prepare_layer(layer: dict, base_directory: str | Path) -> np.ndarray:
    """Load and filter one validated layer as RGBa pixels.

    Relative image paths are resolved from base_directory. Absolute image paths are accepted unchanged.
    """

    image_path = Path(base_directory)/ layer["image"]
    image = load_image(image_path)

    return apply_filters(image, layer.get("filters",[]))