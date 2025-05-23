"""결제 처리 모듈.

사양은
``docs/4_development/module_specs/infrastructure/PaymentProcessor_Spec.md``
를 따른다.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict


class PaymentProcessor:
    def __init__(self, api_key: str, logger=None) -> None:
        self.api_key = api_key
        self.logger = logger or logging.getLogger(__name__)

    def process(self, payment: Dict) -> bool:
        # 실제 결제 처리 로직은 외부 API 연동 필요
        self.logger.info(
            "결제 처리: %s, 금액: %s",
            payment.get("user_id"),
            payment.get("amount"),
        )
        return True

    async def request_withdrawal(self, account_id: str, amount: float, currency: str) -> Dict[str, Any]:
        self.logger.debug("출금 요청 %s %s %s", account_id, amount, currency)
        return {"status": "requested"}

    async def confirm_deposit(self, account_id: str, amount: float, currency: str) -> Dict[str, Any]:
        self.logger.debug("입금 확인 %s %s %s", account_id, amount, currency)
        return {"status": "confirmed"}

    async def process_payment(self, info: Dict[str, Any]) -> Dict[str, Any]:
        order_id = info.get("order_id")
        for attempt in range(1, self.max_retry + 1):
            try:
                await self.request_withdrawal(
                    info.get("account_id"),
                    info.get("amount"),
                    info.get("currency"),
                )
                await asyncio.sleep(0)  # 외부 API 호출 자리
                result = {
                    "order_id": order_id,
                    "status": "confirmed",
                    "txid": "dummy",
                }
                self.logger.debug("결제 완료: %s", result)
                return result
            except Exception as exc:  # pragma: no cover - 네트워크 예외
                self.logger.warning(
                    "결제 시도 실패 (%d/%d): %s",
                    attempt,
                    self.max_retry,
                    exc,
                )
                if attempt >= self.max_retry:
                    raise
                await asyncio.sleep(1)

    async def verify_balance(self, account_id: str) -> float:
        self.logger.debug("잔고 확인 %s", account_id)
        return 0.0
