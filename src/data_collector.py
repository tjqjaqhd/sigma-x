import asyncio
import os
from typing import Optional

import websockets


class DataCollector:
    """시세 데이터를 수집하는 모듈.

    외부 거래소나 데이터 소스에서 시세 정보를 받아 Redis 채널로 전달합니다.

    예시:
        >>> collector = DataCollector()
        >>> await collector.run()
    """

    def __init__(
        self,
        url: str | None = None,
        *,
        redis_client=None,
        rabbitmq_client=None,
        channel: str = "ticks",
        queue: str = "ticks",
    ) -> None:
        self.url = url or os.getenv("SIGMA_WS_URL", "ws://localhost:8765")
        self.redis = redis_client
        self.rabbitmq = rabbitmq_client
        self.channel = channel
        self.queue = queue

    async def __aenter__(self) -> "DataCollector":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        """호환성을 위한 빈 메서드."""
        return None

    async def run(self, limit: Optional[int] = None) -> None:
        """WebSocket에서 데이터를 읽어 큐 혹은 Redis로 전달한다."""

        if self.rabbitmq is None and self.redis is None:
            import redis.asyncio as redis

            self.redis = redis.from_url("redis://localhost")

        received = 0
        while True:
            try:
                async with websockets.connect(self.url) as ws:
                    async for message in ws:
                        if self.rabbitmq is not None:
                            await self.rabbitmq.publish(self.queue, message)
                        else:
                            await self.redis.publish(self.channel, message)
                        received += 1
                        if limit and received >= limit:
                            return
            except (websockets.WebSocketException, OSError):
                await asyncio.sleep(1)
