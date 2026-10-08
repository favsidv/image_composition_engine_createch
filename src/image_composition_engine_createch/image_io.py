from pathlib import Path

import numpy as np
from PIL import Image

from .validation import validate_image

def load_image(path: str | Path) -> np.ndarray:
    """Load a supported single-frame image as normalized RGBA pixels.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the source image.

    Returns
    -------
    numpy.ndarray
        A float32 array of shape (height, width, 4), with values in [0, 1]. Existing alpha is preserved; opaque images receive alpha 1.

    Raises
    ------
    OSError
        If the file is missing, unreadable, or cannot be decoded.
    ValueError
        If the image mode is unsupported or it contains multiple frames.
    """
    with Image.open(path) as image:
        if image.mode not in {"1", "L", "LA", "P", "RGB", "RGBA", "CMYK"}:
            raise ValueError(f"Unsupported image mode {image.mode!r}: {path}.")
        if getattr(image, "n_frames", 1) != 1:
            raise ValueError(f"Expected a single-frame image: {path}.") # files suche as GIF, animated WebP or PNG and multilayer images are not supported here.

        rgba = image.convert("RGBA")
        pixels = np.array(rgba, dtype=np.float32)

    return pixels / np.float32(255.0)

def save_image(image: np.ndarray, path: str | Path) -> None:
    """Save RGB or RGBA float pixels as an 8-bit PNG.

    Clip finite values to [0, 1], round them to byte values and preserve alpha. Create missing parent directories without modifying the input array. An existing output file is replaced.
    """
    validate_image(image)

    path = Path(path)
    if path.suffix.lower() != ".png":
        raise ValueError("The output file must have a .png extension.")

    pixels = np.rint(np.clip(image,0,1) * 255).astype(np.uint8)
    path.parent.mkdir(parents = True, exist_ok = True)

    Image.fromarray(pixels).save(path, format="PNG")