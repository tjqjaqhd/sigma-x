from .strategies import BaseStrategy
from .execution import OrderExecutor


class TradingBot:
    def __init__(self, strategy: BaseStrategy, is_simulation: bool = True):
        self.strategy = strategy
        self.executor = OrderExecutor(is_simulation=is_simulation)

    def run(self) -> None:
        for signal in self.strategy.generate_signals():
            self.execute_order(signal)

    def execute_order(self, signal: str) -> None:
        self.executor.execute(signal)
