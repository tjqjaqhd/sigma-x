import asyncio
import os
from typing import Optional


class TradeExecutor:
    """매매 로직을 실행하는 컴포넌트.

    수집된 시세 데이터를 바탕으로 이동평균 교차 전략을 수행하고 주문 결과를 Redis에 저장합니다.

    예시:
        >>> executor = TradeExecutor()
        >>> await executor.run()
    """

    def __init__(
        self,
        *,
        redis_client=None,
        channel: str | None = None,
        order_key: str | None = None,
        short_window: int | None = None,
        long_window: int | None = None,
    ) -> None:
        self.redis = redis_client
        self.channel = channel or os.getenv("SIGMA_TICK_CHANNEL", "ticks")
        self.order_key = order_key or os.getenv("SIGMA_ORDER_KEY", "orders")
        self.short_window = short_window or int(os.getenv("SIGMA_SHORT_WINDOW", "3"))
        self.long_window = long_window or int(os.getenv("SIGMA_LONG_WINDOW", "5"))
        self.prices: list[float] = []

    async def process_price(self, price: float) -> str:
        self.prices.append(price)
        if len(self.prices) > self.long_window:
            self.prices.pop(0)

        if len(self.prices) >= self.long_window:
            short_ma = sum(self.prices[-self.short_window :]) / self.short_window
            long_ma = sum(self.prices) / self.long_window
            if short_ma > long_ma:
                return "BUY"
            if short_ma < long_ma:
                return "SELL"
            return "HOLD"
        return "HOLD"

    async def run(self, limit: Optional[int] = None) -> None:
        """Redis 채널을 구독해 주문 로직을 수행한다."""

        if self.redis is None:
            import redis.asyncio as redis

            self.redis = redis.from_url("redis://localhost")

        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.channel)

        processed = 0
        try:
            async for message in pubsub.listen():
                if message.get("type") != "message":
                    continue
                price = float(message["data"])
                signal = await self.process_price(price)
                if len(self.prices) >= self.long_window:
                    await self.redis.rpush(self.order_key, signal)

                processed += 1
                if limit and processed >= limit:
                    break
        finally:
            await pubsub.unsubscribe(self.channel)


