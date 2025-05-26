from __future__ import annotations

import asyncio
import os

from .strategy_selector import StrategySelector


class SigmaScheduler:
    """StrategySelector를 실행하는 백그라운드 스케줄러."""

    def __init__(self, interval: int = 86400) -> None:
        self.selector = StrategySelector(switch_interval=interval, report_interval=interval)

    async def run(self) -> None:
        mode = os.getenv("MODE", "live")
        if mode != "live":
            return
        self.selector.start()
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass
        finally:
            self.selector.stop()


if __name__ == "__main__":
    asyncio.run(SigmaScheduler().run())
