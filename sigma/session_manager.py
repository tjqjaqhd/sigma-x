from sigma.utils.logger import logger


def init_session() -> object:
    """세션을 초기화합니다."""
    logger.info("세션 초기화")
    return object()
