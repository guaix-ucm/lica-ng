# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import asyncio
import logging
import sys
import traceback
from argparse import ArgumentParser, Namespace
from typing import Any, Callable, Coroutine

from lica_log import LogLevel
from lica_log.asyncio.logging import root_logger

# get the root logger
log = logging.getLogger()


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


async def _wrapped_main(
    main_func: Callable[[Namespace], Coroutine[Any, Any, None]],
    args: Namespace,
    name: str,
    version: str,
    log_rotate: bool,
    log_fmt: str | None,
) -> None:
    """Internal coroutine that starts logging thread and the main coroutine"""
    global listener
    listener = root_logger(args.log_level, args.console, args.log_file, log_rotate, log_fmt)
    listener.start()
    log.info("============== %s %s ==============", name, version)
    await main_func(args)


def execute(
    main_func: Callable[[Namespace], Coroutine[Any, Any, None]],
    add_args_func: Callable[[ArgumentParser], None],
    name: str,
    version: str,
    description: str,
    log_rotate: bool = False,
    log_fmt: str | None = None,
) -> None:
    """
    Utility entry point
    """
    try:
        return_code = 1
        parser = arg_parser(name, version, description)
        add_args_func(parser)  # Adds more arguments
        args = parser.parse_args(sys.argv[1:])
        asyncio.run(_wrapped_main(main_func, args, name, version, log_rotate, log_fmt))
        return_code = 0
    except KeyboardInterrupt:
        log.critical("[%s] Interrupted by user ", name)
    except Exception as e:
        log.critical("[%s] Fatal error => %s", name, str(e))
        if args.trace:
            traceback.print_exc()
    finally:
        if listener:
            listener.stop()
        sys.exit(return_code)
