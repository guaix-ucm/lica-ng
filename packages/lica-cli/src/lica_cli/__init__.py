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
    __version__ = version("lica-cli")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"


from .common import parse_args
from .startup import run_cli

__all__ = ["parse_args", "run_cli"]
