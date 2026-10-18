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
import traceback
from argparse import Namespace
from typing import Any, Callable, Coroutine

# ----------------
# Own dependencies
# ----------------
from lica_log import Logger

# get the root logger
log = logging.getLogger()


async def _wrapped_main(
    main_func: Callable[[Namespace], Coroutine[Any, Any, None]],
    args: Namespace,
    name: str,
    version: str,
    logger: Logger,
) -> None:
    """Internal coroutine that starts logging thread and the main coroutine"""
    global listener
    listener = logger.configure()
    listener.start()
    log.info("============== %s %s ==============", name, version)
    await main_func(args)


def run_cli(
    main_func: Callable[[Namespace], Coroutine[Any, Any, None]],
    args: Namespace,
    name: str,
    version: str,
    logger: Logger,
) -> int:
    return_code = 1
    try:
        logger.additional_args(args)
        asyncio.run(_wrapped_main(main_func, args, name, version, logger))
        return_code = 0
    except KeyboardInterrupt:
        log.critical("[%s] Interrupted by user", name)
    except Exception as e:
        log.critical("[%s] Fatal error => %s", name, e)
        if args.trace:
            traceback.print_exc()
    return return_code
