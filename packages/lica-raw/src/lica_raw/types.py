# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
from enum import IntEnum, StrEnum

# ---------------------
# Third party libraries
# ---------------------
import numpy as np

# type alias
type IntArray2D = np.ndarray[tuple[int, int], np.dtype[np.uint16]]

# -----------------
# Enumeration types
# -----------------

class HeaderType(StrEnum):
    FITS = "FITS"
    EXIF = "EXIF"


class BayerPattern(StrEnum):
    RGGB = "RGGB"
    BGGR = "BGGR"
    GRBG = "GRBG"
    GBRG = "GBRG"


class ImageType(StrEnum):
    BIAS = "BIAS"
    DARK = "DARK"
    FLAT = "FLAT"
    LIGHT = "LIGHT"


class BayerIndex(IntEnum):
    """Indexes to bidimensional 2x2 RGB Bayer pattern, black_level_per_channel and white_levels_per_channel"""

    R = 0
    Gr = 1
    B = 2
    Gb = 3
