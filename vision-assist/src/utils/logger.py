import csv
from pathlib import Path
from datetime import datetime


class DetectionLogger:
    """
    Append each spoken detection to logs/detections.csv
    CSV format: timestamp, label
    """

    def __init__(self, log_dir: str = "logs", filename: str = "detections.csv"):
        Path(log_dir).mkdir(exist_ok=True)
        self.file = Path(log_dir) / filename
        # create header once
        if not self.file.exists():
            with self.file.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "label"])

    def write(self, label: str) -> None:
        ts = datetime.now().isoformat(timespec="seconds")
        with self.file.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([ts, label])
