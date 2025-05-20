from sigma.data.collector import DataCollector
from .strategies import BaseStrategy
from .execution import OrderExecutor


class TradingBot:
    def __init__(
        self,
        strategy: BaseStrategy,
        collector: DataCollector | None = None,
        is_simulation: bool = True,
    ) -> None:
        self.strategy = strategy
        self.collector = collector or DataCollector()
        self.executor = OrderExecutor(is_simulation=is_simulation)

    def run(self, iterations: int = 1) -> None:
        """시장 데이터를 수집하고 전략을 실행합니다."""
        for _ in range(iterations):
            data = self.collector.fetch_market_data()
            for signal in self.strategy.generate_signals(data):
                self.execute_order(signal)

    def execute_order(self, signal: str) -> None:
        self.executor.execute(signal)
