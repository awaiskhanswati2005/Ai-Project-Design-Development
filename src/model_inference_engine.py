"""Lab 02 interface and result type for object detection."""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class Detection:
    """One raw detection with box coordinates in resized-image pixels."""

    label: str
    confidence: float
    bounding_box: Tuple[float, float, float, float]


class ModelInferenceEngine:
    """Load model weights and expose raw object detections."""

    def load_model(self, weights_path: str) -> None:
        """Accept a local weights path; return no value after loading."""
        raise NotImplementedError("Model loading is not implemented.")

    def predict(self, image: np.ndarray) -> List[Detection]:
        """Accept normalized RGB data; return raw detections (possibly empty).

        Each box is (x_min, y_min, x_max, y_max) in input-image pixels.
        Confidence values range from 0 to 1. Filtering and coordinate
        mapping belong to the planned post-processing stage.
        """
        raise NotImplementedError("Model inference is not implemented.")
