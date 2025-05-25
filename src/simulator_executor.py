from __future__ import annotations

from typing import Iterable


class SimulatorExecutor:
    """가상 체결을 수행하는 간단한 시뮬레이터."""

    def __init__(self, db_session=None) -> None:
        self.db = db_session
        self.orders: list[dict[str, float | str]] = []

    async def execute(self, signal: str, price: float) -> None:
        if signal in ("BUY", "SELL"):
            self.orders.append({"side": signal, "price": price})
            if self.db is not None:
                from .database import Order

                self.db.add(Order(side=signal, price=price))
                self.db.commit()

    async def run(self, stream: Iterable[tuple[str, float]]) -> None:
        for signal, price in stream:
            await self.execute(signal, price)
