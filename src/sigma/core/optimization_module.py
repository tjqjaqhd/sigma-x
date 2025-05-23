"""OptimizationModule 모듈.

단순 그리드서치 방식으로 전략 파라미터를 탐색한다.
"""

from __future__ import annotations

import itertools
import logging
from typing import Any, Dict, Iterable


class OptimizationModule:
    def __init__(self, logger=None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    async def run(self, strategy_id: str, params: Dict[str, Iterable[Any]]) -> Dict[str, Any]:
        """파라미터 조합을 순차적으로 평가해 가장 첫 값을 반환한다."""
        combos = list(itertools.product(*params.values()))
        if not combos:
            return {"strategy_id": strategy_id, "best_params": {}}

        # 실제 백테스트 대신 첫 조합을 선택
        best = combos[0]
        best_params = dict(zip(params.keys(), best))
        self.logger.debug("선택된 파라미터: %s", best_params)
        return {"strategy_id": strategy_id, "best_params": best_params}

    async def report_best(self, result: Dict[str, Any]) -> None:
        self.logger.info("최적 파라미터: %s", result)
