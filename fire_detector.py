from ultralytics import YOLO


class FireDetector:

    def __init__(self, settings):

        self.settings = settings

        self.model = YOLO(
            "weights/fire_smoke.pt"
        )

        self.class_names = {

            0: "fire",

            1: "smoke"

        }

        print(
            "[INFO] Fire/Smoke AI loaded"
        )

    # =========================================
    # DETECT
    # =========================================

    def detect(self, frame):

        detections = []

        try:

            results = self.model(

                frame,

                imgsz=640,

                conf=0.4,

                verbose=False

            )

            for r in results:

                if r.boxes is None:
                    continue

                for box in r.boxes:

                    cls_id = int(
                        box.cls[0]
                    )

                    confidence = float(
                        box.conf[0]
                    )

                    x1, y1, x2, y2 = map(

                        int,

                        box.xyxy[0]
                    )

                    detections.append({

                        "type":
                            self.class_names[
                                cls_id
                            ],

                        "confidence":
                            confidence,

                        "box":
                            (
                                x1,
                                y1,
                                x2,
                                y2
                            )

                    })

        except Exception as e:

            print(
                f"[ERROR] {e}"
            )

        return detections