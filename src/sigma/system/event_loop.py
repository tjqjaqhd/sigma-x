"""이벤트 루프."""

import asyncio
import redis.asyncio as redis_asyncio
from sigma.data.models import SystemConfig

from sigma.utils.logger import logger


async def start_event_loop(bot, price_queue, order_queue) -> None:
    """비동기 이벤트 루프를 시작합니다."""

    async def run_bot() -> None:
        redis_url = SystemConfig.get("REDIS_URL", "redis://localhost:6379/0")
        redis = redis_asyncio.from_url(redis_url)
        pubsub = redis.pubsub()
        await pubsub.subscribe("prices")
        async for msg in pubsub.listen():
            if msg["type"] != "message":
                continue
            data = msg["data"]
            for signal in bot.strategy.generate_signals(data):
                await order_queue.put(signal)
        await pubsub.unsubscribe("prices")
        await redis.close()

    logger.info("이벤트 루프 시작")
    await asyncio.gather(run_bot())
