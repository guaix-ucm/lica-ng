# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import os

# ----------------
# Own dependencies
# ----------------
from ..errors import UnsupportedImageFormatError
from ..ports import ImageReader, ImageReaderFactory

FITS_EXTENSIONS = (".fit", ".fits", ".fts")

RAW_EXTENSIONS = (".nef", ".cr2", ".cr3", ".arw", ".raf", ".orf", ".dng", ".rw2")


class ImageReaderFactoryImpl(ImageReaderFactory):
    def get_reader(self, path: str) -> ImageReader:
        ext = os.path.splitext(path)[1].lower()
        if ext in FITS_EXTENSIONS:
            try:
                from .fits import FitsReader
            except ModuleNotFoundError:
                raise UnsupportedImageFormatError("consider adding lica-raw[fits] support")
            return FitsReader()
        if ext in RAW_EXTENSIONS:
            try:
                from .exif import ExifReader
            except ModuleNotFoundError:
                raise UnsupportedImageFormatError("consider adding lica-raw[exif] support")
            return ExifReader()
        raise UnsupportedImageFormatError(path)
