"""시스템 초기화 모듈."""

from sigma.utils.logger import logger, init_logger

from . import plugin_loader, metrics, user_prefs, health_check, cache, additional_setup, notification_service, api_service, event_loop, session_manager, logging_service


def initialize() -> None:
    """플로우 차트에 맞춰 시스템을 순차적으로 초기화합니다."""
    init_logger()
    plugin_loader.load_plugins()
    metrics.init_metrics()
    user_prefs.load_user_preferences()
    health_check.check_system_health()
    cache.init_cache()
    additional_setup.configure_additional_services()
    notification_service.init_notification()
    api_service.init_api()
    event_loop.start_event_loop()
    session_manager.init_session()
    logging_service.init_logging()
    logger.info("시스템 초기화 완료")

__all__ = ["initialize"]
