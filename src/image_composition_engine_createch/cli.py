from pathlib import Path
from .application import compose_from_file

CONFIG_PATH = Path("conf.json")
OUTPUT_PATH = Path("output/result.png")

def main() -> None:
    """Compose the configured image layers from the project root."""
    try:
        output = compose_from_file(CONFIG_PATH, OUTPUT_PATH)
    except (OSError, TypeError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from error

    print(f"Image saved to {output}")