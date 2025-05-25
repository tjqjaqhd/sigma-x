import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.strategy_manager import StrategyManager  # noqa: E402
from src.strategy import BaseStrategy  # noqa: E402


class DummyStrategy(BaseStrategy):
    async def process(self, price: float) -> str:
        return "HOLD"


def test_register_and_change():
    manager = StrategyManager()
    manager.register("dummy", DummyStrategy())
    manager.change_strategy("dummy")
    assert isinstance(manager.current(), DummyStrategy)
