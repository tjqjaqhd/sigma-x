import os
from dotenv import load_dotenv
from typing import Any, Dict

from sigma.utils.logger import logger


def load_env() -> None:
    """환경변수를 로드합니다."""
    load_dotenv()
    logger.info("환경변수를 로드했습니다")


def load_db_config() -> Dict[str, Any]:
    """데이터베이스 설정을 반환합니다."""
    db_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    logger.info("DB 설정 로드 완료")
    return {"url": db_url}
