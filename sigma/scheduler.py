import time
from apscheduler.schedulers.background import BackgroundScheduler

from .data.collector import DataCollector
from .engine.bot import TradingBot
from .strategies.moving_average import MovingAverageStrategy


def start() -> None:
    collector = DataCollector()
    bot = TradingBot(strategy=MovingAverageStrategy())
    scheduler = BackgroundScheduler()
    scheduler.add_job(collector.collect, "interval", minutes=1)
    scheduler.add_job(bot.run_once, "interval", minutes=1)
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
