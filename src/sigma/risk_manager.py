"""RiskManager 모듈.

주문 초안에 대한 기본적인 리스크 검증을 수행한다. 자세한 사양은
``docs/4_development/module_specs`` 참조.
"""

from __future__ import annotations

import logging
from typing import Any, Dict


class RiskManager:
    """주문 검증 로직을 단순화하여 구현."""

    def __init__(self, balance: float = 0.0, max_size: float = 1.0, logger=None) -> None:
        self.balance = balance
        self.max_size = max_size
        self.logger = logger or logging.getLogger(__name__)

    async def validate_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """주문 파라미터와 잔고를 체크해 결과를 반환한다."""
        size = float(order.get("size", 0))
        price = float(order.get("price", 0))
        if size <= 0 or price <= 0:
            return {"valid": False, "reason": "잘못된 주문 값"}
        if size > self.max_size:
            return {"valid": False, "reason": "수량 한도 초과"}
        cost = size * price
        if cost > self.balance:
            return {"valid": False, "reason": "잔고 부족"}

        self.balance -= cost
        return {"valid": True}

    def record_rejection(self, reason: str) -> None:
        self.logger.info("주문 거부 사유: %s", reason)
