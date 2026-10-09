"""Explicit factories for filters and Adobe-style blending mode names."""

from .blends.comparative import Difference, Divide, Exclusion, Subtract
from .blends.contrast import HardLight, HardMix, LinearLight, Overlay, PinLight, SoftLight, VividLight
from .blends.darken import ColorBurn, Darken, DarkerColor, LinearBurn, Multiply
from .blends.hsl import Color, Hue, Luminosity, Saturation
from .blends.lighten import ColorDodge, Lighten, LighterColor, LinearDodge, Screen
from .blends.normal import Behind, Clear, Dissolve, Normal
from .external_filters.bubble_pop import BubblePop
from .external_filters.glitch import Glitch
from .external_filters.hue import Hue as HueFilter
from .external_filters.pixelate import Pixelate
from .filters import Blur, Brightness, Contrast, GaussianBlur, Invert


FILTERS = {
    "brightness": lambda params: Brightness(**params),
    "contrast": lambda params: Contrast(**params),
    "invert": lambda params: Invert(**params),
    "boxblur": lambda params: Blur(**params),
    "gaussianblur": lambda params: GaussianBlur(**params),
    "pixelate": lambda params: Pixelate(**params),
    "glitch": lambda params: Glitch(**params),
    "hue": lambda params: HueFilter(**params),
    "bubble_pop": lambda params: BubblePop(**params),
}

BLENDS = {
    "normal": Normal,
    "dissolve": Dissolve,
    "behind": Behind,
    "clear": Clear,
    "darken": Darken,
    "multiply": Multiply,
    "color_burn": ColorBurn,
    "linear_burn": LinearBurn,
    "darker_color": DarkerColor,
    "lighten": Lighten,
    "screen": Screen,
    "color_dodge": ColorDodge,
    "linear_dodge": LinearDodge,
    "lighter_color": LighterColor,
    "overlay": Overlay,
    "soft_light": SoftLight,
    "hard_light": HardLight,
    "vivid_light": VividLight,
    "linear_light": LinearLight,
    "pin_light": PinLight,
    "hard_mix": HardMix,
    "difference": Difference,
    "exclusion": Exclusion,
    "subtract": Subtract,
    "divide": Divide,
    "hue": Hue,
    "saturation": Saturation,
    "color": Color,
    "luminosity": Luminosity,
}


def create_filter(name: str, params: dict | None = None):
    """Create a filter; constructors validate their own numeric parameters."""
    if not isinstance(name, str) or name not in FILTERS:
        raise ValueError(f"Unknown filter: {name!r}.")
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
        raise ValueError(f"Invalid parameters for {name!r}: {error}") from error


def create_blend(name: str):
    """Create an RGB or alpha-aware blending mode from its registered name."""
    if not isinstance(name, str) or name not in BLENDS:
        raise ValueError(f"Unknown blending mode: {name!r}.")
    return BLENDS[name]()
