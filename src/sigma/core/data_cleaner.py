"""데이터 정제 모듈.

DB 테이블의 오래된 기록을 삭제하여 공간을 확보한다. 사양은
``docs/4_development/module_specs/core/DataCleaner_Spec.md`` 를 따른다.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Iterable, List
from sigma.common.logging_service import get_logger


class DataCleaner:
    """간단한 정제 작업을 수행한다."""

    def __init__(self, db=None, retention_days: int = 30, logger=None) -> None:
        self.db = db
        self.retention_days = retention_days
        self.logger = logger or get_logger(__name__)

    async def clean_table(self, table: str) -> Dict[str, Any]:
        removed = 0
        if self.db:
            await asyncio.sleep(0)  # 실제 DELETE 쿼리 자리
        self.logger.debug("테이블 정리: %s -> %d rows", table, removed)
        return {"table": table, "removed": removed}

    async def run_daily(self, tables: Iterable[str]) -> List[Dict[str, Any]]:
        results = []
        for table in tables:
            results.append(await self.clean_table(table))
        return results
