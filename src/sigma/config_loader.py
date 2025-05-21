import os
from sqlalchemy.orm import Session

from src.sigma.db.database import SessionLocal
from src.sigma.data.models import SystemConfig
from src.sigma.utils.logger import logger


def load_db_config() -> dict:
    """시스템 설정을 DB에서 읽어 딕셔너리로 반환합니다. DB URL만 환경변수 허용."""
    db_url = os.getenv("DATABASE_URL", "sqlite:///./sigma.db")
    config: dict[str, str] = {"url": db_url}
    session: Session = SessionLocal()
    try:
        rows = session.query(SystemConfig).all()
        for row in rows:
            config[row.key] = row.value
    except Exception as exc:  # pragma: no cover - DB 오류 로깅
        logger.warning(f"설정 로드 실패: {exc}")
    finally:
        session.close()
    return config


__all__ = ["load_db_config"]
