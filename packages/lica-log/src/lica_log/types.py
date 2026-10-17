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
from enum import IntEnum

class LogLevel(IntEnum):
    NOTSET = logging.NOTSET
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARN = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
