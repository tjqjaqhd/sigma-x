import asyncio
import sys
from contextlib import suppress
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.strategy_selector import StrategySelector  # noqa: E402
from src.sigma_scheduler import SigmaScheduler  # noqa: E402


class DummySelector(StrategySelector):
    def __init__(self):
        self.started = False
        super().__init__(switch_interval=1, report_interval=1)

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        pass


@pytest.mark.asyncio
async def test_sigma_scheduler_run(monkeypatch):
    selector = DummySelector()
    monkeypatch.setattr("src.sigma_scheduler.StrategySelector", lambda *a, **k: selector)
    sched = SigmaScheduler(interval=1)
    task = asyncio.create_task(sched.run())
    await asyncio.sleep(0.1)
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
    assert selector.started
