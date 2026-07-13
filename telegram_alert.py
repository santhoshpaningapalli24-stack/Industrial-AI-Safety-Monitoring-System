"""
alerts/telegram_alert.py
Sends a photo + caption to a Telegram bot when a threat is detected.
Requires: pip install requests
"""

import os
import requests
from utils.logger import get_logger

logger = get_logger("TelegramAlert")


class TelegramAlert:
    def __init__(self, settings):
        self.token   = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self._base   = f"https://api.telegram.org/bot{self.token}"

    def send(self, event: dict):
        if not self.token or self.token == "YOUR_BOT_TOKEN_HERE":
            logger.warning("Telegram token not configured — skipping alert.")
            return

        level     = event["threat_level"]["level"]
        reason    = event["threat_level"]["reason"]
        fires     = event["threat_level"]["fire_count"]
        smokes    = event["threat_level"]["smoke_count"]
        ts        = event.get("timestamp", 0)
        snapshot  = event.get("snapshot", "")

        caption = (
            f"🔥 *INDUSTRIAL SAFETY ALERT*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️  Threat Level: *{level}*\n"
            f"🔥  Fires detected: {fires}\n"
            f"💨  Smoke detected: {smokes}\n"
            f"📋  Reason: {reason}\n"
            f"🕒  Time: {self._fmt_time(ts)}"
        )

        try:
            if snapshot and os.path.isfile(snapshot):
                self._send_photo(snapshot, caption)
            else:
                self._send_message(caption)
            logger.info(f"Telegram alert sent (level={level})")
        except Exception as exc:
            logger.error(f"Telegram alert failed: {exc}")

    # ── helpers ────────────────────────────────────────────────────────────────

    def _send_message(self, text: str):
        url = f"{self._base}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()

    def _send_photo(self, path: str, caption: str):
        url = f"{self._base}/sendPhoto"
        with open(path, "rb") as f:
            resp = requests.post(
                url,
                data={"chat_id": self.chat_id, "caption": caption, "parse_mode": "Markdown"},
                files={"photo": f},
                timeout=15,
            )
        resp.raise_for_status()

    @staticmethod
    def _fmt_time(ts: float) -> str:
        import datetime
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
