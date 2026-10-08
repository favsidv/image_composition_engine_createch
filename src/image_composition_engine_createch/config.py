import json
from pathlib import Path
import yaml

from .registry import create_blend, create_filter

def load_config(path: str | Path) -> dict:
    """Read a JSON or YAML configuration and validate its structure."""

    path = Path(path)
    suffix = path.suffix.lower()

    if suffix not in {".json", ".yml", ".yaml"}:
        raise ValueError("Configuration must be a JSON or YAML file")

    try:
        with path.open(encoding="utf-8") as file:
            config = (
                json.load(file)
                if suffix == ".json"
                else yaml.safe_load(file)
            )
    except (json.JSONDecodeError, yaml.YAMLError) as error:
        raise ValueError(f"Invalid configuration in {path}: {error}") from error

    validate_config(config)
    return config

def validate_config(config: dict) -> None: # Partially made by AI.
    """Check required fields and registered operations without loading images"""

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary.")

    layers = config.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("Configuration must contain a nonempty layers list.")

    for number, layer in enumerate(layers, start=1):
        try:
            if not isinstance(layer, dict):
                raise ValueError("Each layer must be a dictionary.")

            image = layer.get("image")
            if not isinstance(image, str) or not image.strip():
                raise ValueError("image must be a nonempty path string.")

            opacity = layer.get("opacity", 1.0)
            if type(opacity) not in (int, float) or not 0 <= opacity <= 1:
                raise ValueError("opacity must be a number between 0 and 1.")

            create_blend(layer.get("blend", "normal"))

            filters = layer.get("filters", [])
            if not isinstance(filters, list):
                raise ValueError("filters must be a list.")

            for settings in filters:
                if not isinstance(settings, dict):
                    raise ValueError("Each filter must be a dictionary.")

                params = settings.get("params", {})
                if not isinstance(params, dict):
                    raise ValueError("Filter params must be a dictionary.")

                create_filter(settings.get("name"), params)

        except (TypeError, ValueError) as error:
            raise ValueError(f"Layer {number}: {error}") from error