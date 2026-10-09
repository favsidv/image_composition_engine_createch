from abc import ABC, abstractmethod

import numpy as np


class Filter(ABC):
    """Reference RGB filter interface; registries adapt constructor arguments."""

    def __init__(self, params: dict) -> None:
        """Keep a shallow copy of dictionary-based filter parameters."""
        self.params = params.copy()

    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Return independent RGB pixels with the input shape and float dtype.

        Inputs are normalized to [0, 1]. Do not modify the input array.
        The pipeline clips finite output values to [0, 1].
        """
        raise NotImplementedError


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
