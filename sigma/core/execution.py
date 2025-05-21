import asyncio
from dataclasses import dataclass

from sigma.utils.logger import logger
from sigma.data.models import Alert
from sigma.db.database import SessionLocal


class OrderExecutor:
    """Execute real or simulated orders."""

    def __init__(self, is_simulation: bool = True):
        self.is_simulation = is_simulation

    def execute(self, signal: str) -> None:
        if self.is_simulation:
            logger.info(f"[SIM] execute {signal}")
        else:
            # TODO: 실제 주문 로직을 구현합니다.
            logger.info(f"execute {signal}")


@dataclass
class OrderEvent:
    signal: str


class OrderWorker:
    """RabbitMQ 기반 워커를 대신하는 비동기 워커."""

    def __init__(self, queue: asyncio.Queue) -> None:
        self.queue = queue
        self._task: asyncio.Task | None = None

    async def _consume(self) -> None:
        while True:  # pragma: no cover - 무한 루프
            event: OrderEvent = await self.queue.get()
            logger.info("주문 처리: %s", event.signal)
            session = SessionLocal()
            try:
                session.add(Alert(level="INFO", message=event.signal))
                session.commit()
            finally:
                session.close()

    def start(self) -> None:
        self._task = asyncio.create_task(self._consume())

    def stop(self) -> None:
        if self._task:
            self._task.cancel()
