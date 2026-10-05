"""
Central logging setup.

Save as:  backend/app/logging_config.py

Then, at the very top of app/main.py (before the FastAPI app is created):

    from app.logging_config import setup_logging
    setup_logging()
"""

from __future__ import annotations

import logging
from pathlib import Path

_LOG_DIR = Path(__file__).resolve().parents[1] / "storage"
_LOG_FILE = _LOG_DIR / "discovery.log"

_FORMAT = "%(asctime)s %(levelname)-7s [%(name)s] %(message)s"


def setup_logging(level: int = logging.INFO, to_file: bool = True) -> None:
    """Configure logging for the discovery and AI-provider loggers."""

    formatter = logging.Formatter(_FORMAT)

    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if to_file:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(_LOG_FILE, encoding="utf-8"))

    for name in ("ai_discovery", "ai_provider", "app"):
        logger = logging.getLogger(name)

        # Avoid duplicate handlers when uvicorn --reload re-imports the app.
        if logger.handlers:
            continue

        logger.setLevel(level)
        logger.propagate = False

        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)