import asyncio
from typing import Optional

import websockets


class DataCollector:
    """시세 데이터를 수집하는 모듈.

    외부 거래소나 데이터 소스에서 시세 정보를 받아 Redis 채널로 전달합니다.

    예시:
        >>> collector = DataCollector()
        >>> await collector.run()
    """

    def __init__(self, url: str = "ws://localhost:8765", *, redis_client=None, channel: str = "ticks") -> None:
        self.url = url
        self.redis = redis_client
        self.channel = channel

    async def run(self, limit: Optional[int] = None) -> None:
        """WebSocket에서 데이터를 읽어 Redis 채널로 발행한다."""

        if self.redis is None:
            import redis.asyncio as redis

            self.redis = redis.from_url("redis://localhost")

        received = 0
        while True:
            try:
                async with websockets.connect(self.url) as ws:
                    async for message in ws:
                        await self.redis.publish(self.channel, message)
                        received += 1
                        if limit and received >= limit:
                            return
            except websockets.WebSocketException:
                await asyncio.sleep(1)

