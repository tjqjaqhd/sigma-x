"""비정상 패턴 감지 모듈.

`docs/4_development/module_specs/core/AnomalyDetector_Spec.md` 사양을 따른다.
"""

from __future__ import annotations

import collections
import logging
from collections import deque
from typing import Deque, Dict, Optional

from sigma.common.notification_service import NotificationService


class AnomalyDetector:
    """단순 이동평균 기반 이상 감지를 수행한다."""

    def __init__(
        self,
        window: int = 10,
        threshold: float = 2.0,
        notifier: Optional[NotificationService] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.window = window
        self.threshold = threshold
        self.logger = logger or logging.getLogger(__name__)
        self.notifier = notifier or NotificationService()
        self.history: Dict[str, Deque[float]] = collections.defaultdict(lambda: deque(maxlen=window))

    async def scan(self, metric: str, value: float, ts: float) -> Optional[Dict[str, float]]:
        series = self.history[metric]
        series.append(value)
        if len(series) < self.window:
            return None

        mean = sum(series) / len(series)
        var = sum((x - mean) ** 2 for x in series) / len(series)
        std = var**0.5
        if value > mean + self.threshold * std:
            alert = {
                "metric": metric,
                "value": value,
                "level": "warning",
                "ts": ts,
            }
            await self.notify(alert)
            return alert
        return None

    async def notify(self, alert: Dict[str, float]) -> None:
        msg = f"{alert['metric']} anomaly: {alert['value']}"
        await self.notifier.notify({"level": alert["level"], "message": msg, "ts": alert["ts"]})
