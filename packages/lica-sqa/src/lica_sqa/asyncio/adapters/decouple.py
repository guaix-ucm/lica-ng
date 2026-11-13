# ----------------------------------------------------------------------
# Copyright (c) 2026 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------
# ----------------
# standard library
# ----------------
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

# ---------------------
# Third party libraries
# ---------------------
import decouple
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ...errors import DatabaseNotFoundError

# -----------------
# Local dependecies
# -----------------
from ..ports import AsyncDatabase


class AsyncDcplDatabase(AsyncDatabase):
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
        self._engine = create_async_engine(
            url,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},
        )
        self._session_factory = async_sessionmaker(
            self._engine, autoflush=False, expire_on_commit=False
        )
        if url.startswith("sqlite"):
            event.listen(
                self._engine.sync_engine,
                "connect",
                self._set_sqlite_pragma,
            )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with self._session_factory() as _session:
            yield _session

    @property
    def engine(self) -> AsyncEngine | None:
        return self._engine


__all__ = ["AsyncDcplDatabase"]
