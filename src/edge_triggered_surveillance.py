"""Lab 03 Task 8: save high-priority detections with a cooldown. Press q to quit."""

import argparse
import json
from datetime import datetime
from time import monotonic

try:
    from .live_detection import ROOT, draw_detections, load_model
except ImportError:
    from live_detection import ROOT, draw_detections, load_model

import cv2


def run(target: str = "person", cooldown: float = 5.0) -> None:
    """Log the strongest matching detection once per cooldown period."""
    if cooldown < 1.0:
        raise ValueError("Cooldown must be at least 1 second to preserve unique filenames.")
    if target not in ("person", "cell phone"):
        raise ValueError("Target must be person or cell phone.")
    model = load_model()
    target_id = next(index for index, name in model.names.items() if name == target)
    cap = cv2.VideoCapture(0)
    last_saved = float("-inf")
    try:
        if not cap.isOpened():
            raise RuntimeError("Cannot open webcam 0. Check camera access and other apps.")
        while True:
            success, frame = cap.read()
            if not success:
                print("Camera frame could not be read; stopping.")
                break
            result = model.predict(frame, imgsz=640, conf=0.65,
                                   classes=[target_id], verbose=False)[0]
            # Enforce strictly greater than 0.65, even at the threshold boundary.
            matches = [box for box in result.boxes if float(box.conf.item()) > 0.65]
            display = draw_detections(frame, result)
            now = monotonic()
            status = f"Monitoring: {target}"
            color = (0, 255, 0)
            if matches:
                color = (0, 0, 255)
                remaining = max(0.0, cooldown - (now - last_saved))
                status = f"ALERT: {target} | cooldown {remaining:.1f}s"
                if remaining == 0.0:
                    detected = max(matches, key=lambda box: float(box.conf.item()))
                    timestamp = datetime.now().astimezone()
                    directory = ROOT / "outputs" / "lab03" / "alerts"
                    directory.mkdir(parents=True, exist_ok=True)
                    path = directory / (timestamp.strftime("%Y%m%d_%H%M%S") + ".jpg")
                    # A second launch in the same second must not overwrite evidence.
                    if not path.exists():
                        cv2.putText(display, "ALERT LOGGED", (10, 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                        if not cv2.imwrite(str(path), display):
                            raise OSError(f"Could not save {path}")
                        event = {
                            "timestamp": timestamp.isoformat(timespec="seconds"),
                            "class_name": target,
                            "confidence": round(float(detected.conf.item()), 4),
                            "bounding_box": [round(value, 2) for value in detected.xyxy[0].cpu().tolist()],
                            "snapshot": str(path.relative_to(ROOT)),
                        }
                        with (directory.parent / "events.log").open("a", encoding="utf-8") as log:
                            log.write(json.dumps(event) + "\n")
                        last_saved = now
                        status = f"ALERT LOGGED: {target}"
                        print(json.dumps(event))
            cv2.putText(display, status, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
            cv2.imshow("Lab 03 - Edge-Triggered Surveillance", display)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("person", "cell phone"), default="person")
    parser.add_argument("--cooldown", type=float, default=5.0, help="Seconds between alerts; minimum 1")
    args = parser.parse_args()
    run(args.target, args.cooldown)


if __name__ == "__main__":
    main()
