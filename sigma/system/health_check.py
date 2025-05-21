"""시스템 헬스 체크."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import redis

from sigma.utils.logger import logger
from sigma.db.database import echo_engine
from sigma.utils.slack_notifier import SlackNotifier


def check_system_health() -> None:
    """DB, Redis, Slack 설정을 점검합니다."""
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

    notifier = SlackNotifier()
    if notifier.channel:
        logger.info("Slack 설정 확인")
    else:
        logger.warning("Slack 설정 없음")

    logger.info("시스템 헬스 체크 완료")
