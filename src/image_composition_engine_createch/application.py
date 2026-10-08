from pathlib import Path

from .config import load_config
from .engine import compose_layers
from .image_io import save_image

def compose_from_file(config_path: str | Path, output_path: str | Path) -> Path:
    """Read a configuration, compose its layers and save a PNG

    Image paths are relative to the configuration directory. A relative output path is interpreted from the current working directory.
    Return the absolute path to the saved image.

    """
    config_path = Path(config_path).resolve()
    output_path = Path(output_path).resolve()

    if output_path.suffix.lower()!=".png":
        raise ValueError("The output file must have a .png extension.")

    config = load_config(config_path)
    result = compose_layers(config["layers"],config_path.parent)

    save_image(result, output_path)
    return output_path