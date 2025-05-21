from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """전략 기본 클래스."""

    @abstractmethod
    def generate_signals(self, market_data: dict):
        """시장 데이터를 기반으로 매매 신호를 생성합니다."""
        raise NotImplementedError


class DummyStrategy(BaseStrategy):
    """매수와 매도 신호를 번갈아 발생시키는 더미 전략."""

    def generate_signals(self, market_data: dict):
        price = market_data.get("price", 0)
        for _ in range(5):
            if price > 0:
                yield "BUY"
                yield "SELL"
