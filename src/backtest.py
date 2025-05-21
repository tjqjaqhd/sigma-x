import argparse
from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", default="dummy")
    parser.parse_args()
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
