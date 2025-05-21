from src.sigma.core.bot import TradingBot
from src.sigma.core.strategies import DummyStrategy


def main():
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
