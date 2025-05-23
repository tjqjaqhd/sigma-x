"""시스템 메트릭 수집 모듈.

``docs/4_development/module_specs/common/Metrics_Spec.md`` 의 사양을 따른다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional

import aiohttp
from sigma.common.logging_service import get_logger


class MetricsTracker:
    """메트릭을 수집해 주기적으로 푸시한다."""

    def __init__(
        self,
        pushgateway_url: str,
        interval: float = 1.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.pushgateway_url = pushgateway_url
        self.interval = interval
        self.logger = logger or get_logger(__name__)
        self.metrics: Dict[str, float] = {}
        self._task: Optional[asyncio.Task] = None

    def collect_pnl(self, value: float) -> None:
        self.metrics["profit_total"] = self.metrics.get("profit_total", 0.0) + value

    def collect_latency(self, value: float) -> None:
        self.metrics["latency_total"] = self.metrics.get("latency_total", 0.0) + value

    async def push_metrics(self) -> None:
        """모은 메트릭을 Pushgateway로 전송한다."""
        if not self.metrics:
            return
        body = "\n".join(f"{k} {v}" for k, v in self.metrics.items()) + "\n"
        url = f"{self.pushgateway_url}/metrics/job/sigma"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=body) as resp:
                    resp.raise_for_status()
            self.logger.debug("메트릭 전송 성공: %s", body)
        except Exception as exc:  # pragma: no cover - 네트워크 오류
            self.logger.warning("메트릭 전송 실패: %s", exc)
        finally:
            self.metrics.clear()

    async def _loop(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self.push_metrics()

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:  # pragma: no cover - 종료 처리
                pass
            self._task = None
