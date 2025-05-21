from sigma.config_loader import load_env, load_db_config
from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy
from sigma.system import initialize
from sigma.utils.logger import logger


def main() -> None:
    load_env()
    db_conf = load_db_config()
    logger.info(f"DB config: {db_conf['url']}")
    initialize()
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
