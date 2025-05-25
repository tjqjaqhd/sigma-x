from __future__ import annotations

import os
import httpx


async def send_alert(message: str, *, webhook_url: str | None = None) -> None:
    """Slack 웹훅으로 알림 전송."""
    url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        raise ValueError("Slack webhook URL이 설정되지 않았습니다")

    async with httpx.AsyncClient() as client:
        await client.post(url, json={"text": message})
