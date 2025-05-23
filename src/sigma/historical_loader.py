"""과거 시장 데이터 로더."""

from __future__ import annotations

import asyncio
import csv
import logging
from typing import Dict, List


class HistoricalLoader:
    """CSV 파일을 읽어 Redis 채널로 재생한다."""

    def __init__(self, redis, logger=None) -> None:
        self.redis = redis
        self.logger = logger or logging.getLogger(__name__)

    async def load_csv(self, path: str) -> List[Dict[str, str]]:
        with open(path) as fp:
            return list(csv.DictReader(fp))

    async def replay(self, path: str, speed: float = 1.0) -> None:
        ticks = await self.load_csv(path)
        prev_ts = None
        for row in ticks:
            ts = float(row.get("ts", 0))
            if prev_ts is not None:
                await asyncio.sleep(max(0, (ts - prev_ts) / speed))
            prev_ts = ts
            await self.redis.publish("market.tick", row)
            self.logger.debug("tick 재생: %s", row)

