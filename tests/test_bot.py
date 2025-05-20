# flake8: noqa

from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy


def test_bot_runs():
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()
