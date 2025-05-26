from __future__ import annotations

from typing import Iterable

from ..report_repository import ReportRepository


class PerformanceReporter:
    """성과 리포트를 생성하는 클래스."""

    def __init__(self, report_repository: ReportRepository):
        self.report_repository = report_repository

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
        report = {"summary": "백테스트 결과 요약", "details": orders}

        # 리포트 저장
        self.report_repository.save(report)

        return profit
