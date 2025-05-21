"""알림 서비스."""

from datetime import datetime
from src.sigma.utils.logger import logger
from src.sigma.db.database import SessionLocal
from src.sigma.data.models import Alert
from src.sigma.config_loader import load_db_config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

config = load_db_config()

class BaseNotifier:
    async def send(self, level, msg):
        raise NotImplementedError

class SlackNotifier(BaseNotifier):
    def __init__(self):
        self.token = config.get("SLACK_TOKEN")
        self.channel = config.get("SLACK_CHANNEL")
        self.client = WebClient(token=self.token) if self.token else None

    async def send(self, level, msg):
        if not self.client or not self.channel:
            logger.warning("Slack channel not configured")
            return
        try:
            self.client.chat_postMessage(channel=self.channel, text=f"[{level}] {msg}")
        except SlackApiError as exc:
            logger.error(f"Slack API error: {exc.response['error']}")

class EmailNotifier(BaseNotifier):
    def __init__(self):
        self.smtp_host = config.get("SMTP_HOST")
        self.smtp_user = config.get("SMTP_USER")
        self.smtp_pass = config.get("SMTP_PASS")
        self.to = config.get("ALERT_EMAIL")

    async def send(self, level, msg):
        # TODO: SMTP 연동 구현
        logger.info(f"[Email] {level}: {msg} (미구현)")

_notifiers = [SlackNotifier(), EmailNotifier()]

def init_notification() -> None:
    """알림 서비스를 초기화합니다."""
    logger.info("알림 서비스 초기화")

import asyncio

def notify(level: str, message: str) -> None:
    """메시지를 DB에 저장하고 Slack으로 전송합니다. 주문 type 기록은 제거."""
    session = SessionLocal()
    try:
        alert = Alert(level=level, message=message, timestamp=datetime.utcnow())
        session.add(alert)
        session.commit()
    finally:
        session.close()
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(*(n.send(level, message) for n in _notifiers))
    )
    logger.info(f"알림 전송: {message}")

__all__ = ["init_notification", "notify"]
