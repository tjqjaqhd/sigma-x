from threading import Event, Thread

try:
    from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
except Exception:  # pragma: no cover - fallback when APScheduler is missing
    BackgroundScheduler = None

from src.sigma.core.bot import TradingBot


class SimpleScheduler:
    def __init__(self) -> None:
        self._thread: Thread | None = None
        self._stop_event = Event()
        self._interval = 0
        self._func: callable | None = None

    def add_job(self, func: callable, interval_seconds: int) -> None:
        self._func = func
        self._interval = interval_seconds

    def _run(self) -> None:
        assert self._func is not None
        while not self._stop_event.wait(self._interval):
            self._func()

    def start(self) -> None:
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def shutdown(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()


def start_bot_scheduler(bot: TradingBot, interval_seconds: int = 60) -> object:
    """Start scheduler to run the bot periodically."""
    if BackgroundScheduler is not None:  # pragma: no cover - APScheduler path
        scheduler = BackgroundScheduler()
        scheduler.add_job(bot.run, "interval", seconds=interval_seconds)
    else:
        scheduler = SimpleScheduler()
        scheduler.add_job(bot.run, interval_seconds)
    scheduler.start()
    return scheduler
