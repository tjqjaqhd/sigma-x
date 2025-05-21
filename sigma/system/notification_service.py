"""알림 서비스."""

from datetime import datetime

from sigma.utils.logger import logger
from sigma.utils.slack_notifier import SlackNotifier
from sigma.db.database import SessionLocal
from sigma.data.models import Alert

notifier = SlackNotifier()


def init_notification() -> None:
    """알림 서비스를 초기화합니다."""
    logger.info("알림 서비스 초기화")


def notify(level: str, message: str) -> None:
    """메시지를 DB에 저장하고 Slack으로 전송합니다."""
    session = SessionLocal()
    try:
        alert = Alert(level=level, message=message, timestamp=datetime.utcnow())
        session.add(alert)
        session.commit()
    finally:
        session.close()
    notifier.send_message(f"[{level}] {message}")
    logger.info(f"알림 전송: {message}")


__all__ = ["init_notification", "notify", "notifier"]
