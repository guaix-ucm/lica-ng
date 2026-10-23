# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import re
from typing import NamedTuple, SupportsIndex
from operator import index

# ----------------
# Own dependencies
# ----------------
from .errors import RawBaseError


class InvalidRectStringError(RawBaseError):
    """Rectangle string incorrectly formatted"""


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, rhs: object) -> "Point":
        if not isinstance(rhs, Point):
            return NotImplemented
        return Point(self.x + rhs.x, self.y + rhs.y)

    def __mul__(self, rhs: SupportsIndex) -> "Point":
        n = index(rhs)
        return Point(self.x * n, self.y * n)

    def __floordiv__(self, rhs: int) -> "Point":
        return Point(self.x // rhs, self.y // rhs)

    @classmethod
    def zero(cls) -> "Point":
        return cls(0, 0)


PATTERN: re.Pattern[str] = re.compile(r"\[(\d+):(\d+),(\d+):(\d+)\]")


class Rect(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> "Rect":
        return cls(p1.x, p1.y, p2.x, p2.y)

    @classmethod
    def from_string(cls, value: str) -> "Rect":
        match = re.fullmatch(PATTERN, value.strip())
        if match is None:
            raise InvalidRectStringError(f"{value!r}")
        x1, y1, x2, y2 = map(int, match.groups())
        return cls(x1, y1, x2, y2)

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def shape(self) -> tuple[int, int]:
        """numpy style -> (height, width)"""
        return self.y2 - self.y1,  self.x2 - self.x1

    @property
    def dimensions(self) -> tuple[int, int]:
        """returns -> (width, height)"""
        return self.x2 - self.x1, self.y2 - self.y1

    @property
    def origin(self) -> Point:
        return Point(self.x1, self.y1)

    @property
    def central(self) -> Point:
        return Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    def contains(self, other: "Rect") -> bool:
        return (
            (self.x1 <= other.x1)
            and (self.y1 <= other.y1)
            and (other.x2 <= self.x2)
            and (other.y2 <= self.y2)
        )

    def recenter_on(self, screen: "Rect") -> "Rect":
        c_screen = screen.central
        c_self = self.central
        dx = c_screen.x - c_self.x
        dy = c_screen.y - c_self.y
        return self + Point(dx, dy)

    def __str__(self) -> str:
        """as a numpy slice"""
        return f"[{self.y1}:{self.y2},{self.x1}:{self.x2}]"

    def __add__(self, rhs: object) -> "Rect":
        """Add a Point to a Rect and prodcue a new Rect"""
        if not isinstance(rhs, Point):
            return NotImplemented
        return Rect(self.x1 + rhs.x, self.y1 + rhs.y, self.x2 + rhs.x, self.y2 + rhs.y)

    def __mul__(self, rhs: SupportsIndex) -> "Rect":
        """Multiply Rect by an integer and produce another Rect"""
        n = index(rhs)
        return Rect(self.x1 * n, self.y1 * n, self.x2 * n, self.y2 * n)

    def __floordiv__(self, rhs: int) -> "Rect":
        """Divide Rect by an integer and produce another Rect"""
        return Rect(self.x1 // rhs, self.y1 // rhs, self.x2 // rhs, self.y2 // rhs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rect):
            return NotImplemented
        return (
            self.x1 == other.x1
            and self.y1 == other.y1
            and self.x2 == other.x2
            and self.y2 == other.y2
        )

def autocenter(screen_raw_width: int, screen_raw_height: int, width: int, height: int) -> Rect:
    dim = Point(width, height) * 2  # to raw coordinates
    raw_size = Point(screen_raw_width, screen_raw_height)
    raw_screen = Rect.from_points(Point.zero(), raw_size)
    rect = Rect.from_points(Point.zero(), dim).recenter_on(raw_screen)
    rect = rect // 2  # to each plane coordinates
    return rect
