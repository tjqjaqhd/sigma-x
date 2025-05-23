"""TradingBot 모듈.

`TradingBot`은 실시간 틱 데이터를 받아 전략 실행부터 주문 집행까지의 전체
오케스트레이션을 담당한다. 사양은 ``docs/4_development/module_specs`` 를
참조한다.
"""

from __future__ import annotations

from typing import Any, Dict
from sigma.common.logging_service import get_logger


class TradingBot:
    """실제 거래 흐름을 제어하는 핵심 클래스."""

    def __init__(self, strategy_manager, risk_manager, executor, logger=None) -> None:
        self.strategy_manager = strategy_manager
        self.risk_manager = risk_manager
        self.executor = executor
        self.logger = logger or get_logger(__name__)

    async def process_tick(self, tick: Dict[str, Any]) -> None:
        """틱 데이터 한 건을 처리한다."""
        try:
            order_draft = await self.strategy_manager.execute(tick)
            if not order_draft:
                return

            validation = await self.risk_manager.validate_order(order_draft)
            if validation.get("valid"):
                await self.executor.execute(order_draft)
            else:
                reason = validation.get("reason", "unknown")
                self.logger.info("주문 거부: %s", reason)
        except Exception as exc:  # pragma: no cover - 예상치 못한 오류 로깅
            self.logger.exception("틱 처리 중 오류: %s", exc)

    async def run(self, tick_source) -> None:
        """비동기 틱 소스를 순회하며 주문을 처리한다."""
        async for tick in tick_source:
            await self.process_tick(tick)
