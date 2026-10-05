"""Lab 02 interface for preparing images for inference."""

from typing import Tuple

import numpy as np


class ImagePreprocessor:
    """Resize BGR frames and produce normalized RGB model inputs."""

    def preprocess(
        self, frame: np.ndarray, target_size: Tuple[int, int]
    ) -> np.ndarray:
        """Return an H x W x 3 float32 RGB array in [0, 1].

        Input is a uint8 BGR frame; target_size is (width, height).
        This contract uses direct resizing without letterboxing.
        """
        raise NotImplementedError("Image preprocessing is not implemented.")
