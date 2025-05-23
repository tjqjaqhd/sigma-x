"""TrendScanner 모듈.

시장 데이터를 주기적으로 분석해 추세 변화를 감지한다.
"""

from __future__ import annotations

import collections
from sigma.common.logging_service import get_logger
from typing import Deque, Dict, Iterable


class DummyRedis:
    async def publish(self, channel: str, message: str) -> None:  # pragma: no cover
        print(f"{channel}: {message}")


class TrendScanner:
    def __init__(self, period: int = 5, redis=None, logger=None) -> None:
        self.period = period
        self.redis = redis or DummyRedis()
        self.logger = logger or get_logger(__name__)
        self.prices: Deque[float] = collections.deque(maxlen=period)

    async def scan_market(self, price: float, symbol: str) -> None:
        self.prices.append(price)
        if len(self.prices) < self.period:
            return

        avg = sum(self.prices) / self.period
        trend = "UP" if price > avg else "DOWN"
        msg = {"symbol": symbol, "trend": trend}
        await self.redis.publish("trend.signal", str(msg))
        self.logger.debug("추세 신호: %s", msg)

    async def start(self, source: Iterable[Dict[str, float]]) -> None:
        for data in source:
            await self.scan_market(data["price"], data.get("symbol", "BTC"))
