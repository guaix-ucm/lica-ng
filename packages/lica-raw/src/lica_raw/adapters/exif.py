# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import logging
import os
from datetime import datetime, timezone
from fractions import Fraction
from typing import Any, Mapping
from types import TracebackType

# ---------------------
# Third party libraries
# ---------------------
import exifread
import numpy as np
import rawpy
from rawpy._rawpy import RawPy

# ----------------
# Own dependencies
# ----------------
from ..rect import Point, Rect
from ..types import IntArray2D, BayerIndex, BayerPattern, HeaderType

from ..errors import (
    MissingImageError,
    OutOfBoundsError,
    ReadMetadataError,
    UnknownDateTimeFormatError,
    UnsupportedCFAError,
    AlreadyClosedError,
)
from ..models import ImageMetadata
from ..ports import ImageReader, RawPixels
from ..utils import image_type_by_path

# get the root logger
log = logging.getLogger(__name__.split(".")[-1])


def to_positive_float(value: Any | None) -> float | None:
    if value in (0, "0", None):
        return None
    try:
        result = round(float(Fraction(str(value))), 2)
    except (ValueError, ZeroDivisionError, TypeError):
        return None
    return result if result > 0 else None


def handle_date_obs(exif: Mapping[str, Any], path: str) -> datetime | None:
    date_obs = None
    for key in ("Image DateTime", "EXIF DateTimeOriginal"):
        date_obs = exif.get(key)
        if date_obs:
            date_obs = str(date_obs)
            break
    if date_obs is None:
        return None
    new_date_obs = None
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            new_date_obs = datetime.strptime(date_obs, fmt)
        except Exception:
            pass
        else:
            break
    if new_date_obs is None:
        raise UnknownDateTimeFormatError(date_obs)
    return new_date_obs.replace(tzinfo=timezone.utc)


class ExifReader(ImageReader):
    def header_type(self) -> HeaderType:
        return HeaderType.EXIF

    def read_metadata(self, path: str) -> ImageMetadata:
        with open(path, "rb") as fd:
            exif = exifread.process_file(fd, details=True)
        if not exif:
            raise ReadMetadataError(os.path.basename(path))
        make = exif.get("Image Make")
        make = str(make).strip() if make is not None else None
        model = exif.get("Image Model")
        model = str(model).strip() if model is not None else None
        focal_len = to_positive_float(exif.get("EXIF FocalLength"))
        f_number = to_positive_float(exif.get("EXIF FNumber"))
        iso = exif.get("EXIF ISOSpeedRatings")
        iso = int(float(str(iso))) if iso is not None else None
        exptime = exif.get("EXIF ExposureTime")
        exptime = float(Fraction(str(exptime))) if exptime is not None else None
        timestamp = handle_date_obs(exif, path)
        image_type = image_type_by_path(path)
        with rawpy.imread(path) as img:
            raw_height, raw_width = img.raw_image.shape
            black_levels = img.black_level_per_channel
            black_level = int(round(sum(black_levels) / len(black_levels), 0))  # mean black level
            color_desc = img.color_desc.decode("utf-8")
            if color_desc != "RGBG":
                raise UnsupportedCFAError(color_desc)
            cfa = "".join(
                map(
                    lambda c: {"Gr": "G", "Gb": "G"}.get(c, c),
                    [BayerIndex(i).name for i in img.raw_pattern.ravel()],
                )
            )
            bayer = BayerPattern(cfa)
            header_type = self.header_type()
            extension = os.path.splitext(path)[1]

        metadata = ImageMetadata(
            raw_width=raw_width,
            raw_height=raw_height,
            make=make,
            model=model,
            exptime=exptime,
            iso=iso,
            gain=None,
            black_level=black_level,
            bayer=bayer,
            imagetyp=image_type,
            timestamp=timestamp,
            focal_len=focal_len,
            f_number=f_number,
            header_type=header_type,
            extension=extension,
        )
        return metadata

    def read_pixels(self, path: str) -> RawPixels:
        """returns an object that implements the RawPixels interface"""
        if not os.path.isfile(path):
            raise MissingImageError(path)
        raw = rawpy.imread(path)
        return ExifRawPixels(raw, path)


class ExifRawPixels(RawPixels):
    def __init__(self, raw: RawPy, path: str) -> None:
        self.path = path
        self.img = raw
        self.black_levels = raw.black_level_per_channel
        self.shape = raw.raw_image.shape
        self.pattern = raw.raw_pattern

    def close(self) -> None:
        if self.img is not None:
            self.img.close()
            self.img = None

    # No context managers here, we need to keep the internal numpy
    # raw_pixels array alive while statistics are being computed
    def __del__(self) -> None:
        try:
            if self.img is not None:
                self.img.close()
        finally:
            self.img = None

    def __enter__(self) -> "ExifRawPixels":
            if self.img is None:
                raise AlreadyClosedError(os.path.basename(self.path))
            return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
        ) -> None:
            self.close()

    def _section(
        self,
        x: int,
        y: int,
        section: Rect | None,
    ) -> IntArray2D:
        screen = Rect.from_points(Point.zero(), Point(x=self.shape[1], y=self.shape[0])) // 2
        if section is None:
            section = screen
        elif not screen.contains(section):
            raise OutOfBoundsError(section)
        section = section * 2
        x1 = x + section.x1
        y1 = y + section.y1
        x2 = section.x2
        y2 = section.y2
        return self.img.raw_image[y1:y2:2, x1:x2:2]

    def red(self, section: Rect | None) -> IntArray2D:
        y, x = np.argwhere(self.pattern == BayerIndex.R)[0]
        return self._section(x, y, section)

    def greenr(self, section: Rect | None) -> IntArray2D:
        y, x = np.argwhere(self.pattern == BayerIndex.Gr)[0]
        return self._section(x, y, section)

    def greenb(self, section: Rect | None) -> IntArray2D:
        y, x = np.argwhere(self.pattern == BayerIndex.Gb)[0]
        return self._section(x, y, section)

    def blue(self, section: Rect | None) -> IntArray2D:
        y, x = np.argwhere(self.pattern == BayerIndex.B)[0]
        return self._section(x, y, section)

    def red_black_level(self) -> int:
        return self.black_levels[BayerIndex.R]

    def greenr_black_level(self) -> int:
        return self.black_levels[BayerIndex.Gr]

    def greenb_black_level(self) -> int:
        return self.black_levels[BayerIndex.Gb]

    def blue_black_level(self) -> int:
        return self.black_levels[BayerIndex.B]
