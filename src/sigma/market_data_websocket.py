"""실시간 시세 WebSocket 수집 모듈.

사양은
`docs/4_development/module_specs/interfaces/MarketDataWebSocket_Spec.md`
를 따른다.
"""

from __future__ import annotations

import json
import logging
from typing import Iterable, Optional

import websockets


class DummyRedis:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    async def publish(self, channel: str, message: str) -> None:
        """디버그 로그로 메시지를 기록한다."""  # pragma: no cover
        self.logger.debug("%s: %s", channel, message)


class MarketDataWebSocket:
    """거래소 WebSocket을 연결하고 틱 데이터를 Redis로 전달한다."""

    def __init__(
        self, url: str, symbols: Iterable[str], redis=None, logger=None
    ) -> None:
        self.url = url
        self.symbols = list(symbols)
        self.logger = logger or logging.getLogger(__name__)
        self.redis = redis or DummyRedis(logger=self.logger)
        self.ws: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self) -> None:
        self.ws = await websockets.connect(self.url)
        self.logger.debug("WS 연결: %s", self.url)

    async def subscribe(self) -> None:
        assert self.ws
        if "upbit" in self.url:
            payload = [
                {"ticket": "sigma"},
                {"type": "ticker", "codes": self.symbols},
            ]
        else:
            streams = [f"{s.lower()}@ticker" for s in self.symbols]
            payload = {"method": "SUBSCRIBE", "params": streams, "id": 1}
        await self.ws.send(json.dumps(payload))

    def _standardize(self, data: dict) -> dict:
        if "code" in data:
            return {
                "symbol": data["code"],
                "bid": data.get("tp"),
                "ask": data.get("ap"),
                "ts": data.get("ttm"),
            }
        if "s" in data:
            return {
                "symbol": data["s"],
                "bid": float(data.get("b", 0)),
                "ask": float(data.get("a", 0)),
                "ts": data.get("E", 0) / 1000,
            }
        return data

    async def forward_tick(self) -> None:
        assert self.ws
        async for msg in self.ws:
            try:
                data = json.loads(msg)
            except json.JSONDecodeError:
                continue
            tick = self._standardize(data)
            await self.redis.publish("market.tick", json.dumps(tick))
            self.logger.debug("틱 전송: %s", tick)

    async def run(self) -> None:
        await self.connect()
        await self.subscribe()
        await self.forward_tick()
