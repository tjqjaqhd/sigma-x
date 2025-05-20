from .bot import TradingBot
from .strategies import DummyStrategy


def main():
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()


if __name__ == "__main__":
    main()
