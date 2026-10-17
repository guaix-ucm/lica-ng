# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------
# -----------------
# Standard library
# ----------------
import logging
from enum import StrEnum


class LogLevel(StrEnum):
    NOTSET = "notset"
    CRITICAL = "critical"
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"


__MAP__ = {
    LogLevel.NOTSET: logging.NOTSET,
    LogLevel.CRITICAL: logging.CRITICAL,
    LogLevel.ERROR: logging.ERROR,
    LogLevel.WARN: logging.WARN,
    LogLevel.INFO: logging.INFO,
    LogLevel.DEBUG: logging.DEBUG,
}

def to_std_logging(level: LogLevel) -> int:
    return __MAP__[level]
