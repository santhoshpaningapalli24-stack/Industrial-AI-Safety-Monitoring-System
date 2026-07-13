"""
Object Detector
YOLOv8-based universal object detection
"""

from ultralytics import YOLO
import torch


class ObjectDetector:

    def __init__(self, settings):

        self.settings = settings

        self.model_path = "weights/yolov8n.pt"

        print(
            f"[INFO] Loading object detector: "
            f"{self.model_path}"
        )

        # =================================================
        # LOAD MODEL
        # =================================================

        self.model = YOLO(self.model_path)

        # =================================================
        # CLASS NAMES
        # =================================================

        self.class_names = self.model.names

        # =================================================
        # DEVICE
        # =================================================

        if torch.cuda.is_available():

            self.device = "cuda"

        else:

            self.device = "cpu"

        print(
            f"[INFO] ObjectDetector running on "
            f"{self.device.upper()}"
        )

        print(
            "[INFO] Object detector ready"
        )

    # =====================================================
    # DETECT
    # =====================================================

    def detect(self, frame):

        detections = []

        try:

            # =============================================
            # YOLO INFERENCE
            # =============================================

            results = self.model(

                frame,

                verbose=False,

                device=self.device,

                conf=0.35

            )

            # =============================================
            # PARSE RESULTS
            # =============================================

            for r in results:

                if r.boxes is None:
                    continue

                for box in r.boxes:

                    try:

                        # =============================
                        # CLASS
                        # =============================

                        cls_id = int(
                            box.cls[0].item()
                        )

                        label = self.class_names[
                            cls_id
                        ]

                        # =============================
                        # CONFIDENCE
                        # =============================

                        confidence = float(
                            box.conf[0].item()
                        )

                        # =============================
                        # BOUNDING BOX
                        # =============================

                        coords = (
                            box.xyxy[0]
                            .cpu()
                            .numpy()
                            .astype(int)
                        )

                        x1, y1, x2, y2 = coords

                        # =============================
                        # INVALID CHECK
                        # =============================

                        if x2 <= x1:
                            continue

                        if y2 <= y1:
                            continue

                        # =============================
                        # DETECTION OBJECT
                        # =============================

                        detections.append({

                            "type": label,

                            "confidence": confidence,

                            "box": (
                                int(x1),
                                int(y1),
                                int(x2),
                                int(y2)
                            )

                        })

                    except Exception as e:

                        print(
                            f"[BOX ERROR] {e}"
                        )

        except Exception as e:

            print(
                f"[OBJECT DETECTOR ERROR] {e}"
            )

        return detections