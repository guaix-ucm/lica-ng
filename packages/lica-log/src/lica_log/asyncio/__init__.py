# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------
# -----------------
# Standard library
# ----------------
from typing import Protocol
from logging.handlers import QueueListener

# ----------------
# Own dependencies
# ----------------
from ..common import LogLevel

class AsyncLogger(Protocol):
    def configure(self) -> QueueListener: ...


__all__ = ["LogLevel", "AsyncLogger"]
