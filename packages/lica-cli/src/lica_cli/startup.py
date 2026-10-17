# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import sys
import traceback
from argparse import ArgumentParser, Namespace
from typing import Callable

from lica_log import LogLevel
from lica_log.logging import root_logger


def arg_parser(name: str, version: str, description: str) -> ArgumentParser:
    # create the top-level parser
    parser = ArgumentParser(prog=name, description=description)
    # Generic args common to every command
    parser.add_argument("--version", action="version", version="{0} {1}".format(name, version))
    parser.add_argument(
        "--console",
        action="store_true",
        default=False,
        help="Log to console (defaults to %(default).",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        metavar="<FILE>",
        default=None,
        help="Log to file (defaults to %(default).",
    )
    parser.add_argument(
        "--log-level", choices=LogLevel, default=None, help="Log level (defaults to %(default)"
    )
    parser.add_argument("--trace", action="store_true", help="Show exception stack trace.")
    return parser


def execute(
    main_func: Callable[[Namespace], None],
    add_args_func: Callable[[ArgumentParser], None],
    name: str,
    version: str,
    description: str,
    log_rotate: bool = False,
    log_fmt: str | None = None,
) -> None:
    try:
        print("CUCUUUUU")
        return
        return_code = 1
        parser = arg_parser(name, version, description)
        add_args_func(parser)  # Adds more arguments
        args = parser.parse_args(sys.argv[1:])
        log_level = LogLevel.INFO if args.log_level is None else args.log_level
        root_logger(log_level, args.console, args.log_file, log_rotate, log_fmt)
        log.info(f"============== {name} {version} ==============")
        main_func(args)
        return_code = 0
    except KeyboardInterrupt:
        log.critical("[%s] Interrupted by user ", name)
    except Exception as e:
        log.critical("[%s] Fatal error => %s", name, str(e))
        if args.trace:
            traceback.print_exc()
    finally:
        sys.exit(return_code)
