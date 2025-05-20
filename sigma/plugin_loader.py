from sigma.utils.logger import logger


def load_plugins() -> list[str]:
    """플러그인을 로드합니다 (더미 구현)."""
    plugins = ["core"]
    logger.info("플러그인 로드 완료")
    return plugins
