from __future__ import annotations

import time


class SystemStatus:
    """모듈 헬스 상태를 Redis에 기록."""

    def __init__(self, redis_client=None, prefix: str = "system_status") -> None:
        self.redis = redis_client
        self.prefix = prefix

    async def _ensure_redis(self) -> None:
        if self.redis is None:
            import redis.asyncio as redis

            self.redis = redis.from_url("redis://localhost")

    async def report(self, name: str, status: str) -> None:
        await self._ensure_redis()
        key = f"{self.prefix}:{name}"
        ts = int(time.time())
        await self.redis.hset(key, mapping={"status": status, "ts": ts})

    async def get(self, name: str) -> dict:
        await self._ensure_redis()
        key = f"{self.prefix}:{name}"
        return await self.redis.hgetall(key)
