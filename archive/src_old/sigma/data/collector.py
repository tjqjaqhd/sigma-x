import asyncio
import websockets
import redis.asyncio as redis_asyncio
from sigma.utils.logger import logger
from sigma.data.models import SystemConfig


class DataCollector:
    """WebSocket→Redis Pub/Sub 기반 실시간 시장 데이터 수집기."""

    async def stream_prices(self):
        """WebSocket에서 실시간 시세를 받아 Redis Pub/Sub로 전파."""
        ws_url = SystemConfig.get("WS_ENDPOINT")
        redis_url = SystemConfig.get("REDIS_URL", "redis://localhost:6379/0")
        redis = redis_asyncio.from_url(redis_url)
        async with websockets.connect(ws_url) as ws:
            async for msg in ws:
                await redis.publish("prices", msg)
        await redis.close()

    def fetch_market_data(self) -> dict:
        """시장 가격 데이터를 반환합니다."""
        logger.info("시장 데이터 수집")
        # TODO: 실제 데이터 수집 로직을 구현합니다.
        return {"price": 100.0}
