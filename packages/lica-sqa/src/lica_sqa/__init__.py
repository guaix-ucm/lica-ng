# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# standard library
# ----------------
import logging
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lica-sqa")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"


from .ports import Database
from .metadata import Model, metadata
from .view import view

def sqa_logging(debug: bool) -> None:
    if debug:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
        # This is needed, otherwise aiosqlite msgs will jump in
        logging.getLogger("aiosqlite").setLevel(logging.INFO)
    else:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

__all__ = ["sqa_logging","Database", "Model", "metadata", "view"]
