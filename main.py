"""
Industrial AI Safety Monitoring System
Advanced Main Pipeline
"""

import cv2
import time
import threading

from config.settings import Settings

from detectors.fire_detector import FireDetector
from detectors.object_detector import ObjectDetector
from detectors.scene_detector import SceneDetector
from detectors.threat_analyzer import ThreatAnalyzer

from tracking.tracker import ObjectTracker

from alerts.telegram_alert import TelegramAlert
from alerts.email_alert import EmailAlert
from alerts.siren import Siren

from recording.event_recorder import EventRecorder

from ui.hud import HUD

from utils.fps import FPSCounter
from utils.logger import get_logger


logger = get_logger("main")


# =========================================================
# ALERT MANAGER
# =========================================================

def build_alert_manager(settings):

    alerts = []

    if settings.TELEGRAM_ENABLED:

        alerts.append(
            TelegramAlert(settings)
        )

    if settings.EMAIL_ENABLED:

        alerts.append(
            EmailAlert(settings)
        )

    if settings.SIREN_ENABLED:

        alerts.append(
            Siren(settings)
        )

    return alerts


def dispatch_alerts(alert_channels, event):

    for channel in alert_channels:

        t = threading.Thread(

            target=channel.send,

            args=(event,),

            daemon=True

        )

        t.start()


# =========================================================
# MAIN
# =========================================================

def main():

    settings = Settings()

    logger.info(
        "Starting Industrial AI Safety Monitor"
    )

    logger.info(
        f"Camera source: {settings.CAMERA_SOURCE}"
    )

    # =====================================================
    # LOAD DETECTORS
    # =====================================================

    fire_detector = FireDetector(settings)

    object_detector = ObjectDetector(settings)

    scene_detector = SceneDetector(settings)

    threat_analyzer = ThreatAnalyzer(settings)

    tracker = ObjectTracker(settings)

    recorder = EventRecorder(settings)

    hud = HUD(settings)

    fps_counter = FPSCounter()

    alert_channels = build_alert_manager(settings)

    # =====================================================
    # CAMERA
    # =====================================================

    cap = cv2.VideoCapture(
        settings.CAMERA_SOURCE
    )

    if not cap.isOpened():

        logger.error(
            f"Cannot open camera source: "
            f"{settings.CAMERA_SOURCE}"
        )

        return

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        settings.FRAME_WIDTH
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        settings.FRAME_HEIGHT
    )

    logger.info(
        "Camera opened. Press 'q' to quit."
    )

    last_alert_time = {}

    # =====================================================
    # MAIN LOOP
    # =====================================================

    while True:

        try:

            ret, frame = cap.read()

            if not ret:

                logger.warning(
                    "Frame capture failed."
                )

                time.sleep(0.1)

                continue

            # =================================================
            # FPS
            # =================================================

            fps = fps_counter.update()

            # =================================================
            # FIRE + SMOKE DETECTION
            # =================================================

            all_results = fire_detector.detect(
                frame
            )

            # FIRE
            fire_results = [

                detection

                for detection in all_results

                if detection["type"] == "fire"

            ]

            # SMOKE
            smoke_results = [

                detection

                for detection in all_results

                if detection["type"] == "smoke"

            ]

            # =================================================
            # OBJECT DETECTION
            # =================================================

            object_results = object_detector.detect(
                frame
            )

            # =================================================
            # SCENE ANALYSIS
            # =================================================

            scene_info = scene_detector.analyze(
                frame
            )

            # =================================================
            # COMBINE DETECTIONS
            # =================================================

            all_detections = (

                fire_results +

                smoke_results +

                object_results

            )

            # =================================================
            # TRACKING
            # =================================================

            tracked_objects = tracker.update(

                all_detections,

                frame

            )

            # =================================================
            # THREAT ANALYSIS
            # =================================================

            threat_level = threat_analyzer.evaluate(

                fire_results,

                smoke_results,

                scene_info

            )

            # =================================================
            # ALERTS
            # =================================================

            now = time.time()

            if threat_level["level"] in (

                "HIGH",

                "CRITICAL"

            ):

                key = threat_level["level"]

                cooldown = (
                    settings.ALERT_COOLDOWN_SECONDS
                )

                if (

                    now -

                    last_alert_time.get(key, 0)

                    >= cooldown

                ):

                    last_alert_time[key] = now

                    snapshot_path = (

                        recorder.save_snapshot(

                            frame,

                            threat_level

                        )

                    )

                    event = {

                        "threat_level":
                            threat_level,

                        "fire":
                            fire_results,

                        "smoke":
                            smoke_results,

                        "objects":
                            object_results,

                        "scene":
                            scene_info,

                        "snapshot":
                            snapshot_path,

                        "timestamp":
                            now,
                    }

                    recorder.log_event(
                        event
                    )

                    dispatch_alerts(

                        alert_channels,

                        event

                    )

                    logger.warning(
                        f"[ALERT] "
                        f"{threat_level['level']}"
                    )

            # =================================================
            # RECORDING
            # =================================================

            if threat_level["level"] in (

                "HIGH",

                "CRITICAL"

            ):

                recorder.write_frame(frame)

            else:

                recorder.stop_clip()

            # =================================================
            # HUD
            # =================================================

            display_frame = hud.draw(

                frame.copy(),

                fire_results=fire_results,

                smoke_results=smoke_results,

                tracked_objects=tracked_objects,

                threat_level=threat_level,

                scene_info=scene_info,

                fps=fps,

            )

            # =================================================
            # DISPLAY
            # =================================================

            cv2.imshow(

                "Industrial AI Safety Monitor",

                display_frame

            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                logger.info(
                    "Quit signal received."
                )

                break

        except Exception as e:

            logger.error(
                f"MAIN LOOP ERROR: {e}"
            )

            continue

    # =====================================================
    # CLEANUP
    # =====================================================

    recorder.force_stop_clip()

    cap.release()

    cv2.destroyAllWindows()

    logger.info(
        "System shut down cleanly."
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()