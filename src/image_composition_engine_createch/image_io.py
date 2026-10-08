from pathlib import Path

import numpy as np
from PIL import Image

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