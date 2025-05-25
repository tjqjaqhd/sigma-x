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
        rabbitmq_client=None,
        channel: str | None = None,
        queue: str | None = None,
        order_key: str | None = None,
        short_window: int | None = None,
        long_window: int | None = None,
    ) -> None:
        self.redis = redis_client
        self.rabbitmq = rabbitmq_client
        self.channel = channel or os.getenv("SIGMA_TICK_CHANNEL", "ticks")
        self.queue = queue or os.getenv("SIGMA_TICK_QUEUE", "ticks")
        self.order_key = order_key or os.getenv("SIGMA_ORDER_KEY", "orders")
        self.short_window = short_window or int(
            os.getenv("SIGMA_SHORT_WINDOW", "3")
        )  # noqa: E501
        self.long_window = long_window or int(
            os.getenv("SIGMA_LONG_WINDOW", "5")
        )  # noqa: E501
        self.prices: list[float] = []

    async def process_price(self, price: float) -> str:
        """새 가격을 처리해 매매 신호를 계산한다.

        Args:
            price (float): 최신 가격

        Returns:
            str: "BUY", "SELL", "HOLD" 중 하나

        동작 원리:
            - 가격 목록을 이동평균 계산 범위만큼 유지
            - 데이터가 충분할 때 단기·장기 평균을 계산
            - 단기 평균이 더 높으면 "BUY" 반환
            - 단기 평균이 더 낮으면 "SELL" 반환
            - 그 외에는 "HOLD" 반환
        """
        self.prices.append(price)
        if len(self.prices) > self.long_window:
            self.prices.pop(0)

        if len(self.prices) >= self.long_window:
            # fmt: off
            short_ma = sum(self.prices[-self.short_window:]) / self.short_window  # noqa: E501
            # fmt: on
            long_ma = sum(self.prices) / self.long_window
            if short_ma > long_ma:
                return "BUY"
            if short_ma < long_ma:
                return "SELL"
            return "HOLD"
        return "HOLD"

    async def run(self, limit: Optional[int] = None) -> None:
        """큐 또는 Redis 구독을 통해 주문 로직을 수행한다."""

        if self.rabbitmq is None and self.redis is None:
            import redis.asyncio as redis

            self.redis = redis.from_url("redis://localhost")

        processed = 0

        if self.rabbitmq is not None:
            async for message in self.rabbitmq.consume(self.queue):
                price = float(message)
                signal = await self.process_price(price)
                if len(self.prices) >= self.long_window:
                    await self.redis.rpush(self.order_key, signal)

                processed += 1
                if limit and processed >= limit:
                    break
        else:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(self.channel)
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
