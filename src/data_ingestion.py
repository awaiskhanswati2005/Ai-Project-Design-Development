"""Lab 02 interface for reading camera frames."""

from typing import Optional

import numpy as np


class DataIngestion:
    """Connect to a video source and supply decoded BGR frames."""

    def connect(self, source_url: str) -> bool:
        """Accept an RTSP URL; return True when the connection succeeds."""
        raise NotImplementedError("Video connection is not implemented.")

    def read_frame(self) -> Optional[np.ndarray]:
        """Return an H x W x 3 uint8 BGR frame, or None if unavailable."""
        raise NotImplementedError("Frame reading is not implemented.")

    def close(self) -> None:
        """Release the active camera connection; return no value."""
        raise NotImplementedError("Connection cleanup is not implemented.")
