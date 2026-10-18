# lica-cli

## Introduction

`lica-cli` is a startup utility for LICA Python command-line applications. It provides a small, consistent API for parsing common command-line arguments and running either synchronous or asynchronous application entry points.

The package integrates with `lica-log`: it creates the standard CLI logging options, parses them into an `argparse.Namespace`, and passes them to a logging adapter. It also returns a process exit code after handling normal completion, keyboard interruption, and unexpected errors.

## Installation

Install `lica-cli` directly from PyPI:

```bash
pip install lica-cli
```

The package depends on `lica-log`, which is installed automatically.

If you use [uv](https://docs.astral.sh/uv/), add it to your project:

```toml
[project]
dependencies = [
    "lica-cli",
]
```

## Public API

The public API is:

```python
from lica_cli import parse_args, run_cli
```

### Parsing arguments

```python
parse_args(
    add_args_func: Callable[[ArgumentParser], None],
    name: str,
    version: str,
    description: str,
) -> Namespace
```

`parse_args()` creates an `ArgumentParser`, adds the common LICA CLI options, calls `add_args_func()` so the application can add its own options, and parses `sys.argv[1:]`.

The following common options are added automatically:

| Option | Description |
|---|---|
| `--version` | Prints the application name and version. |
| `--console` | Enables logging to the console. |
| `--log-file <FILE>` | Writes log messages to the given file. |
| `--log-level` | Sets the logging level using `lica_log.LogLevel`. |
| `--trace` | Prints the full traceback when an unexpected exception occurs. |

### Running a synchronous application

```python
run_cli(
    main_func: Callable[[Namespace], None],
    args: Namespace,
    name: str,
    version: str,
    logger: Logger,
) -> int
```

`run_cli()` configures the logger, runs `main_func(args)`, and returns `0` on success. It returns `1` after a `KeyboardInterrupt` or an unhandled exception. If `args.trace` is true, it also prints the exception traceback.

### Running an asynchronous application

```python
run_cli(
    main_func: Callable[[Namespace], Coroutine[Any, Any, None]],
    args: Namespace,
    name: str,
    version: str,
    logger: AsyncLogger,
) -> int
```

The asynchronous variant starts the `QueueListener` returned by `AsyncLogger.configure()`, runs the application coroutine with `asyncio.run()`, and returns the same exit-code convention as the synchronous API.

## Input validators

The package also provides reusable command-line argument validators in `lica_cli.validate` to be used in an `ArgumentParser`. To name a few:

- `vfile`: validates an existing file.
- `vdir`: validates an existing directory.
- `vbool`: validates `"True"` or `"False"`.
- `vdate`: validates several ISO-like date and datetime formats.
- `vmac`: validates and normalises a MAC address.

Example:

```python
from lica_cli.validate import vfile

parser.add_argument(
    "--config",
    type=vfile,
    help="Path to an existing configuration file.",
)
```

## Usage example

### Synchronous application

```python
import logging
import sys
from argparse import ArgumentParser, Namespace

from lica_cli import parse_args, run_cli
from lica_cli.validate import vdate
from lica_log.adapters.default import DefaultLogger

from myprog import __version__

DESCRIPTION = "My program short description"

log = logging.getLogger(__name__.split(".")[-1])


def add_args(parser: ArgumentParser) -> None:
    """Add extra CLI arguments here."""
    parser.add_argument(
        "-d",
        "--images-dir",
        type=vdir,
        action="store",
        metavar="<path>",
        help="Base directory to edit FITS files",
    ).


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

### Asynchronous application

```python
import logging
import sys
from argparse import ArgumentParser, Namespace

from lica_cli.asyncio import parse_args, run_cli
from lica_log.asyncio.adapters.default import AsyncDefaultLogger

from myprog import __version__

DESCRIPTION = "My asynchronous program"

log = logging.getLogger(__name__.split(".")[-1])


def add_args(parser: ArgumentParser) -> None:
    """Add extra CLI arguments here."""
    pass


async def cli_main(args: Namespace) -> None:
    log.info("Hello World")


def main():
    args = parse_args(add_args, __name__, __version__, DESCRIPTION)
    logger = AsyncDefaultLogger(args)

    return_code = run_cli(cli_main, args, __name__, __version__, logger)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
```
