# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

# -----------------
# Standard library
# ----------------

import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler

from .types import LogLevel

# -----------------------
# Module global variables
# -----------------------

# get the root logger
log = logging.getLogger()


def root_logger(
    level: LogLevel,
    console: bool,
    log_file: str | None = None,
    rotate: bool = False,
    fmt_str: str | None = None,
) -> None:
    """Configure the root logger"""
    # set the root logger level
    log.setLevel(level)
    # Log formatter
    # fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    if fmt_str is None:
        fmt_str = "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s"
    fmt = logging.Formatter(fmt_str)
    # remove previous handlers installed at load time by other libraries
    for h in log.handlers:
        log.removeHandler(h)
    # create console handler and set level to debug
    if console:
        ch = StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(logging.DEBUG)
        log.addHandler(ch)
    # Create a file handler suitable for logrotate usage
    if log_file:
        fh = (
            TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=365)
            if rotate
            else WatchedFileHandler(log_file)
        )
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        log.addHandler(fh)
