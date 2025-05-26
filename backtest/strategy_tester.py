from typing import AsyncIterator


class StrategyTester:
    """단순 이동평균 교차 전략을 테스트하는 컴포넌트."""

    def __init__(self, short_window: int = 3, long_window: int = 5) -> None:
        self.short_window = short_window
        self.long_window = long_window
        self.prices: list[float] = []

    async def process_price(self, price: float) -> str:
        self.prices.append(price)
        if len(self.prices) > self.long_window:
            self.prices.pop(0)
        if len(self.prices) >= self.long_window:
            short_slice = self.prices[-self.short_window :]  # noqa: E203
            short_ma = sum(short_slice) / self.short_window
            long_ma = sum(self.prices) / self.long_window
            if short_ma > long_ma:
                return "BUY"
            if short_ma < long_ma:
                return "SELL"
            return "HOLD"
        return "HOLD"

    async def run(
        self, prices: AsyncIterator[float]
    ) -> AsyncIterator[tuple[str, float]]:
        async for price in prices:
            signal = await self.process_price(price)
            yield signal, price
