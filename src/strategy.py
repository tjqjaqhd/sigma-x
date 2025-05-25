from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """추상 전략 클래스."""

    @abstractmethod
    async def process(self, price: float) -> str:
        """가격을 입력받아 주문 신호를 반환한다."""
        raise NotImplementedError


class MovingAverageStrategy(BaseStrategy):
    """단순 이동평균 교차 전략."""

    def __init__(self, short_window: int = 3, long_window: int = 5) -> None:
        self.short_window = short_window
        self.long_window = long_window
        self.prices: list[float] = []

    async def process(self, price: float) -> str:
        self.prices.append(price)
        if len(self.prices) > self.long_window:
            self.prices.pop(0)
        if len(self.prices) >= self.long_window:
            short_ma = sum(self.prices[-self.short_window :]) / self.short_window
            long_ma = sum(self.prices) / self.long_window
            if short_ma > long_ma:
                return "BUY"
            if short_ma < long_ma:
                return "SELL"
        return "HOLD"
