class ObjectTracker:

    def __init__(self, settings):

        self.settings = settings

        self.next_id = 0

    def update(
        self,
        detections,
        frame
    ):

        tracked_objects = []

        if detections is None:
            return tracked_objects

        for det in detections:

            box = det.get("box")

            if box is None:
                continue

            tracked_objects.append({

                "id": self.next_id,

                "type": det.get(
                    "type",
                    "object"
                ),

                "confidence": det.get(
                    "confidence",
                    0.0
                ),

                "box": box

            })

            self.next_id += 1

        return tracked_objects