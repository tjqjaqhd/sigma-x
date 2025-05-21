import argparse
from src.sigma.core.bot import TradingBot
from src.sigma.core.strategies import DummyStrategy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", default="dummy")
    parser.parse_args()
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
