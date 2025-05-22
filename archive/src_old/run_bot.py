import argparse

from sigma.config_loader import load_db_config
from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy
from sigma.system import initialize
from sigma.utils.logger import logger


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "sim"], default="live")
    args = parser.parse_args()

    db_conf = load_db_config()
    logger.info(f"DB config: {db_conf['url']}")
    initialize()
    bot = TradingBot(strategy=DummyStrategy(), is_simulation=args.mode != "live")
    bot.run()


if __name__ == "__main__":
    main()
