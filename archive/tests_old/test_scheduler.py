import time
from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy
from sigma.core.scheduler import start_bot_scheduler


def test_start_bot_scheduler():
    bot = TradingBot(strategy=DummyStrategy())
    scheduler = start_bot_scheduler(bot, interval_seconds=0.01)
    time.sleep(0.03)
    scheduler.shutdown()
    assert hasattr(scheduler, "shutdown")
