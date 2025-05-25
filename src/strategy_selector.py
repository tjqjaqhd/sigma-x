from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .strategy_manager import StrategyManager
from .performance_reporter import PerformanceReporter
from .report_repository import ReportRepository


class StrategySelector:
    """전략 교체와 성과 보고를 스케줄링한다."""

    def __init__(
        self,
        *,
        manager: StrategyManager | None = None,
        reporter: PerformanceReporter | None = None,
        repository: ReportRepository | None = None,
        switch_interval: int = 86400,
        report_interval: int = 86400,
    ) -> None:
        self.manager = manager or StrategyManager()
        self.reporter = reporter or PerformanceReporter()
        self.repo = repository or ReportRepository()
        self.scheduler = AsyncIOScheduler()
        self.switch_interval = switch_interval
        self.report_interval = report_interval

    def start(self) -> None:
        self.scheduler.add_job(self._switch_job, "interval", seconds=self.switch_interval)
        self.scheduler.add_job(self._report_job, "interval", seconds=self.report_interval)
        self.scheduler.start()

    def stop(self) -> None:
        self.scheduler.shutdown(wait=False)

    async def _switch_job(self) -> None:
        available = self.manager.available()
        if not available:
            return
        current = self.manager.current().__class__.__name__.lower()
        try:
            idx = available.index(current)
        except ValueError:
            idx = -1
        next_name = available[(idx + 1) % len(available)]
        self.manager.change_strategy(next_name)

    async def _report_job(self) -> None:
        profit = self.reporter.report([])
        self.repo.save(profit)
