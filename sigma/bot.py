from .database import get_db
from .strategies import BaseStrategy


class TradingBot:
    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy

    def run(self):
        for signal in self.strategy.generate_signals():
            self.execute_order(signal)

    def execute_order(self, signal):
        # TODO: 실제 주문 실행 로직 또는 시뮬레이션
        print(f"execute {signal}")
