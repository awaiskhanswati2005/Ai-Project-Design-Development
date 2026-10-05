"""Lab 02 interface for persisting events and sending alerts."""

from datetime import datetime
from typing import List, Tuple


class AlertLogger:
    """Record processed detections and deliver rule-approved alerts."""

    def log_event(
        self,
        camera_id: str,
        timestamp: datetime,
        labels: List[str],
        bounding_boxes: List[Tuple[float, float, float, float]],
        confidences: List[float],
    ) -> str:
        """Return the stored event ID for aligned detection lists.

        Timestamp must be timezone-aware. Boxes use original-frame pixel
        coordinates in (x_min, y_min, x_max, y_max) order. All three
        detection lists must have equal lengths.
        """
        raise NotImplementedError("Event persistence is not implemented.")

    def send_alert(self, event_id: str, message: str, recipient: str) -> bool:
        """Accept a stored event ID and destination; return delivery success."""
        raise NotImplementedError("Alert delivery is not implemented.")
