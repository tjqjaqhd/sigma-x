# flake8: noqa
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # noqa: E402

from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy


def test_bot_runs():
    bot = TradingBot(strategy=DummyStrategy())
    bot.run()
