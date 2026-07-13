"""
Advanced HUD Renderer
Industrial AI Safety Monitoring System
"""

import cv2
import time


class HUD:

    def __init__(self, settings):

        self.settings = settings

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.last_blink = time.time()

        self.blink_state = True

    # =====================================================
    # COLORS
    # =====================================================

    RED     = (0, 0, 255)
    GREEN   = (0, 255, 0)
    BLUE    = (255, 0, 0)
    YELLOW  = (0, 255, 255)
    ORANGE  = (0, 165, 255)
    WHITE   = (255, 255, 255)
    CYAN    = (255, 255, 0)
    BLACK   = (0, 0, 0)
    GRAY    = (40, 40, 40)

    # =====================================================
    # MAIN DRAW
    # =====================================================

    def draw(
        self,
        frame,
        fire_results,
        smoke_results,
        tracked_objects,
        threat_level,
        scene_info,
        fps,
    ):

        # SAFE CHECKS

        if fire_results is None:
            fire_results = []

        if smoke_results is None:
            smoke_results = []

        if tracked_objects is None:
            tracked_objects = []

        # =================================================
        # DRAW OBJECTS
        # =================================================

        for obj in tracked_objects:

            try:

                x1, y1, x2, y2 = map(
                    int,
                    obj.get(
                        "box",
                        (0, 0, 0, 0)
                    )
                )

                label = obj.get(
                    "type",
                    "object"
                )

                obj_id = obj.get(
                    "id",
                    0
                )

                confidence = obj.get(
                    "confidence",
                    0.0
                )

                # COLOR LOGIC

                if label == "fire":
                    color = self.RED

                elif label == "smoke":
                    color = self.ORANGE

                elif label == "person":
                    color = self.GREEN

                else:
                    color = self.CYAN

                text = (
                    f"{label.upper()} "
                    f"ID:{obj_id} "
                    f"{confidence:.2f}"
                )

                self.draw_box(
                    frame,
                    (x1, y1, x2, y2),
                    text,
                    color
                )

            except Exception as e:

                print(
                    f"[HUD OBJECT ERROR] {e}"
                )

        # =================================================
        # TOP BAR
        # =================================================

        self.draw_top_bar(
            frame,
            fps,
            threat_level
        )

        # =================================================
        # SIDE PANEL
        # =================================================

        self.draw_side_panel(
            frame,
            fire_results,
            smoke_results,
            tracked_objects,
            threat_level
        )

        # =================================================
        # ALERT BANNER
        # =================================================

        self.draw_alert_banner(
            frame,
            threat_level
        )

        return frame

    # =====================================================
    # DRAW BOX
    # =====================================================

    def draw_box(
        self,
        frame,
        box,
        label,
        color
    ):

        try:

            x1, y1, x2, y2 = map(
                int,
                box
            )

            # INVALID CHECK

            if x2 <= x1 or y2 <= y1:
                return

            # MAIN BOX

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # LABEL BG

            cv2.rectangle(
                frame,
                (x1, max(0, y1 - 30)),
                (x1 + 260, y1),
                color,
                -1
            )

            # LABEL TEXT

            cv2.putText(
                frame,
                str(label),
                (x1 + 5, max(20, y1 - 8)),
                self.font,
                0.5,
                self.BLACK,
                2
            )

        except Exception as e:

            print(
                f"[DRAW BOX ERROR] {e}"
            )

    # =====================================================
    # TOP BAR
    # =====================================================

    def draw_top_bar(
        self,
        frame,
        fps,
        threat_level
    ):

        h, w = frame.shape[:2]

        cv2.rectangle(
            frame,
            (0, 0),
            (w, 45),
            self.BLACK,
            -1
        )

        # TITLE

        cv2.putText(
            frame,
            "INDUSTRIAL AI SAFETY MONITOR",
            (20, 30),
            self.font,
            0.8,
            self.CYAN,
            2
        )

        # FPS

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (500, 30),
            self.font,
            0.7,
            self.GREEN,
            2
        )

        # THREAT

        level = threat_level.get(
            "level",
            "NONE"
        )

        score = threat_level.get(
            "score",
            0.0
        )

        color = self.get_threat_color(level)

        cv2.putText(
            frame,
            f"THREAT: {level} "
            f"({score:.2f})",
            (700, 30),
            self.font,
            0.7,
            color,
            2
        )

    # =====================================================
    # SIDE PANEL
    # =====================================================

    def draw_side_panel(
        self,
        frame,
        fire_results,
        smoke_results,
        tracked_objects,
        threat_level
    ):

        h, w = frame.shape[:2]

        panel_width = 320

        x = w - panel_width

        cv2.rectangle(
            frame,
            (x, 45),
            (w, h),
            (25, 25, 25),
            -1
        )

        # TITLE

        cv2.putText(
            frame,
            "SYSTEM STATUS",
            (x + 20, 80),
            self.font,
            0.8,
            self.CYAN,
            2
        )

        # INFO

        info_lines = [

            f"Fire Detections : {len(fire_results)}",

            f"Smoke Detections: {len(smoke_results)}",

            f"Tracked Objects : {len(tracked_objects)}",

            f"Threat Level   : "
            f"{threat_level.get('level','NONE')}",

            f"Threat Score   : "
            f"{threat_level.get('score',0):.2f}"

        ]

        y = 130

        for line in info_lines:

            cv2.putText(
                frame,
                line,
                (x + 20, y),
                self.font,
                0.6,
                self.WHITE,
                2
            )

            y += 40

    # =====================================================
    # ALERT BANNER
    # =====================================================

    def draw_alert_banner(
        self,
        frame,
        threat_level
    ):

        level = threat_level.get(
            "level",
            "NONE"
        )

        if level == "NONE":
            return

        h, w = frame.shape[:2]

        # BLINK EFFECT

        if time.time() - self.last_blink > 0.5:

            self.blink_state = (
                not self.blink_state
            )

            self.last_blink = time.time()

        if not self.blink_state:
            return

        color = self.get_threat_color(level)

        cv2.rectangle(
            frame,
            (0, h - 70),
            (w, h),
            color,
            -1
        )

        text = (
            f"WARNING: "
            f"{level} THREAT DETECTED"
        )

        cv2.putText(
            frame,
            text,
            (30, h - 25),
            self.font,
            1.0,
            self.BLACK,
            3
        )

    # =====================================================
    # THREAT COLORS
    # =====================================================

    def get_threat_color(
        self,
        level
    ):

        if level == "CRITICAL":
            return self.RED

        elif level == "HIGH":
            return self.ORANGE

        elif level == "MEDIUM":
            return self.YELLOW

        elif level == "LOW":
            return self.GREEN

        return self.WHITE