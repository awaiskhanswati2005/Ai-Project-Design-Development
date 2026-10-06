"""Lab 03 Task 7: local webcam detection. Press q to quit or s to save."""

import argparse
import os
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
# Keep library configuration inside the existing, ignored environment folder.
CACHE = ROOT / "aipdd_env" / "lab03_cache"
for name, folder in (("MPLCONFIGDIR", "matplotlib"), ("YOLO_CONFIG_DIR", "ultralytics")):
    directory = CACHE / folder
    directory.mkdir(parents=True, exist_ok=True)
    os.environ[name] = str(directory)

import cv2
import numpy as np
from ultralytics import YOLO


def load_model(model_name: str = "yolov8n.pt") -> YOLO:
    """Load a supported pretrained model; Ultralytics downloads missing weights."""
    weights = ROOT / "models" / model_name
    weights.parent.mkdir(parents=True, exist_ok=True)
    return YOLO(str(weights))


def draw_detections(frame: np.ndarray, result: Any) -> np.ndarray:
    """Draw YOLO boxes and labels manually on a copy of the BGR frame."""
    output = frame.copy()
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().tolist())
        label = result.names[int(box.cls.item())]
        confidence = float(box.conf.item())
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 200, 255), 2)
        cv2.putText(output, f"{label} {confidence:.2f}", (x1, max(20, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
    return output


def run(model_name: str = "yolov8n.pt") -> None:
    """Capture webcam 0 and display measured processing FPS."""
    model = load_model(model_name)
    cap = cv2.VideoCapture(0)
    try:
        if not cap.isOpened():
            raise RuntimeError("Cannot open webcam 0. Check camera access and other apps.")
        while True:
            started = perf_counter()
            success, frame = cap.read()
            if not success:
                print("Camera frame could not be read; stopping.")
                break
            result = model.predict(frame, imgsz=640, conf=0.25, verbose=False)[0]
            display = draw_detections(frame, result)
            fps = 1.0 / max(perf_counter() - started, 1e-6)
            cv2.putText(display, f"FPS: {fps:.1f} | q: quit | s: save", (10, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.imshow("Lab 03 - Live Detection", display)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("s"):
                directory = ROOT / "outputs" / "lab03" / "webcam"
                directory.mkdir(parents=True, exist_ok=True)
                path = directory / (datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg")
                if not cv2.imwrite(str(path), display):
                    raise OSError(f"Could not save {path}")
                print(f"Saved {path.relative_to(ROOT)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=("yolov8n.pt", "yolov8m.pt"), default="yolov8n.pt")
    args = parser.parse_args()
    run(args.model)


if __name__ == "__main__":
    main()
