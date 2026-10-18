# lica-tables

## Introduction

`lica-tables` is a lightweight utility for displaying tabular data in day-to-day LICA Python command-line applications. It defines a minimal display interface based on `typing.Protocol` and provides an adapter that renders tables in the standard output using [`tabulate`](https://pypi.org/project/tabulate/).

The package supports plain text output, optional table titles, several `tabulate` formats, and optional pagination for long tables. Application code depends only on the `DisplayService` protocol, while the concrete rendering behaviour is supplied by an adapter.

## Installation

Install `lica-tables` directly from the `lica-ng` Git repository:

```bash
pip install lica-tables
```

or add it to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "lica-tables",
]
```

The included `StdoutDisplay` adapter requires `tabulate`:

```toml
[project]
dependencies = [
    "lica-tables",
    "tabulate",
]
```

## Interfaces

`lica-tables` defines its display contracts using `typing.Protocol`. Adapters do not need to inherit from these protocols explicitly; they only need to provide the required methods.

### Tabular data

```python
from dataclasses import Field
from typing import Any, ClassVar, Protocol, TypeVar
from collections.abc import Mapping, Sequence


class DataclassLike(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


DataClass = TypeVar("DataClass", bound=DataclassLike)

TableRow = DataClass | Mapping[str, Any] | Sequence[Any]
TabularData = Sequence[TableRow]
```

A table row may therefore be:

- A dataclass instance.
- A mapping, typically with string keys.
- Any sequence of values.

### Display service

```python
from collections.abc import Sequence
from typing import Protocol

from lica_tables import TabularData


class DisplayService(Protocol):
    def show(self, text: str) -> None: ...

    def show_tabular(
        self,
        table: Sequence[TabularData],
        keys: Sequence[str] | None = None,
    ) -> None: ...
```

## Adapters

| Adapter | Module | Extra | Description |
|---|---|---|---|
| `StdoutDisplay` | `lica_tables.adapters.tabulate` | `tabulate` | Renders tabular data to standard output using `tabulate.tabulate`. |

The adapter is created with an optional `tabulate` table format and an optional page size:

```python
StdoutDisplay(table_fmt: str = "simple", page_size: int | None = None) -> None
```

### Supported table formats

`StdoutDisplay` accepts the following `tabulate` formats:

- `simple`
- `grid`
- `fancy_grid`
- `outline`
- `presto`
- `plain`
- `psql`

For formats that draw a complete table frame, an optional title is rendered inside the top border. For simpler formats, the title is centred above the table.

### Pagination

If `page_size` is set, `show_tabular()` splits the input rows into fixed-size pages. After each page, it waits for the user to press `Enter` before displaying the next one. `Ctrl-C` aborts the display.

## Usage example

```python
from dataclasses import dataclass

from lica_tables import DisplayService
from lica_tables.adapters.tabulate import StdoutDisplay


@dataclass
class Star:
    name: str
    magnitude: float
    spectral_type: str


stars = [
    Star("Sirius", -1.46, "A1V"),
    Star("Vega", 0.03, "A0V"),
    Star("Betelgeuse", 0.50, "M1-2Ia-Iab"),
]

display: DisplayService = StdoutDisplay(table_fmt="fancy_grid")

display.show_tabular(
    stars,
    keys=["Name", "Magnitude", "Spectral type"],
    title="Bright stars",
)
```

Example output:

```text
╔══════════════════════════════════════════════╗
║                 Bright stars                 ║
╠═════════════╦═══════════════╦════════════════╣
║ Name        ║   Magnitude   ║ Spectral type  ║
╠═════════════╬═══════════════╬════════════════╣
║ Sirius      ║         -1.46 ║ A1V            ║
║ Vega        ║          0.03 ║ A0V            ║
║ Betelgeuse  ║          0.50 ║ M1-2Ia-Iab     ║
╚═════════════╩═══════════════╩════════════════╝
```

## Usage example, with lica-cli package

```python
import sys
from argparse import ArgumentParser, Namespace

from lica_cli import parse_args, run_cli
from lica_tables.adapters.tabulate import StdoutDisplay

from myprog import __version__

DESCRIPTION = "My program short description"


def add_args(parser: ArgumentParser) -> None:
    """Add extra CLI arguments here"""
    pass


def cli_main(args: Namespace) -> None:
    rows = [
        ["Sirius", -1.46, "A1V"],
        ["Vega", 0.03, "A0V"],
    ]

    display = StdoutDisplay(table_fmt="simple")
    display.show_tabular(
        rows,
        keys=["Name", "Magnitude", "Spectral type"],
        title="Bright stars",
    )


def main():
    args = parse_args(add_args, __name__, __version__, DESCRIPTION)
    return_code = run_cli(cli_main, args, __name__, __version__)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
```
