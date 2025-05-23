"""PostgreSQL 접속 래퍼.

`docs/4_development/module_specs/infrastructure/PostgreSQL_Spec.md` 사양을 따른다.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator, Iterable

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class Postgres:
    """동기식 PostgreSQL 클라이언트."""

    def __init__(self, dsn: str, pool_size: int = 5, echo: bool = False) -> None:
        self.engine: Engine = create_engine(
            dsn, pool_size=pool_size, echo=echo, future=True
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def execute_query(self, query: str, **params: Any) -> None:
        with self.session_scope() as session:
            session.execute(text(query), params)

    def fetch_all(self, query: str, **params: Any) -> Iterable[Any]:
        with self.session_scope() as session:
            result = session.execute(text(query), params)
            return result.fetchall()

    def close_db(self) -> None:
        self.engine.dispose()
