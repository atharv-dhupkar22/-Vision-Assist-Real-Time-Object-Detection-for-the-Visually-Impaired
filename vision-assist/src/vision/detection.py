from ultralytics import YOLO
import numpy as np
import cv2
from typing import List, Tuple, Dict


class ObjectDetector:
    """
    Wrapper around Ultralytics YOLO to return easy-to-use detections
    plus an annotated frame for display.
    """

    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        conf_thres: float = 0.35,
        device: str = "cpu",
    ):
        self.model = YOLO(model_path)
        self.model.fuse()                     # speed boost
        self.conf_thres = conf_thres
        self.device = device
        self.names = self.model.names         # class-id → label dict

    def detect(
        self, frame: np.ndarray
    ) -> Tuple[List[Dict], np.ndarray]:
        """
        Returns:
            detections  – list[{label, conf, bbox(x1,y1,x2,y2)}]
            annotated   – frame with boxes and labels drawn
        """
        results = self.model(
            frame, conf=self.conf_thres, verbose=False, device=self.device
        )[0]

        detections = []
        for box in results.boxes:
            conf = float(box.conf)
            cls  = int(box.cls)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append(
                {"label": self.names[cls], "conf": conf, "bbox": (x1, y1, x2, y2)}
            )

        annotated = results.plot()            # Ultralytics helper draws bboxes
        return detections, annotated
