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
from argparse import Namespace
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler

import textual.logging

from .. import Logger
from ..common import LogLevel, to_std_logging

# -----------------------
# Module global variables
# -----------------------

# get the root logger
log = logging.getLogger()


class TextualLogger(Logger):
    def __init__(self, fmt_str: str | None = None, rotate: bool = False) -> None:
        self.level = LogLevel.INFO
        self.console = True
        self.log_file = None
        self.rotate = rotate
        self.textual = True
        self.fmt = (
            "%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s" if fmt_str is None else fmt_str
        )

    def additional_args(self, args: Namespace) -> None:
        self.level = args.log_level
        self.console = args.console
        self.log_file = args.log_file
        self.textual = args.textual

    def configure(self) -> None:
        # set the root logger level
        log.setLevel(to_std_logging(self.level))
        # Log formatter
        # fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        fmt = logging.Formatter(self.fmt)
        # remove previous handlers installed at load time by other libraries
        for h in log.handlers:
            log.removeHandler(h)
        # create console handler and set level to debug
        if self.console:
            ch = StreamHandler()
            ch.setFormatter(fmt)
            ch.setLevel(logging.DEBUG)
            log.addHandler(ch)
        if self.textual:
            ch = textual.logging.TextualHandler()
            ch.setFormatter(fmt)
            ch.setLevel(logging.DEBUG)
            log.addHandler(ch)
        # Create a file handler suitable for logrotate usage
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
            log.addHandler(fh)
