# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# standard library
# ----------------
from collections.abc import Generator
from contextlib import contextmanager

import decouple  # pyright: ignore[reportMissingImports]
from sqlalchemy import create_engine, event
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from ..errors import DatabaseNotFoundError

# ---------------
# Own dependecies
# ---------------
from ..ports import Database


class DcplDatabase(Database):
    @staticmethod
    def _set_sqlite_pragma(
        dbapi_connection,
        connection_record,
    ) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def __init__(self, env_var: str = "DATABASE_URL") -> None:
        self._env_var = env_var
        self._engine = None

    def init(self) -> None:
        try:
            url: str = decouple.config(self._env_var)
        except Exception as e:
            raise DatabaseNotFoundError(str(e))
        self._engine = create_engine(
            url,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},
        )
        self._session_factory = sessionmaker(self._engine, autoflush=False, expire_on_commit=False)
        if url.startswith("sqlite"):
            event.listen(
                self._engine,
                "connect",
                self._set_sqlite_pragma,
            )

    @contextmanager
    def session(self) -> Generator[Session]:
        with self._session_factory() as _session:
            yield _session

    @property
    def engine(self) -> Engine | None:
        return self._engine


__all__ = ["DcplDatabase"]
