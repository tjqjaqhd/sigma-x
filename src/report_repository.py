from __future__ import annotations

from .database import BacktestResult, SessionLocal, init_db


class ReportRepository:
    """성과 리포트 저장소."""

    def __init__(self, db_session=None) -> None:
        if db_session is None:
            init_db()
            self.db = SessionLocal()
        else:
            self.db = db_session

    def save(self, profit: float) -> None:
        self.db.add(BacktestResult(profit=profit))
        self.db.commit()
