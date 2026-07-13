import cv2
import time
from pathlib import Path


class EventRecorder:

    def __init__(self, settings):

        self.settings = settings

        # =========================================
        # OUTPUT DIRECTORY
        # =========================================

        self.out_dir = Path(
            settings.OUTPUT_DIR
        )

        self.out_dir.mkdir(
            exist_ok=True
        )

        # =========================================
        # VIDEO SETTINGS
        # =========================================

        self.codec = cv2.VideoWriter_fourcc(
            *settings.VIDEO_CODEC
        )

        self.fps = settings.VIDEO_FPS

        self.writer = None

        self.recording = False

        self.last_write_time = 0

        self.clip_start_time = None

    # =========================================
    # START RECORDING
    # =========================================

    def start_clip(self, frame):

        timestamp = time.strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            self.out_dir /
            f"clip_{timestamp}.mp4"
        )

        h, w = frame.shape[:2]

        self.writer = cv2.VideoWriter(

            str(filename),

            self.codec,

            self.fps,

            (w, h)

        )

        self.recording = True

        self.clip_start_time = time.time()

        print(
            f"[INFO] Started recording: {filename}"
        )

    # =========================================
    # WRITE FRAME
    # =========================================

    def write_frame(self, frame):

        if not self.recording:

            self.start_clip(frame)

        if self.writer is not None:

            self.writer.write(frame)

            self.last_write_time = time.time()

    # =========================================
    # STOP RECORDING
    # =========================================

    def stop_clip(self):

        if not self.recording:
            return

        elapsed = (
            time.time() -
            self.last_write_time
        )

        if elapsed < self.settings.CLIP_DURATION_SECONDS:
            return

        if self.writer is not None:

            self.writer.release()

            self.writer = None

        self.recording = False

        print(
            "[INFO] Recording stopped"
        )

    # =========================================
    # FORCE STOP
    # =========================================

    def force_stop_clip(self):

        if self.writer is not None:

            self.writer.release()

            self.writer = None

        self.recording = False

    # =========================================
    # SAVE SNAPSHOT
    # =========================================

    def save_snapshot(self, frame, threat_level):

        timestamp = time.strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            self.out_dir /
            f"snapshot_{timestamp}.{self.settings.SNAPSHOT_FORMAT}"
        )

        cv2.imwrite(
            str(filename),
            frame
        )

        print(
            f"[INFO] Snapshot saved: {filename}"
        )

        return str(filename)

    # =========================================
    # LOG EVENT
    # =========================================

    def log_event(self, event):

        print(
            "[EVENT]",
            event
        )