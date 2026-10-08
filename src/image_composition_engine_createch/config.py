import json
from pathlib import Path
import yaml

def load_config(path: str | Path) -> dict:
    """Read a JSON or YAML configuration as a dictionary."""


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

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary.")

    return config
