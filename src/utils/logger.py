"""Logging configuration for the scraper package."""

import logging
import os
from datetime import datetime
from typing import Optional


def setup_logger(name: str = "scraper", log_file: Optional[str] = None) -> logging.Logger:
    """Create a logger configured for console and file output."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if log_file is None:
            log_file = os.path.join("logs", "scraper.log")

        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_timestamp() -> str:
    """Return a simple timestamp string for log-friendly messages."""
    return datetime.utcnow().isoformat()
