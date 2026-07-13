"""
alerts/email_alert.py
Sends an HTML email with an embedded snapshot via SMTP (TLS).
Requires: standard library only (smtplib, email).
"""

import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from utils.logger import get_logger

logger = get_logger("EmailAlert")

_LEVEL_COLOR = {
    "LOW":      "#f0ad4e",
    "MODERATE": "#fd7e14",
    "HIGH":     "#dc3545",
    "CRITICAL": "#6f0000",
}


class EmailAlert:
    def __init__(self, settings):
        self.smtp_host   = settings.EMAIL_SMTP_HOST
        self.smtp_port   = settings.EMAIL_SMTP_PORT
        self.sender      = settings.EMAIL_SENDER
        self.password    = settings.EMAIL_PASSWORD
        self.recipients  = settings.EMAIL_RECIPIENTS

    def send(self, event: dict):
        if not self.password or self.password == "your_app_password":
            logger.warning("Email credentials not configured — skipping alert.")
            return

        level     = event["threat_level"]["level"]
        reason    = event["threat_level"]["reason"]
        fires     = event["threat_level"]["fire_count"]
        smokes    = event["threat_level"]["smoke_count"]
        ts        = event.get("timestamp", 0)
        snapshot  = event.get("snapshot", "")
        color     = _LEVEL_COLOR.get(level, "#333333")

        subject = f"[{level}] Industrial Safety Alert — Fire/Smoke Detected"
        html    = self._build_html(level, reason, fires, smokes, ts, color)

        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["From"]    = self.sender
        msg["To"]      = ", ".join(self.recipients)

        msg.attach(MIMEText(html, "html"))

        if snapshot and os.path.isfile(snapshot):
            with open(snapshot, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", "<snapshot>")
                img.add_header("Content-Disposition", "inline", filename=os.path.basename(snapshot))
                msg.attach(img)

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.recipients, msg.as_string())
            logger.info(f"Email alert sent to {self.recipients} (level={level})")
        except Exception as exc:
            logger.error(f"Email alert failed: {exc}")

    # ── helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _build_html(level, reason, fires, smokes, ts, color) -> str:
        time_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        return f"""
        <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
          <div style="max-width:600px;margin:auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.15);">
            <div style="background:{color};padding:24px;text-align:center;">
              <h1 style="color:#fff;margin:0;font-size:28px;">🔥 SAFETY ALERT</h1>
              <p style="color:#fff;margin:8px 0 0;font-size:18px;">Threat Level: <strong>{level}</strong></p>
            </div>
            <div style="padding:24px;">
              <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:8px;color:#555;font-weight:bold;">Fires Detected</td><td style="padding:8px;">{fires}</td></tr>
                <tr style="background:#f9f9f9;"><td style="padding:8px;color:#555;font-weight:bold;">Smoke Detected</td><td style="padding:8px;">{smokes}</td></tr>
                <tr><td style="padding:8px;color:#555;font-weight:bold;">Reason</td><td style="padding:8px;">{reason}</td></tr>
                <tr style="background:#f9f9f9;"><td style="padding:8px;color:#555;font-weight:bold;">Time</td><td style="padding:8px;">{time_str}</td></tr>
              </table>
              <br/>
              <img src="cid:snapshot" style="width:100%;border-radius:4px;" alt="Event snapshot"/>
            </div>
            <div style="background:#eee;padding:12px;text-align:center;font-size:12px;color:#999;">
              Industrial AI Safety Monitoring System — Automated Alert
            </div>
          </div>
        </body></html>
        """
