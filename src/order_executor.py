from __future__ import annotations


class OrderExecutor:
    """주문 실행을 담당한다."""

    def __init__(
        self,
        redis_client=None,
        order_key: str = "orders",
        simulator=None,
        db_session=None,
        exchange_client=None,
    ) -> None:
        self.redis = redis_client
        self.order_key = order_key
        self.simulator = simulator
        self.exchange_client = exchange_client
        self.db = db_session

    async def _save_db(self, signal: str, price: float) -> None:
        if self.db is not None:
            from .database import Order

            self.db.add(Order(side=signal, price=price))
            self.db.commit()

    async def execute(self, signal: str, price: float, **kwargs) -> None:
        if self.simulator is not None:
            await self.simulator.execute(signal, price)
        elif self.exchange_client is not None:
            symbol = kwargs.get("symbol")
            volume = kwargs.get("volume", 0)
            await self.exchange_client.place_order(signal, symbol, volume)
            await self._save_db(signal, price)
        else:
            await self._save_db(signal, price)
        if self.redis is not None:
            await self.redis.rpush(self.order_key, signal)
