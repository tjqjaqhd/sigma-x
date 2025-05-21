"""알림 서비스."""

from datetime import datetime
from sigma.utils.logger import logger
from sigma.db.database import SessionLocal
from sigma.data.models import Alert, SystemConfig

class NotifierPlugin:
    def send(self, level: str, message: str) -> None:
        raise NotImplementedError

class SlackNotifier(NotifierPlugin):
    def __init__(self):
        self.client = None
        self.channel = None
        self._initialized = False

    def _init(self):
        if self._initialized:
            return
        try:
            from slack_sdk import WebClient
        except ImportError:
            self.client = None
            return
        token = SystemConfig.get("SLACK_TOKEN")
        channel = SystemConfig.get("SLACK_CHANNEL")
        self.client = WebClient(token=token) if token else None
        self.channel = channel
        self._initialized = True

    def send(self, level: str, message: str) -> None:
        self._init()
        if not self.client or not self.channel:
            logger.warning("슬랙 알림 채널 미설정")
            return
        try:
            self.client.chat_postMessage(channel=self.channel, text=f"[{level}] {message}")
        except Exception as exc:
            logger.error(f"슬랙 알림 전송 실패: {exc}")

class EmailNotifier(NotifierPlugin):
    def __init__(self):
        self._initialized = False
        self.smtp_host = None
        self.smtp_user = None
        self.smtp_pass = None
        self.to = None

    def _init(self):
        if self._initialized:
            return
        self.smtp_host = SystemConfig.get("SMTP_HOST")
        self.smtp_user = SystemConfig.get("SMTP_USER")
        self.smtp_pass = SystemConfig.get("SMTP_PASS")
        self.to = SystemConfig.get("ALERT_EMAIL")
        self._initialized = True

    def send(self, level: str, message: str) -> None:
        self._init()
        # TODO: 실제 이메일 발송 로직 구현 예정
        logger.info(f"[이메일 알림] {level}: {message} (미구현)")

class NotificationService:
    """플러그인 방식 다채널 알림(notification) 서비스."""
    _plugins = [SlackNotifier(), EmailNotifier()]

    @classmethod
    def send(cls, level: str, message: str) -> None:
        for plugin in cls._plugins:
            plugin.send(level, message)
        logger.info(f"[알림] {level}: {message}")

def init_notification() -> None:
    """알림(notification) 서비스를 초기화합니다."""
    logger.info("알림 서비스 초기화")

def notify(level: str, message: str) -> None:
    """메시지를 DB에 저장하고 NotificationService로 전송합니다."""
    session = SessionLocal()
    try:
        alert = Alert(level=level, message=message, timestamp=datetime.utcnow())
        session.add(alert)
        session.commit()
    finally:
        session.close()
    NotificationService.send(level, message)
    logger.info(f"알림 전송: {message}")

__all__ = ["init_notification", "notify"]
