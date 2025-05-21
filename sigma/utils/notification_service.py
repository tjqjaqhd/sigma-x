from __future__ import annotations

"""다양한 알림 채널을 통합하는 서비스."""

from sigma.utils.logger import logger
from .slack_notifier import SlackNotifier


class NotificationService:
    """알림 채널을 묶어 제공하는 클래스."""

    def __init__(self) -> None:
        self.slack = SlackNotifier()

    def notify(self, message: str, level: str = "info") -> None:
        """메시지를 로그와 함께 전송합니다."""
        log_func = logger.info if level == "info" else logger.error
        log_func(message)
        self.slack.send_message(f"[{level.upper()}] {message}")


__all__ = ["NotificationService"]
