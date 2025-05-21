from __future__ import annotations

"""시장 국면 탐지 및 파라미터 조정 모듈."""

from sqlalchemy.orm import Session

from sigma.db.database import SessionLocal
from sigma.data.models import StrategyParam


class RegimeDetector:
    """간단한 시장 국면 탐지기."""

    def detect(self, market_data: dict) -> str:
        return "bull" if market_data.get("price", 0) > 0 else "bear"


class ParamAdjuster:
    """전략 파라미터를 DB에 반영합니다."""

    def __init__(self, session: Session | None = None) -> None:
        self.session = session or SessionLocal()

    def update_param(self, name: str, value: str) -> None:
        param = self.session.get(StrategyParam, name)
        if param is None:
            param = StrategyParam(name=name, value=value)
            self.session.add(param)
        else:
            param.value = value
        self.session.commit()


__all__ = ["RegimeDetector", "ParamAdjuster"]
