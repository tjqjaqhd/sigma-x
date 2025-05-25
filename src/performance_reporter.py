from __future__ import annotations

from typing import Iterable


class PerformanceReporter:
    """단순 수익률을 계산해 DB에 기록한다."""

    def __init__(self, db_session=None) -> None:
        self.db = db_session

    def calculate_profit(
        self,
        orders: Iterable[dict[str, float | str]],
    ) -> float:
        profit = 0.0
        position: float | None = None
        for order in orders:
            side = order["side"]
            price = float(order["price"])
            if side == "BUY":
                position = price
            elif side == "SELL" and position is not None:
                profit += price - position
                position = None
        return profit

    def report(self, orders: Iterable[dict[str, float | str]]) -> float:
        profit = self.calculate_profit(orders)
        if self.db is not None:
            from .database import BacktestResult

            self.db.add(BacktestResult(profit=profit))
            self.db.commit()
        return profit
