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
import queue
from argparse import Namespace
from logging import StreamHandler
from logging.handlers import (
    QueueHandler,
    QueueListener,
    TimedRotatingFileHandler,
    WatchedFileHandler,
)

from ...common import LogLevel, to_std_logging
from .. import AsyncLogger

# -----------------------
# Module global variables
# -----------------------

# get the root logger
log = logging.getLogger()


class DefaultAsyncLogger(AsyncLogger):
    def __init__(self, fmt_str: str | None = None, rotate: bool = False):
        self.level = LogLevel.INFO
        self.console = True
        self.log_file = None
        self.rotate = (rotate,)
        self.fmt = (
            "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s" if fmt_str is None else fmt_str
        )

    def additional_args(self, args: Namespace) -> None:
        self.level = args.log_level
        self.console = args.console
        self.log_file = args.log_file

    def configure(self) -> QueueListener:
        # set the root logger level
        log.setLevel(to_std_logging(self.level))
        # Log formatter
        # fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        fmt = logging.Formatter(self.fmt)
        # remove previous handlers installed at load time by other libraries
        for h in log.handlers:
            log.removeHandler(h)
        q = queue.Queue()
        log.addHandler(QueueHandler(q))
        handlers = list()
        if self.console:
            ch = StreamHandler()
            ch.setFormatter(fmt)
            ch.setLevel(logging.DEBUG)
            handlers.append(ch)
        if self.log_file:
            fh = (
                TimedRotatingFileHandler(
                    self.log_file, when="midnight", interval=1, backupCount=365
                )
                if self.rotate
                else WatchedFileHandler(self.log_file)
            )
            fh.setFormatter(fmt)
            fh.setLevel(logging.DEBUG)
            handlers.append(fh)
        listener = QueueListener(q, *handlers)
        return listener


def root_logger(
    level: LogLevel,
    console: bool,
    log_file: str | None = None,
    rotate: bool = False,
    fmt_str: str | None = None,
) -> QueueListener:
    """Configure the root logger"""
    # set the root logger level
    log.setLevel(to_std_logging(level))
    # Log formatter
    # fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    if fmt_str is None:
        fmt_str = "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s"
    fmt = logging.Formatter(fmt_str)
    # remove previous handlers installed at load time by other libraries
    for h in log.handlers:
        log.removeHandler(h)
    q = queue.Queue()
    log.addHandler(QueueHandler(q))
    handlers = list()
    if console:
        ch = StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(logging.DEBUG)
        handlers.append(ch)
    if log_file:
        fh = (
            TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=365)
            if rotate
            else WatchedFileHandler(log_file)
        )
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        handlers.append(fh)
    listener = QueueListener(q, *handlers)
    return listener
