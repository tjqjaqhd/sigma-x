from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """추상 전략 클래스."""

    @abstractmethod
    async def process(self, price: float) -> str:
        """가격을 입력받아 주문 신호를 반환한다."""
        raise NotImplementedError


# 기본 제공 전략은 strategies 패키지에서 불러와 재노출한다.
try:
    from .strategies.moving_average import MovingAverageStrategy
except Exception:  # pragma: no cover - fallback if plugins missing
    MovingAverageStrategy = None  # type: ignore

__all__ = ["BaseStrategy", "MovingAverageStrategy"]
