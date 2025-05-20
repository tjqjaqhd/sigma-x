from dotenv import load_dotenv
import os
from sigma.utils.logger import logger


def load_env() -> None:
    """환경 변수를 로드합니다."""
    load_dotenv()
    logger.info("env loaded")


def load_db_config() -> dict:
    """데이터베이스 설정을 반환합니다."""
    db_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    return {"DATABASE_URL": db_url}
