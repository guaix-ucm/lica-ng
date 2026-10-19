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
    __version__ = version("lica-tables")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"


from .ports import TabularData, DisplayService

__all__ = ["TabularData", "DisplayService"]
