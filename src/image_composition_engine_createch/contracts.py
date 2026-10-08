from abc import ABC, abstractmethod
import numpy as np

class Filter(ABC):
    """Reference interface for RGB filters configured with a dictionary."""

    def __init__(self, params:dict) -> None:
        """Keep a shallow copy of the filter parameters."""
        self.params = params.copy()

    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return a new RGB array without modifying the input.

        Input values are in [0,1]. Preserve shape and float32/float64 dtype. The pipeline clips output values to [0, 1]"""

        raise NotImplementedError

class BlendMode(ABC):
    """Reference interface for RGB blending"""

    @abstractmethod
    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Return blended RGB values without modifying either input.

        Inputs have the same shape (height width, 3) and values in [0, 1]. Return a floating point array of the same shape with finite values."""
        raise NotImplementedError