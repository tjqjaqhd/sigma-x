from sigma.utils.logger import logger


def init_cache() -> dict:
    """캐시 시스템을 초기화합니다."""
    logger.info("캐시 초기화")
    return {}
