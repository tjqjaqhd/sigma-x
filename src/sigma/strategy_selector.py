"""StrategySelector 모듈.

스케줄 기반으로 활성 전략을 교체하고 파라미터를 갱신한다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict


class StrategySelector:
    def __init__(self, manager, logger=None) -> None:
        self.manager = manager
        self.current_strategy: str | None = None
        self.logger = logger or logging.getLogger(__name__)

    async def select_strategy(self, strategy_id: str, params: Dict[str, Any]) -> None:
        """새 전략을 적용한다."""
        self.logger.info("전략 변경: %s -> %s", self.current_strategy, strategy_id)
        self.current_strategy = strategy_id
        # 파라미터 갱신 로직은 간단히 기록만 수행
        self.logger.debug("파라미터 갱신: %s", params)
        await self.manager.initialize()

    async def update_params(self, params: Dict[str, Any]) -> None:
        self.logger.debug("전략 파라미터 업데이트: %s", params)
