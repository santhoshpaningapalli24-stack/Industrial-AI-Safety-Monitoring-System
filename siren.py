"""
alerts/siren.py
Plays an audio siren when a high-threat event is detected.

Priority order:
  1. Custom sound file (settings.SIREN_SOUND_FILE)     → pygame
  2. System beep via winsound (Windows) or os bell (*nix)

pygame is optional; install with:  pip install pygame
"""

import os
import sys
import time
import threading
from utils.logger import get_logger

logger = get_logger("Siren")

try:
    import pygame
    _PYGAME_AVAILABLE = True
except ImportError:
    _PYGAME_AVAILABLE = False


class Siren:
    def __init__(self, settings):
        self.sound_file   = settings.SIREN_SOUND_FILE
        self.duration_sec = settings.SIREN_DURATION_SEC
        self.repeat       = settings.SIREN_REPEAT
        self._lock        = threading.Lock()

    def send(self, event: dict):
        """Called from a daemon thread — plays siren non-blocking."""
        with self._lock:
            level = event["threat_level"]["level"]
            logger.info(f"Siren triggered (level={level})")
            self._play()

    # ── private ────────────────────────────────────────────────────────────────

    def _play(self):
        if self.sound_file and os.path.isfile(self.sound_file) and _PYGAME_AVAILABLE:
            self._play_file()
        else:
            self._system_beep()

    def _play_file(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_file)
            for _ in range(self.repeat):
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            pygame.mixer.quit()
        except Exception as exc:
            logger.error(f"Siren playback error: {exc}")
            self._system_beep()

    def _system_beep(self):
        """Cross-platform fallback beep."""
        for _ in range(self.repeat):
            if sys.platform == "win32":
                try:
                    import winsound
                    winsound.Beep(1000, int(self.duration_sec * 1000))
                except Exception:
                    print("\a", end="", flush=True)
            else:
                # Terminal bell
                print("\a", end="", flush=True)
                time.sleep(self.duration_sec)
