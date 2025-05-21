import argparse

from src.sigma.config_loader import load_env, load_db_config
from src.sigma.core.bot import TradingBot
from src.sigma.core.strategies import DummyStrategy
from src.sigma.system import initialize
from src.sigma.utils.logger import logger


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "sim"], default="live")
    args = parser.parse_args()

    load_env()
    db_conf = load_db_config()
    logger.info(f"DB config: {db_conf['url']}")
    initialize()
    bot = TradingBot(strategy=DummyStrategy(), is_simulation=args.mode != "live")
    bot.run()


if __name__ == "__main__":
    main()
