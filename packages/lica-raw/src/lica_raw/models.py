# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
from dataclasses import dataclass
from datetime import datetime

# ----------------
# Own dependencies
# ----------------
from .types import BayerPattern, ImageType, HeaderType


@dataclass
class ImageMetadata:
    width: int
    height: int
    make: str | None
    model: str | None
    exptime: float | None
    iso: int | None
    gain: float | None
    black_level: int | None
    bayer: BayerPattern
    imagetyp: ImageType | None
    timestamp: datetime | None
    focal_len: float | None
    f_number: float | None
    header_type: HeaderType
    extension: str

    def __str__(self) -> str:
        return f"{self.model} {self.width}x{self.height}"
