from __future__ import annotations

import asyncio
import os

from .strategy_selector import StrategySelector


class SigmaScheduler:
    """스케줄링을 통해 전략을 교체하는 역할."""

    def __init__(self, strategy_manager, strategy_selector):
        self.strategy_manager = strategy_manager
        self.strategy_selector = strategy_selector

    def schedule(self, market_conditions):
        """스케줄링에 따라 전략 교체."""
        new_strategy = self.strategy_selector.select_strategy(market_conditions)
        if new_strategy:
            self.strategy_manager.set_strategy(new_strategy)


if __name__ == "__main__":
    asyncio.run(SigmaScheduler().run())
