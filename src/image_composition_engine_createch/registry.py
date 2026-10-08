from .filters import Blur, Brightness, Contrast, GaussianBlur

FILTERS = { 
    "brightness": lambda params: Brightness(**params),
    "contrast": lambda params: Contrast(**params),
    "boxblur": lambda params: Blur(**params),
    "gaussianblur": lambda params: GaussianBlur(**params),
}

def create_filter(name: str, params: dict | None = None): # Partially made by AI
    """Create a registered filter; interpret window as a blur radius."""

    if not isinstance(name, str) or name not in FILTERS:
        raise ValueError(f"Unknown filter: {name!r}")

    if params is not None and not isinstance(params, dict):
        raise TypeError("Filter parameters must be a dictionary.")

    settings = {} if params is None else params.copy()

    if name in {"boxblur", "gaussianblur"} and "window" in settings:
        if "radius" in settings:
            raise ValueError("Use either window or radius, not both.")
        settings["radius"] = settings.pop("window")

    try:
        return FILTERS[name](settings)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Invalid parameters for {name!r}: {error}"
        ) from error