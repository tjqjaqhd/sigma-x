from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy


def main():
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
