"""외부 뉴스 수집 및 브로드캐스트 모듈."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional


class NewsHandler:
    """주기적으로 뉴스를 수집해 이벤트로 전파한다."""

    def __init__(self, api, redis=None, interval: float = 60.0, logger=None) -> None:
        self.api = api
        self.redis = redis
        self.interval = interval
        self.logger = logger or logging.getLogger(__name__)
        self._running = False

    async def fetch_news(self) -> List[Dict[str, Any]]:
        try:
            return await self.api.get("/news")
        except Exception as exc:  # pragma: no cover - 네트워크 오류
            self.logger.warning("뉴스 수집 실패: %s", exc)
            return []

    async def broadcast(self, item: Dict[str, Any]) -> None:
        if self.redis:
            await self.redis.publish("news.events", item)
        self.logger.debug("뉴스 이벤트 전송: %s", item)

    async def run(self) -> None:
        self._running = True
        while self._running:
            for item in await self.fetch_news():
                await self.broadcast(item)
            await asyncio.sleep(self.interval)

    async def stop(self) -> None:
        self._running = False

