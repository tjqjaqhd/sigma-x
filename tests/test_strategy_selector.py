import asyncio
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.strategy_selector import StrategySelector  # noqa: E402


class DummyManager:
    def __init__(self):
        self.changed = False

    def available(self):
        return ["dummy", "alt"]

    def current(self):
        class S:
            pass

        return S()

    def change_strategy(self, name: str) -> None:
        self.changed = True


class DummyReporter:
    def __init__(self):
        self.called = False

    def report(self, orders):
        self.called = True
        return 1.0


class DummyRepo:
    def __init__(self):
        self.saved = []

    def save(self, profit: float) -> None:
        self.saved.append(profit)


@pytest.mark.asyncio
async def test_strategy_selector_schedule():
    manager = DummyManager()
    reporter = DummyReporter()
    repo = DummyRepo()
    selector = StrategySelector(
        manager=manager,
        reporter=reporter,
        repository=repo,
        switch_interval=0.1,
        report_interval=0.1,
    )
    selector.start()
    await asyncio.sleep(0.3)
    selector.stop()
    assert manager.changed
    assert reporter.called
    assert repo.saved
