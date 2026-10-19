# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# ----------------
# Own dependencies
# ----------------


class RawBaseError(Exception):
    """Raw library base error"""


class UnsupportedImageFormatError(RawBaseError):
    """Unsupported image format"""


class AlreadyClosedError(RawBaseError):
    """Resource already closed"""


class UnsupportedCFAError(RawBaseError):
    """Unsupported Color Filter Array"""


class ReadMetadataError(RawBaseError):
    """Could not read image metadata"""


class UnknownDateTimeFormatError(RawBaseError):
    """unknown observation date format string"""


class OutOfBoundsError(RawBaseError):
    """out of bounds rectangle"""


class MissingImageError(RawBaseError):
    """Image path does not exists"""


class MissingMandatoryFitsError(RawBaseError):
    """Missing mandatory keywords in FITS image"""
