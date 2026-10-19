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
    __version__ = version("lica-raw")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

from .errors import (
    MissingImageError,
    MissingMandatoryFitsError,
    OutOfBoundsError,
    ReadMetadataError,
    UnknownDateTimeFormatError,
    UnsupportedCFAError,
)
from .models import ImageMetadata
from .ports import ImageReader, ImageReaderFactory
from .types import BayerIndex, BayerPattern, HeaderType, ImageType, IntArray2D
from .rect import Rect, Point

__all__ = [
    "Rect",
    "Point",
    "ImageReader",
    "ImageMetadata",
    "ImageReaderFactory",
    "BayerPattern",
    "BayerIndex",
    "HeaderType",
    "ImageType",
    "IntArray2D",
    "UnsupportedCFAError",
    "ReadMetadataError",
    "UnknownDateTimeFormatError",
    "MissingImageError",
    "MissingMandatoryFitsError",
    "OutOfBoundsError",
]
