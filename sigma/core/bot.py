from sigma.data.collector import DataCollector
from .strategies import BaseStrategy
from .execution import OrderExecutor


class TradingBot:
    def __init__(self, strategy: BaseStrategy, collector: DataCollector | None = None, is_simulation: bool = True):
        self.strategy = strategy
        self.collector = collector or DataCollector()
        self.executor = OrderExecutor(is_simulation=is_simulation)

    def run(self) -> None:
        market_data = self.collector.fetch_market_data()
        for signal in self.strategy.generate_signals(market_data):
            self.execute_order(signal)

    def execute_order(self, signal: str) -> None:
        self.executor.execute(signal)
