"""전략 테스트 도구 모듈.

``docs/4_development/module_specs/core/StrategyTester_Spec.md`` 의 사양을 따른다.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List


class StrategyTester:
    def __init__(self, executor, repository, logger=None) -> None:
        self.executor = executor
        self.repository = repository
        self.logger = logger or logging.getLogger(__name__)

    async def execute_case(self, case: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.executor.execute_order(case)
        if hasattr(self.repository, "save_report"):
            self.repository.save_report(result)
        self.logger.debug("테스트 케이스 결과: %s", result)
        return result

    async def run_test(self, cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for case in cases:
            results.append(await self.execute_case(case))
        return results

