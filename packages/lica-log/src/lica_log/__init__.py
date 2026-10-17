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
from argparse import Namespace

# ----------------
# Own dependencies
# ----------------
from .common import LogLevel, to_std_logging

class Logger(Protocol):
    def additional_args(self, args: Namespace) -> None: ...
    def configure(self) -> None: ...


__all__ = ["LogLevel", "Logger", "to_std_logging"]
