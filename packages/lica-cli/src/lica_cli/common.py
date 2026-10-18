# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
from argparse import ArgumentParser
import sys

from argparse import ArgumentParser, Namespace
from typing import Callable
from collections.abc import

def _create_arg_parser(name: str, version: str, description: str) -> ArgumentParser:
    # create the top-level parser
    parser = ArgumentParser(prog=name, description=description)
    # Generic args common to every command
    parser.add_argument("--version", action="version", version="{0} {1}".format(name, version))
    parser.add_argument(
        "--console",
        action="store_true",
        default=False,
        help="Log to console (defaults to %(default)s).",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        metavar="<FILE>",
        default=None,
        help="Log to file (defaults to %(default)s).",
    )
    parser.add_argument(
        "--log-level", choices=LogLevel, default=LogLevel.INFO, help="Log level (defaults to %(default)s)"
    )
    parser.add_argument("--trace", action="store_true", help="Show exception stack trace.")
    return parser



def parse_args(
    add_args_func: Callable[[ArgumentParser], None],
    name: str,
    version: str,
    description: str,
) -> Namespace:
    parser = _create_arg_parser(name, version, description)
    add_args_func(parser)
    return parser.parse_args(sys.argv[1:])
