"""
Day 5 - Production: Structured logging configuration.

Import and call setup_logging() once at app startup.
Reads LOG_LEVEL from the environment (default: INFO).
"""

import logging
import os
import sys


def setup_logging() -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)

    if not root.handlers:
        root.addHandler(handler)

    return logging.getLogger("career_copilot")
