"""Redis `price_update` 구독 모듈."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable, Optional

import aioredis


class RedisSubscriber:
    """실시간 가격 업데이트를 구독한다."""

    def __init__(
        self,
        redis_url: str = "redis://localhost",
        channel: str = "price_update",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.redis_url = redis_url
        self.channel = channel
        self.redis: Optional[aioredis.Redis] = None
        self.logger = logger or logging.getLogger(__name__)

    async def connect(self) -> None:
        self.redis = await aioredis.from_url(self.redis_url, decode_responses=True)
        self.logger.debug("Redis 연결: %s", self.redis_url)

    async def start(self, callback: Callable[[dict], Any]) -> None:
        if self.redis is None:
            await self.connect()

        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.channel)
        try:
            async for msg in pubsub.listen():
                if msg["type"] != "message":
                    continue
                try:
                    data = json.loads(msg["data"])
                except json.JSONDecodeError:
                    self.logger.warning("잘못된 메시지: %s", msg["data"])
                    continue
                await callback(data)
        finally:
            await pubsub.unsubscribe(self.channel)

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()

