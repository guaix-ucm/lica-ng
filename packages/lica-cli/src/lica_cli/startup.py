# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import logging
import traceback
from argparse import Namespace
from typing import Callable
from collections.abc import

from lica_log import Logger

# get the root logger
log = logging.getLogger()


def run_cli(
    main_func: Callable[[Namespace], None],
    args: Namespace,
    name: str,
    version: str,
    logger: Logger,
) -> int:
    return_code = 1
    try:
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
