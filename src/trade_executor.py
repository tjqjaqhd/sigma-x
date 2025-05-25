from __future__ import annotations

import os
from typing import Optional

from .order_executor import OrderExecutor
from .risk_manager import RiskManager
from .strategy import BaseStrategy, MovingAverageStrategy


class TradeExecutor:
    """가격 스트림을 받아 전략 실행과 주문 처리를 담당한다."""

    def __init__(
        self,
        *,
        redis_client=None,
        rabbitmq_client=None,
        channel: str | None = None,
        queue: str | None = None,
        order_key: str | None = None,
        strategy: BaseStrategy | None = None,
        risk_manager: RiskManager | None = None,
        order_executor: OrderExecutor | None = None,
        short_window: int | None = None,
        long_window: int | None = None,
        db_session=None,
    ) -> None:
        self.redis = redis_client
        self.rabbitmq = rabbitmq_client
        self.channel = channel or os.getenv("SIGMA_TICK_CHANNEL", "ticks")
        self.queue = queue or os.getenv("SIGMA_TICK_QUEUE", "ticks")
        self.order_key = order_key or os.getenv("SIGMA_ORDER_KEY", "orders")
        self.short_window = short_window or int(os.getenv("SIGMA_SHORT_WINDOW", "3"))
        self.long_window = long_window or int(os.getenv("SIGMA_LONG_WINDOW", "5"))
        self.strategy = strategy or MovingAverageStrategy(self.short_window, self.long_window)
        self.risk = risk_manager or RiskManager()
        self.order_executor = order_executor or OrderExecutor(
            redis_client=self.redis,
            order_key=self.order_key,
            simulator=None,
            db_session=db_session,
        )

    async def run(self, limit: Optional[int] = None) -> None:
        """큐 또는 Redis 구독을 통해 주문 로직을 수행한다."""

        if self.rabbitmq is None and self.redis is None:
            import redis.asyncio as redis

            self.redis = redis.from_url("redis://localhost")
            self.order_executor.redis = self.redis

        processed = 0

        async def handle(price: float) -> None:
            signal = await self.strategy.process(price)
            if signal in ("BUY", "SELL") and self.risk.check(signal):
                self.risk.apply(signal)
                await self.order_executor.execute(signal, price)

        if self.rabbitmq is not None:
            async for message in self.rabbitmq.consume(self.queue):
                await handle(float(message))
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
                    await handle(float(message["data"]))
                    processed += 1
                    if limit and processed >= limit:
                        break
            finally:
                await pubsub.unsubscribe(self.channel)
