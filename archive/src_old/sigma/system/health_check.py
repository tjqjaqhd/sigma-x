"""시스템 헬스 체크."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import redis

from sigma.utils.logger import logger
from sigma.db.database import echo_engine
from sigma.system.notification_service import notify


def check_system_health() -> None:
    """DB, Redis, 알림 설정을 점검합니다."""
    try:
        with echo_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("DB 연결 성공")
    except SQLAlchemyError:
        logger.error("DB 연결 실패")

    try:
        redis.Redis().ping()
        logger.info("Redis 연결 성공")
    except Exception:
        logger.error("Redis 연결 실패")

    # 알림 서비스 설정 확인 (NotificationService로 일원화)
    try:
        notify("INFO", "헬스 체크: 알림 서비스 정상 동작 확인")
        logger.info("알림 서비스 설정 확인")
    except Exception as exc:
        logger.warning(f"알림 서비스 설정 오류: {exc}")

    logger.info("시스템 헬스 체크 완료")
