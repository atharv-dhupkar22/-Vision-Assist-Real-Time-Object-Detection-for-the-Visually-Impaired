"""
Real-Time Object Detection with Audio Feedback
Run:  python main.py
Stop: press Q in the video window
"""

import cv2
from src.vision.detection import ObjectDetector
from src.audio.tts import SpeechEngine
from src.utils.helpers import throttle

# ------------ Configuration -------------
MODEL_PATH   = "yolov8n.pt"   # ultralytics provides small YOLOv8n by default
CONF_THRESH  = 0.35
VOICE_RATE   = 180            # words per minute
COOLDOWN_SEC = 2.0            # don't repeat the same label within this time
# ----------------------------------------

def main() -> None:
    detector = ObjectDetector(model_path=MODEL_PATH, conf_thres=CONF_THRESH)
    speaker  = SpeechEngine(rate=VOICE_RATE)

    # Prevent spamming the same label too often
    say_if_new = throttle(cooldown=COOLDOWN_SEC)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise RuntimeError("❌ Could not open webcam. Check permissions / index.")

    print("✅ Camera started. Press Q to quit.")
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        detections, annotated = detector.detect(frame)

        # Speak each unique object, throttled
        for det in detections:
            label = det["label"]
            if say_if_new(label):
                speaker.say(f"{label} ahead")

        # Show annotated video for debugging
        cv2.imshow("Vision-Assist (press Q to quit)", annotated)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

# ⬆️  keep existing imports
from src.utils.logger import DetectionLogger          # NEW

# ------------ Configuration -------------
MODEL_PATH   = "yolov8n.pt"
CONF_THRESH  = 0.35
VOICE_RATE   = 180
COOLDOWN_SEC = 2.0
LANGUAGE     = "en"          # 🔄 change to "hi", "mr", "fr", etc.
# ----------------------------------------

def main() -> None:
    detector = ObjectDetector(model_path=MODEL_PATH, conf_thres=CONF_THRESH)
    speaker  = SpeechEngine(rate=VOICE_RATE, lang=LANGUAGE)   # UPDATED
    logger   = DetectionLogger()                              # NEW

    say_if_new = throttle(cooldown=COOLDOWN_SEC)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise RuntimeError("❌ Could not open webcam.")

    print("✅ Camera started. Press Q to quit.")
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        detections, annotated = detector.detect(frame)

        for det in detections:
            label = det["label"]
            if say_if_new(label):
                spoken = f"{label} ahead"
                speaker.say(spoken)    # speak
                logger.write(label)    # log                🔥 NEW

        cv2.imshow("Vision-Assist (press Q to quit)", annotated)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

    cam.release()
    cv2.destroyAllWindows()
