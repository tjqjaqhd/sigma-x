from sigma import TradingBot, DummyStrategy
from sigma.config_loader import load_env, load_db_config
from sigma.db.init_db import init_db
from sigma.plugin_loader import load_plugins
from sigma.metrics import init_metrics
from sigma.user_prefs import load_user_preferences
from sigma.health_check import check_system_health
from sigma.cache import init_cache
from sigma.additional_setup import configure_additional_services
from sigma.notification_service import init_notification
from sigma.api_service import init_api
from sigma.event_loop import start_event_loop
from sigma.session_manager import init_session
from sigma.logging_service import init_logging


def main() -> None:
    load_env()
    load_db_config()
    init_db()
    load_plugins()
    init_metrics()
    load_user_preferences()
    check_system_health()
    init_cache()
    configure_additional_services()
    init_notification()
    init_api()
    start_event_loop()
    init_session()
    init_logging()

    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
