from sigma.utils.logger import logger


class NotificationService:
    def __init__(self) -> None:
        self.active = True

    def send(self, message: str) -> None:
        logger.info(f"알림 전송: {message}")


def init_notification() -> NotificationService:
    logger.info("알림 서비스 초기화")
    return NotificationService()
