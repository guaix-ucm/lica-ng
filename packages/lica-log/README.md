# lica-log

## Introduction

`lica-log` is a lightweight logging utility for day-to-day LICA Python command-line applications. It defines a minimal logging interface and provides adapters that configure the standard Python root logger from parsed command-line arguments.

The package supports console logging, optional file logging with rotation, and an optional Textual-compatible handler. Application code depends only on the `Logger` protocol, while the concrete logging behaviour is supplied by an adapter.

## Installation

Install `lica-log` directly from the `lica-ng` Git repository:

```bash
pip install lica-log
```

To include support for Textual applications, install the `textual` optional dependency group:

```bash
pip install "lica-log[textual]"
```

or add to your `pyproject.toml` dependencies list

or add it to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "lica-log",
]
```

For a Textual-based application:

```toml
[project]
dependencies = [
    "lica-log[textual]",
]
```

## Interfaces

`lica-log` defines its logging contracts using `typing.Protocol`. Adapters do not need to inherit from these protocols explicitly; they only need to provide the required methods.

### Synchronous logger

```python
from typing import Protocol


class Logger(Protocol):
    def configure(self) -> None: ...
```

### Asynchronous logger

```python
from logging.handlers import QueueListener
from typing import Protocol


class AsyncLogger(Protocol):
    def configure(self) -> QueueListener: ...
```

## Adapters

| Adapter | Module | Extra | Description |
|---|---|---|---|
| `DefaultLogger` | `lica_log.adapters.default` | — | Configures the root logger using console and/or file handlers. |
| `TextualLogger` | `lica_log.adapters.textual` | `textual` | Configures the root logger for Textual applications, adding a `textual.logging.TextualHandler` when requested. |

Both adapters accept a parsed `argparse.Namespace`, an optional log format, and a rotation flag:

```python
DefaultLogger(args: Namespace, fmt: str | None = None, rotate: bool = False) -> None
```

The default log format string is `"%(asctime)s [%(levelname)-8s] %(message)s"`.  Another useful format string to be passed when debugging when creating the adapter can be `"%(asctime)s [%(levelname)-8s] [%(name)s] %(message)s"`.

The expected namespace attributes are:

- `log_level`: logging level, of type `lica_log.LogLevel`.
- `console`: enables a `StreamHandler` when true.
- `log_file`: path to a log file; enables file logging when set.
- `textual`: enables the Textual log handler in the Textual adapter.

These are usually provided by default by its sister package `lica-cli`

With `rotate=True`, file logging uses `TimedRotatingFileHandler`; otherwise it uses `WatchedFileHandler`, which is suitable for external log-rotation tools.

## Usage example, with lica-cli package

```python
import logging
import sys
from argparse import ArgumentParser, Namespace

from lica_cli import parse_args, run_cli
from lica_log.adapters.default import DefaultLogger

from myprog import __version__

DESCRIPTION = "My program short description"

log = logging.getLogger(__name__.split(".")[-1])


def add_args(parser: ArgumentParser) -> None:
    """Add extra CLI arguments here"""
    pass


def cli_main(args: Namespace) -> None:
    log.info("Hello World")


def main():
    args = parse_args(add_args, __name__, __version__, DESCRIPTION)
    logger = DefaultLogger(args)
    logger.configure()

    return_code = run_cli(cli_main, args, __name__, __version__, logger)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
```
