import os
from dotenv import load_dotenv


def load_env() -> None:
    """환경 변수 파일(.env)을 로드합니다."""
    load_dotenv()


def load_db_config() -> dict:
    """데이터베이스 설정을 딕셔너리 형태로 반환합니다."""
    load_env()
    return {"url": os.getenv("DATABASE_URL", "sqlite:///./sigma.db")}


__all__ = ["load_env", "load_db_config"]
