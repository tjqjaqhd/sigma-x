from __future__ import annotations

try:
    import redis.asyncio as redis  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    try:  # fallback to fakeredis if available
        import fakeredis.aioredis as redis  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover - ultimate fallback
        redis = None


class Redis:
    """애플리케이션용 Redis 인터페이스.

    키-값 저장소와의 연결을 관리하며 기본적인 pub/sub 및 리스트 명령을
    비동기로 제공합니다.

    예시:
        >>> store = Redis()
        >>> store.run()
    """

    def __init__(self, url: str = "redis://localhost") -> None:
        self.url = url
        self.client: redis.Redis | None = None

    async def _connect(self) -> redis.Redis:
        if redis is None:
            raise RuntimeError("redis library is not available")
        if self.client is None:
            self.client = redis.from_url(self.url)
        return self.client

    async def publish(self, channel: str, message: str) -> None:
        client = await self._connect()
        await client.publish(channel, message)

    def pubsub(self) -> redis.client.PubSub:
        if redis is None:
            raise RuntimeError("redis library is not available")
        if self.client is None:
            self.client = redis.from_url(self.url)
        return self.client.pubsub()

    async def rpush(self, key: str, value: str) -> None:
        client = await self._connect()
        await client.rpush(key, value)

    async def lrange(self, key: str, start: int, end: int):
        client = await self._connect()
        return await client.lrange(key, start, end)

    def run(self) -> None:
        """호환성을 위한 빈 메서드."""
        return None
