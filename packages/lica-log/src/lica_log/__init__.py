# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# standard library
# ----------------
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lica-log")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"


from .common import to_std_logging
from .ports import Logger
from .types import LogLevel

__all__ = ["LogLevel", "Logger", "to_std_logging"]
