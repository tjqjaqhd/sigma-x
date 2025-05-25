import importlib

redis = importlib.import_module("redis.asyncio")
from typing import AsyncIterator, Optional


class Redis:
    """애플리케이션용 Redis 인터페이스.

    Redis 연결 풀을 관리하며 간단한 Pub/Sub 및 키-값 조작 메서드를 제공한다.
    """

    def __init__(self, url: str = "redis://localhost") -> None:
        self.pool = redis.ConnectionPool.from_url(url)
        self.client = redis.Redis(connection_pool=self.pool)

    async def publish(self, channel: str, message: str) -> None:
        """주어진 채널에 메시지를 발행한다."""
        await self.client.publish(channel, message)

    async def subscribe(self, channel: str) -> AsyncIterator[str]:
        """지정한 채널을 구독하고 메시지를 비동기 이터레이터로 반환한다."""
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel)
        try:
            async for item in pubsub.listen():
                if item.get("type") == "message":
                    yield item["data"].decode() if isinstance(item["data"], bytes) else item["data"]
        finally:
            await pubsub.unsubscribe(channel)

    async def get(self, key: str) -> Optional[str]:
        """키의 값을 문자열로 반환한다."""
        value = await self.client.get(key)
        if value is not None and isinstance(value, bytes):
            return value.decode()
        return value

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        """키에 값을 저장한다. `ex`는 만료 시간을 초 단위로 지정한다."""
        await self.client.set(key, value, ex=ex)
