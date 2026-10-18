# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# Standard library
# ----------------
import asyncio
import logging
import traceback
from argparse import Namespace
from typing import Any, Coroutine, Callable

# ----------------
# Own dependencies
# ----------------
from lica_log.asyncio import AsyncLogger

# get the root logger
log = logging.getLogger()


def run_cli(
    main_func: Callable[[Namespace], Coroutine[Any, Any, None]],
    args: Namespace,
    name: str,
    version: str,
    logger: AsyncLogger,
) -> int:
    return_code = 1
    listener = None
    try:
        listener = logger.configure()
        listener.start()
        log.info("============== %s %s ==============", name, version)
        asyncio.run(main_func(args))
        return_code = 0
    except KeyboardInterrupt:
        log.critical("[%s] Interrupted by user", name)
    except Exception as e:
        log.critical("[%s] Fatal error => %s", name, e)
        if args.trace:
            traceback.print_exc()
    finally:
        if listener is not None:
            listener.stop()

    return return_code
