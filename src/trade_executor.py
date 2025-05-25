import asyncio
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
        channel: str = "ticks",
        order_key: str = "orders",
        short_window: int = 3,
        long_window: int = 5,
    ) -> None:
        self.redis = redis_client
        self.channel = channel
        self.order_key = order_key
        self.short_window = short_window
        self.long_window = long_window
        self.prices: list[float] = []

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
                self.prices.append(price)
                if len(self.prices) > self.long_window:
                    self.prices.pop(0)

                if len(self.prices) >= self.long_window:
                    short_ma = sum(self.prices[-self.short_window :]) / self.short_window
                    long_ma = sum(self.prices) / self.long_window
                    if short_ma > long_ma:
                        await self.redis.rpush(self.order_key, "BUY")
                    elif short_ma < long_ma:
                        await self.redis.rpush(self.order_key, "SELL")
                    else:
                        await self.redis.rpush(self.order_key, "HOLD")

                processed += 1
                if limit and processed >= limit:
                    break
        finally:
            await pubsub.unsubscribe(self.channel)

