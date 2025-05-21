"""알림 서비스."""

from sigma.utils.logger import logger
from sigma.utils.notification_service import NotificationService

service: NotificationService | None = None


def init_notification() -> NotificationService:
    """알림 서비스를 초기화합니다."""
    global service
    service = NotificationService()
    logger.info("알림 서비스 초기화")
    return service
