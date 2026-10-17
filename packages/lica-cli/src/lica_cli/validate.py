# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) 2021
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# --------------------
# System wide imports
#  -------------------

import math
import os
import fractions
import functools

from datetime import datetime
from typing import Union
from collections.abc import Sequence

# ------------------------
# Module utility functions
# ------------------------


def vfile(path: str) -> str:
    """File validator for the command line interface"""
    if not os.path.isfile(path):
        raise IOError(f"Not valid or existing file: {path}")
    return path


def vdir(path: str) -> str:
    """Directory validator for the command line interface"""
    if not os.path.isdir(path):
        raise IOError(f"Not valid or existing directory: {path}")
    return path


def vbool(boolstr: str) -> bool:
    """Boolean text validator for the command line interface"""
    result = None
    if boolstr == "True":
        result = True
    elif boolstr == "False":
        result = False
    else:
        raise ValueError(f"{boolstr} is not a valid boolean")
    return result


def vdate(datestr: str) -> datetime:
    """Date & time validator for the command line interface"""
    date = None
    formats = ("%Y-%m", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ")
    for fmt in formats:
        try:
            date = datetime.strptime(datestr, fmt)
        except ValueError:
            pass
    if date is None:
        raise ValueError(f"{datestr} is not a valid date format ({formats})")
    return date


def vmonth(datestr: str) -> datetime:
    return datetime.strptime(datestr, "%Y-%m")


def vyear(datestr: str) -> datetime:
    return datetime.strptime(datestr, "%Y")


def vfloat(num: str) -> float:
    """Validator that admits fractions"""
    return float(fractions.Fraction(num))


def vfloat01(num_str: str) -> float:
    """Validator between [0..1] that admits fractions"""
    num = float(fractions.Fraction(num_str))
    if not (0.0 <= num <= 1.0):
        raise ValueError(f"Value {num} out of bounds [0..1]")
    return num


def vnat(num_str: str) -> int:
    """Natural nambrs validator"""
    num = int(num_str)
    if not (num > 0):
        raise ValueError(f"Value {num} <= 0]")
    return num


def vint(L: int, H: int, num_str: str) -> int:
    """Integer validator between [L..H]"""
    num = int(num_str)
    if not (L <= num <= H):
        raise ValueError(f"Value {num} out of bounds [{L}..{H}]")
    return num


def voddint(L: int, H: int, num_str: str) -> int:
    """Odd integer validator between [L..H]"""
    num = int(num_str)
    if (L % 2) == 0:
        raise ValueError(f"Low bound value {L} is not an odd number")
    if (H % 2) == 0:
        raise ValueError(f"High bound value {H} is not an odd number")
    if (num % 2) == 0:
        raise ValueError(f"Value {num} is not an odd number")
    if not (3 <= num <= 11):
        raise ValueError(f"Value {num} out of bounds [{L}..{H}]")
    return num


def vevenint(L: int, H: int, num_str: str) -> int:
    """Even integer validator between [L..H]"""
    num = int(num_str)
    if (L % 2) == 1:
        raise ValueError(f"Low bound value {L} is not an even number")
    if (H % 2) == 1:
        raise ValueError(f"High bound value {H} is not an even number")
    if (num % 2) == 1:
        raise ValueError(f"Value {num} is not an even number")
    if not (L <= num <= H):
        raise ValueError(f"Value {num} out of bounds [{L}..{H}]")
    return num


def vflopath(value: str | float) -> str | float:
    """Validator that admits either a single number or a file (representing an image)"""
    try:
        n = float(fractions.Fraction(value))
    except ValueError:
        if not os.path.isfile(value):
            raise IOError(f"Not valid or existing file: {value}")
        return value
    return n


def vmac(mac: str) -> str:
    """'Valid input MAC strings"""
    try:
        corrected_mac = ":".join(f"{int(x, 16):02X}" for x in mac.split(":"))
    except ValueError:
        raise ValueError("Invalid MAC: %s" % mac)
    except AttributeError:
        raise ValueError("Invalid MAC: %s" % mac)
    return corrected_mac


def vsexa(value: str) -> float:
    """Validates HH.HHHH or HH:MM:SS.SSS and converts to floating point"""
    try:
        result = float(value)
    except ValueError:
        ang = value.split(":")
        if len(ang) != 3:
            raise ValueError(f"{value} is not a valid sexagesimal number")
        try:
            result = math.copysign(
                math.fabs(float(ang[0])) + float(ang[1]) / 60.0 + float(ang[2]) / 3600.00,
                float(ang[0]),
            )
        except Exception:
            raise ValueError(f"{value} could not be converted from sexagesimal to float")
    return result
