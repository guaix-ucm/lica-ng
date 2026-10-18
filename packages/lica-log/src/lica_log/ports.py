# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# -----------------
# Standard library
# ----------------
from typing import Protocol


class Logger(Protocol):
    def configure(self) -> None: ...
