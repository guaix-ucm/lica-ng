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
    def r(self, section: Rect | None) -> IntArray2D: ...
    def gr(self, section: Rect | None) -> IntArray2D: ...
    def gb(self, section: Rect | None) -> IntArray2D: ...
    def b(self, section: Rect | None) -> IntArray2D: ...

    def r_black(self) -> int: ...
    def gr_black(self) -> int: ...
    def gb_black(self) -> int: ...
    def b_black(self) -> int: ...

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
