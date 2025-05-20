from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy


def test_bot_benchmark(benchmark):
    bot = TradingBot(strategy=DummyStrategy())
    benchmark(bot.run)
