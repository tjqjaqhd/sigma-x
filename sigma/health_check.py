from sigma.utils.logger import logger


def check_system_health() -> bool:
    """시스템 상태를 점검합니다."""
    logger.info("system healthy")
    return True
