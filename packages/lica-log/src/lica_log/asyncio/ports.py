# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------
# -----------------
# Standard library
# ----------------
from logging.handlers import QueueListener
from typing import Protocol


class AsyncLogger(Protocol):
    def configure(self) -> QueueListener: ...
