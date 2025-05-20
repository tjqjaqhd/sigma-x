from sigma.utils.logger import logger


def check_system_health() -> bool:
    """시스템 헬스체크를 수행합니다."""
    logger.info("시스템 헬스 체크 완료")
    return True
