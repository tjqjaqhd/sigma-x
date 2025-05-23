"""시스템 헬스 체크 모듈.

Redis와 데이터베이스 연결 상태를 주기적으로 확인한다. 사양은
``docs/4_development/module_specs/common/HealthCheck_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional


class HealthCheck:
    def __init__(
        self,
        redis=None,
        db=None,
        interval: int = 60,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.redis = redis
        self.db = db
        self.interval = interval
        self.logger = logger or logging.getLogger(__name__)
        self._running = False

    async def check_redis(self) -> Dict[str, Any]:
        try:
            if self.redis:
                await self.redis.ping()
            return {"component": "redis", "status": "ok"}
        except Exception as exc:  # pragma: no cover - 네트워크 오류
            self.logger.warning("Redis 체크 실패: %s", exc)
            return {"component": "redis", "status": "fail"}

    async def check_db(self) -> Dict[str, Any]:
        try:
            if self.db:
                await self.db.execute("SELECT 1")
            return {"component": "db", "status": "ok"}
        except Exception as exc:  # pragma: no cover - 네트워크 오류
            self.logger.warning("DB 체크 실패: %s", exc)
            return {"component": "db", "status": "fail"}

    async def run_checks(self) -> list[Dict[str, Any]]:
        return [await self.check_redis(), await self.check_db()]

    async def start(self) -> None:
        self._running = True
        while self._running:
            await self.run_checks()
            await asyncio.sleep(self.interval)

    async def stop(self) -> None:
        self._running = False
