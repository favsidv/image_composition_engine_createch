import numpy as np

from .contracts import AlphaBlendMode
from .registry import create_blend
from .validation import validate_image

def compose_layer(
    base: np.ndarray,
    layer: np.ndarray,
    blend: str = "normal",
    opacity: float = 1.0,
) -> np.ndarray:
    """Compose RGBA layers using RGB mixing or an alpha-aware painting mode.

    Inputs must share dimensions and use straight alpha in [0, 1].
    Opacity multiplies layer alpha. Return a new array in the common dtype.
    Fully transparent output pixels receive zero RGB values.

    Behind uses destination-over; Clear erases through the layer alpha;
    Dissolve samples a per-pixel coverage mask.
    Reference: https://www.w3.org/TR/compositing-1/#generalformula
    """
    validate_image(base, channels=4)
    validate_image(layer, channels=4)

    if base.shape != layer.shape:
        raise ValueError("Layers must have the same dimensions.")

    if type(opacity) not in (int, float) or not 0 <= opacity <= 1:
        raise ValueError("Opacity must be a number between 0 and 1.")

    if np.any((base < 0) | (base > 1)) or np.any((layer < 0) | (layer > 1)):
        raise ValueError("Layer pixels must be between 0 and 1.")

    mode = create_blend(blend)
    if isinstance(mode, AlphaBlendMode):
        result = mode.compose(base, layer, opacity)
        validate_image(result, channels=4)
        if result.shape != base.shape:
            raise ValueError("A blending mode must preserve the image dimensions.")
        return np.clip(result, 0, 1).astype(np.result_type(base.dtype, layer.dtype), copy=False)

    base_rgb = base[..., :3]
    layer_rgb = layer[..., :3]
    mixed = mode.apply(base_rgb.copy(), layer_rgb.copy())
    validate_image(mixed, channels=3)

    if mixed.shape != base_rgb.shape:
        raise ValueError("A blending mode must preserve the image dimensions.")

    mixed = np.clip(mixed, 0, 1)
    base_alpha = base[..., 3:4]
    layer_alpha = layer[..., 3:4] * opacity
    output_alpha = layer_alpha + base_alpha * (1 - layer_alpha)

    color = (
        base_rgb * base_alpha * (1 - layer_alpha)
        + layer_rgb * layer_alpha * (1 - base_alpha)
        + mixed * base_alpha * layer_alpha
    )

    rgb = np.divide(
        color,
        output_alpha,
        out=np.zeros_like(color),
        where=output_alpha > 0,
    )
    result = np.clip(np.concatenate((rgb, output_alpha), axis=2), 0, 1)
    return result.astype(np.result_type(base.dtype, layer.dtype), copy=False)