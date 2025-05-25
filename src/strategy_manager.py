from __future__ import annotations

from typing import Dict

from .strategy import BaseStrategy, MovingAverageStrategy
from .plugin_loader import load_strategy, list_strategies


class StrategyManager:
    """전략 로딩과 교체를 담당한다."""

    def __init__(self, initial: str = "moving_average") -> None:
        self._strategies: Dict[str, BaseStrategy] = {}
        self._current: BaseStrategy | None = None
        self.change_strategy(initial)

    def register(self, name: str, strategy: BaseStrategy) -> None:
        self._strategies[name] = strategy

    def current(self) -> BaseStrategy:
        assert self._current is not None
        return self._current

    def available(self) -> list[str]:
        return list_strategies()

    def change_strategy(self, name: str) -> None:
        if name not in self._strategies:
            try:
                strategy = load_strategy(name)
            except Exception:
                if name == "moving_average":
                    strategy = MovingAverageStrategy()
                else:
                    raise
            self.register(name, strategy)
        self._current = self._strategies[name]
