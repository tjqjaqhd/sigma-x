"""Redis Pub/Sub 래퍼 모듈.

사양은 ``docs/4_development/module_specs/infrastructure/RedisPubSub_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, AsyncGenerator, Dict, Optional

import aioredis


class RedisPubsub:
    def __init__(self, url: str = "redis://localhost", logger=None) -> None:
        self.url = url
        self.redis: Optional[aioredis.Redis] = None
        self.logger = logger or logging.getLogger(__name__)

    async def connect(self) -> None:
        self.redis = await aioredis.from_url(self.url, decode_responses=True)
        self.logger.debug("Redis 연결 완료: %s", self.url)

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()

    async def publish(self, channel: str, message: Dict[str, Any]) -> None:
        assert self.redis
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str) -> AsyncGenerator[Dict[str, Any], None]:
        assert self.redis
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        try:
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    yield json.loads(msg["data"])
        finally:
            await pubsub.unsubscribe(channel)

