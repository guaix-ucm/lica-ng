# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
from types import TracebackType
from typing import Protocol, Self

# ----------------
# Own dependencies
# ----------------
from .models import ImageMetadata
from .rect import Rect
from .types import HeaderType, IntArray2D


class RawPixels(Protocol):
    def red(self, section: Rect | None) -> IntArray2D: ...
    def greenr(self, section: Rect | None) -> IntArray2D: ...
    def greenb(self, section: Rect | None) -> IntArray2D: ...
    def blue(self, section: Rect | None) -> IntArray2D: ...

    def red_black_level(self) -> int: ...
    def greenr_black_level(self) -> int: ...
    def greenb_black_level(self) -> int: ...
    def blue_black_level(self) -> int: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...


class ImageReader(Protocol):
    def header_type(self) -> HeaderType: ...

    def read_metadata(self, path: str) -> ImageMetadata:
        """returns an instance of ImageMetadata dataclass"""
        ...

    def read_pixels(self, path: str) -> RawPixels:
        """returns an object that implements the RawPixels interface"""
        ...


class ImageReaderFactory(Protocol):
    def get_reader(self, path: str) -> ImageReader:
        """returns an object that implements the ImageReader interface"""
        ...
