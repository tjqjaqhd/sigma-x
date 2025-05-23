"""시스템 상태 모니터링 모듈.

CPU, 메모리 사용량을 수집하여 Dashboard API 등에 제공한다. 사양은
``docs/4_development/module_specs/core/SystemStatus_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional

import psutil
from sigma.common.logging_service import get_logger


class SystemStatus:
    def __init__(self, interval: int = 5, logger: Optional[logging.Logger] = None) -> None:
        self.interval = interval
        self.logger = logger or get_logger(__name__)
        self.status: Dict[str, float] = {}
        self._task: asyncio.Task | None = None

    async def check_resources(self) -> Dict[str, float]:
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "processes": float(len(psutil.pids())),
        }

    async def report_status(self) -> Dict[str, float]:
        self.status = await self.check_resources()
        self.logger.debug("시스템 상태: %s", self.status)
        return self.status

    async def start(self) -> None:
        async def _loop() -> None:
            while True:
                await self.report_status()
                await asyncio.sleep(self.interval)

        if self._task is None:
            self._task = asyncio.create_task(_loop())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:  # pragma: no cover - 종료 처리
                pass
            self._task = None
