"""알림 전송 모듈.

Slack 및 Telegram 알림을 지원한다. 사양은
``docs/4_development/module_specs/common/NotificationService_Spec.md`` 를 참조한다.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional


class NotificationService:
    def __init__(
        self,
        slack_token: Optional[str] = None,
        telegram_token: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.slack_token = slack_token
        self.telegram_token = telegram_token
        self.logger = logger or logging.getLogger(__name__)

    async def send_slack(self, message: str) -> Dict[str, Any]:
        self.logger.debug("Slack 전송: %s", message)
        return {"ok": True}

    async def send_telegram(self, message: str) -> Dict[str, Any]:
        self.logger.debug("Telegram 전송: %s", message)
        return {"ok": True}

    async def notify(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        level = alert.get("level", "info")
        message = alert.get("message", "")
        ts = alert.get("ts")
        full_msg = f"[{level}] {message} {ts}" if ts else f"[{level}] {message}"
        await self.send_slack(full_msg)
        await self.send_telegram(full_msg)
        return {"ok": True}

    async def alert_listener(self, queue) -> None:
        async for alert in queue:
            await self.notify(alert)
