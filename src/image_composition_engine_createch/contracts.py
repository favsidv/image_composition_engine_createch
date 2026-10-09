from abc import ABC, abstractmethod

import numpy as np


from .filters import Filter


class BlendMode(ABC):
    """Interface for RGB mixing without opacity or alpha composition."""

    @abstractmethod
    def apply(self, base: np.ndarray, layer: np.ndarray) -> np.ndarray:
        """Mix same-sized RGB arrays in [0, 1] without modifying the inputs.

        Return independent normalized pixels in the common floating dtype.
        """
        raise NotImplementedError


class AlphaBlendMode(ABC):
    """Interface for modes whose operation also changes transparency."""

    @abstractmethod
    def compose(
        self, base: np.ndarray, layer: np.ndarray, opacity: float
    ) -> np.ndarray:
        """Return a new RGBA composite of normalized, same-sized inputs."""
        raise NotImplementedError
