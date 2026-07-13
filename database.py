"""
database/database.py
──────────────────────────────────────────────────────────────────────────────
This project is configured to use FILE LOGS instead of a database.
All event records are written to  outputs/events.jsonl  by EventRecorder.

This module is kept as a stub so the import path exists if a database is
added later (e.g. SQLite, PostgreSQL, MongoDB).

To enable a database backend, replace the stub below with a real
implementation and update EventRecorder to call db.insert_event().
──────────────────────────────────────────────────────────────────────────────
"""

from utils.logger import get_logger

logger = get_logger("Database")


class Database:
    """No-op stub. All persistence is handled via file logs."""

    def __init__(self, settings=None):
        logger.info("Database: file-log mode active (no DB connection).")

    def insert_event(self, event: dict):
        """Not used — EventRecorder writes to events.jsonl directly."""
        pass

    def close(self):
        pass
