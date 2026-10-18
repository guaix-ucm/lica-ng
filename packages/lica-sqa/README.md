# lica-sqa

## Introduction

`lica-sqa` is a lightweight SQLAlchemy utility layer for day-to-day LICA Python applications. It defines minimal synchronous and asynchronous database interfaces, provides shared declarative-model metadata, and includes adapters that create SQLAlchemy engines and session factories from a configuration value.

The package supports conventional SQLAlchemy ORM models, asynchronous models based on `AsyncAttrs`, consistent database-object naming conventions, and a small helper for creating and dropping SQL views. Application code depends only on the `Database` or `AsyncDatabase` protocol, while the concrete database behaviour is supplied by an adapter.

## Installation

Install `lica-sqa` directly from the `lica-ng` Git repository:

```bash
pip install lica-sqa
```

or add it to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "lica-sqa",
]
```

The included adapters require SQLAlchemy and `python-decouple`:

```toml
[project]
dependencies = [
    "lica-sqa",
    "sqlalchemy",
    "python-decouple",
]
```

For asynchronous applications using SQLite, add an async driver such as `aiosqlite`:

```toml
[project]
dependencies = [
    "lica-sqa",
    "sqlalchemy",
    "python-decouple",
    "aiosqlite",
]
```

## Interfaces

`lica-sqa` defines its database contracts using `typing.Protocol`. Adapters do not need to inherit from these protocols explicitly; they only need to provide the required methods.

### Synchronous database

```python
from contextlib import AbstractContextManager
from typing import Protocol

from sqlalchemy.orm import Session


class Database(Protocol):
    """Application software uses this interface as the dependency."""

    def session(self) -> AbstractContextManager[Session]: ...
```

### Asynchronous database

```python
from contextlib import AbstractAsyncContextManager
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class AsyncDatabase(Protocol):
    """Application software uses this interface as the dependency."""

    def session(self) -> AbstractAsyncContextManager[AsyncSession]: ...
```

## Adapters

| Adapter | Module | Extra | Description |
|---|---|---|---|
| `DcplDatabase` | `lica_sqa.adapters.decouple` | `sqlalchemy`, `python-decouple` | Creates a synchronous SQLAlchemy engine and session factory from a `python-decouple` configuration value. |
| `AsyncDcplDatabase` | `lica_sqa.adapters.asyncio.decouple` | `sqlalchemy`, `python-decouple` | Creates an asynchronous SQLAlchemy engine and session factory from a `python-decouple` configuration value. |

Both adapters accept the name of the environment variable or configuration key containing the database URL:

```python
DcplDatabase(env_var: str = "DATABASE_URL") -> None
AsyncDcplDatabase(env_var: str = "DATABASE_URL") -> None
```

Call `init()` before using the adapter. It reads the database URL, creates the engine with `pool_pre_ping=True`, and creates a session factory with `autoflush=False` and `expire_on_commit=False`.

The expected configuration value is a standard SQLAlchemy database URL, for example:

```bash
DATABASE_URL=sqlite:///app.db
```

For an asynchronous SQLite database:

```bash
DATABASE_URL=sqlite+aiosqlite:///app.db
```

### Session usage

The `session()` method returns a context manager that yields a SQLAlchemy session and closes it automatically on exit.

```python
with database.session() as session:
    session.add(obj)
    session.commit()
```

For asynchronous adapters:

```python
async with database.session() as session:
    session.add(obj)
    await session.commit()
```

## Models and metadata

`lica-sqa` provides shared SQLAlchemy `MetaData` objects with a consistent naming convention for indexes, unique constraints, check constraints, foreign keys, and primary keys.

### Synchronous models

Derive application models from `Model`:

```python
from sqlalchemy.orm import Mapped, mapped_column

from lica_sqa import Model


class User(Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

### Asynchronous models

Derive asynchronous application models from `AsyncModel`:

```python
from sqlalchemy.orm import Mapped, mapped_column

from lica_sqa.metadata.asyncio import AsyncModel


class User(AsyncModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

`AsyncModel` combines SQLAlchemy’s `AsyncAttrs` and `DeclarativeBase`, enabling lazy attribute loading in asynchronous applications.

## SQL views

The `view()` helper creates a SQLAlchemy table-like object associated with a SQL view. It registers `CREATE VIEW` and `DROP VIEW` events on the supplied `MetaData`, creating the view only if it does not already exist and dropping it only if it exists.

```python
from sqlalchemy import select

from lica_sqa import metadata, view
from myapp.models import User

user_view = view(
    "user_names",
    metadata,
    select(User.id, User.name),
)
```

The helper is based on the SQLAlchemy views recipe and has been updated for SQLAlchemy 2.0.

## Logging

Use `sqa_logging()` to configure the verbosity of SQLAlchemy engine logging:

```python
from lica_sqa import sqa_logging

sqa_logging(debug=True)
```

When `debug=True`, the `sqlalchemy.engine` and `aiosqlite` loggers are set to `INFO`. Otherwise, `sqlalchemy.engine` is set to `WARNING`.

## Usage example, with lica-cli package

```python
import sys
from argparse import ArgumentParser, Namespace

from lica_cli import parse_args, run_cli
from lica_sqa import Database
from lica_sqa.adapters.decouple import DcplDatabase

from myapp.models import User
from myprog import __version__

DESCRIPTION = "My program short description"


def add_args(parser: ArgumentParser) -> None:
    """Add extra CLI arguments here"""
    pass


def cli_main(args: Namespace, database: Database) -> None:
    with database.session() as session:
        session.add(User(name="Alice"))
        session.commit()


def main():
    args = parse_args(add_args, __name__, __version__, DESCRIPTION)

    database: Database = DcplDatabase()
    database.init()

    return_code = run_cli(cli_main, args, __name__, __version__, database=database)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
```
