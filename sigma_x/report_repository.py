from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

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

    def save_report(self, task_type: str, result: Dict[str, Any]) -> int:
        """작업 결과를 리포트로 저장합니다."""
        # 결과에서 profit 값을 추출 (기본값 0.0)
        profit = result.get('profit', 0.0) if isinstance(result, dict) else 0.0

        # BacktestResult에 저장
        report = BacktestResult(
            profit=profit,
            created_at=datetime.utcnow()
        )
        self.db.add(report)
        self.db.commit()

        return report.id

    def get_reports(self, limit: int = 100) -> list[Dict[str, Any]]:
        """저장된 리포트 목록을 반환합니다."""
        results = self.db.query(BacktestResult).order_by(BacktestResult.created_at.desc()).limit(limit).all()
        return [
            {
                "id": result.id,
                "profit": result.profit,
                "created_at": result.created_at.isoformat() if result.created_at else None
            }
            for result in results
        ]
