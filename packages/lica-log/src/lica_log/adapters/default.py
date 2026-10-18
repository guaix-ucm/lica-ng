# ----------------------------------------------------------------------
# Copyright (c) 2026
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# -----------------
# Standard library
# ----------------

import logging
from argparse import Namespace
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler

from .. import Logger
from ..common import to_std_logging

# -----------------------
# Module global variables
# -----------------------

# get the root logger
log = logging.getLogger()


class DefaultLogger(Logger):
    def __init__(self, args: Namespace, fmt: str | None = None, rotate: bool = False) -> None:
        self.args = args
        self.rotate = rotate
        self.fmt = (
            "%(asctime)s [%(levelname)-8s] %(message)s" if fmt is None else fmt
        )


    def configure(self) -> None:
        # set the root logger level
        log.setLevel(to_std_logging(self.args.log_level))
        # Log formatter
        # fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
        fmt = logging.Formatter(self.fmt)
        # remove previous handlers installed at load time by other libraries
        for h in log.handlers:
            log.removeHandler(h)
        # create console handler and set level to debug
        if self.args.console:
            ch = StreamHandler()
            ch.setFormatter(fmt)
            ch.setLevel(logging.DEBUG)
            log.addHandler(ch)
        # Create a file handler suitable for logrotate usage
        if self.args.log_file:
            fh = (
                TimedRotatingFileHandler(
                    self.args.log_file, when="midnight", interval=1, backupCount=365
                )
                if self.rotate
                else WatchedFileHandler(self.args.log_file)
            )
            fh.setFormatter(fmt)
            fh.setLevel(logging.DEBUG)
            log.addHandler(fh)
