from sigma.data.collector import DataCollector
from .strategies import BaseStrategy
from .execution import OrderExecutor


class TradingBot:
    """단순 자동매매 봇."""

    def __init__(
        self,
        strategy: BaseStrategy,
        collector: DataCollector | None = None,
        is_simulation: bool = True,
    ) -> None:
        self.strategy = strategy
        self.collector = collector or DataCollector()
        self.executor = OrderExecutor(is_simulation=is_simulation)

    async def process_market_data(self, data: dict, order_queue) -> None:
        for signal in self.strategy.generate_signals(data):
            await order_queue.put(signal)

    def run(self, iterations: int = 1) -> None:
        """시장 데이터를 수집하고 전략을 실행합니다."""
        for _ in range(iterations):
            data = self.collector.fetch_market_data()
            self.executor.execute(next(self.strategy.generate_signals(data)))

    def execute_order(self, signal: str) -> None:
        self.executor.execute(signal)
