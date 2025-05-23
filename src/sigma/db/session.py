"""SQLAlchemy 세션 관리 모듈.

`docs/4_development/module_specs/common/DBSession_Spec.md` 사양을 따른다.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as _Session, sessionmaker


class DBSession:
    """엔진과 세션 팩토리를 생성해 트랜잭션 컨텍스트를 제공한다."""

    def __init__(self, dsn: str, pool_size: int = 5) -> None:
        self.engine = create_engine(dsn, pool_size=pool_size, future=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )

    def get_session(self) -> _Session:
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[_Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
