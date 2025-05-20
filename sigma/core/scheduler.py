from apscheduler.schedulers.background import BackgroundScheduler
from sigma.core.bot import TradingBot


def start_bot_scheduler(
    bot: TradingBot, interval_seconds: int = 60
) -> BackgroundScheduler:
    """Start APScheduler to run the bot periodically."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(bot.run, "interval", seconds=interval_seconds)
    scheduler.start()
    return scheduler
