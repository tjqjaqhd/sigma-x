from sigma.utils.logger import logger


def load_user_preferences() -> dict:
    """사용자 선호 설정을 로드합니다."""
    prefs = {"lang": "ko"}
    logger.info("사용자 설정 로드")
    return prefs
