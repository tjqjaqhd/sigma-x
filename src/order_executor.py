from __future__ import annotations


class OrderExecutor:
    """주문 실행을 담당한다."""

    def __init__(self, redis_client=None, order_key: str = "orders", simulator=None, db_session=None) -> None:
        self.redis = redis_client
        self.order_key = order_key
        self.simulator = simulator
        self.db = db_session

    async def _save_db(self, signal: str, price: float) -> None:
        if self.db is not None:
            from .database import Order

            self.db.add(Order(side=signal, price=price))
            self.db.commit()

    async def execute(self, signal: str, price: float) -> None:
        if self.simulator is not None:
            await self.simulator.execute(signal, price)
        else:
            await self._save_db(signal, price)
        if self.redis is not None:
            await self.redis.rpush(self.order_key, signal)
