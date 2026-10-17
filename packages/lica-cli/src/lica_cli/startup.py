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
import logging
import traceback
from argparse import ArgumentParser, Namespace
from typing import Callable
from collections.abc import

from lica_log import Logger
from .common import create_arg_parser

# get the root logger
log = logging.getLogger()


def parse_args(
    add_args_func: Callable[[ArgumentParser], None],
    name: str,
    version: str,
    description: str,
) -> Namespace:
    parser = create_arg_parser(name, version, description)
    add_args_func(parser)
    return parser.parse_args(sys.argv[1:])


def run_cli(
    main_func: Callable[[Namespace], None],
    args: Namespace,
    name: str,
    version: str,
    logger: Logger,
) -> int:
    return_code = 1
    try:
        logger.additional_args(args)
        logger.configure()
        log.info("============== %s %s ==============", name, version)
        main_func(args)
        return_code = 0
    except KeyboardInterrupt:
        log.critical("[%s] Interrupted by user", name)
    except Exception as e:
        log.critical("[%s] Fatal error => %s", name, e)
        if args.trace:
            traceback.print_exc()
    return return_code
