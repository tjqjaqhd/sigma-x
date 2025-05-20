import pandas as pd

from .base import BaseStrategy


class MovingAverageStrategy(BaseStrategy):
    def __init__(self, short: int = 5, long: int = 20):
        self.short = short
        self.long = long

    def generate_signal(self, data: pd.DataFrame) -> str | None:
        if len(data) < self.long:
            return None
        short_ma = data['close'].rolling(self.short).mean().iloc[-1]
        long_ma = data['close'].rolling(self.long).mean().iloc[-1]
        if short_ma > long_ma:
            return 'BUY'
        if short_ma < long_ma:
            return 'SELL'
        return None
