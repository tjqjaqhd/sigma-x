import asyncio
from dataclasses import dataclass
import json
import aio_pika
from sigma.utils.logger import logger
from sigma.data.models import Order, SystemConfig
from sigma.db.database import SessionLocal


class OrderExecutor:
    """Execute real or simulated orders."""

    def __init__(self, is_simulation: bool = True):
        self.is_simulation = is_simulation

    def execute(self, signal: str) -> None:
        session = SessionLocal()
        if self.is_simulation:
            # 시뮬레이션: 체결가=요청가, 체결시간=now
            logger.info(f"[SIM] execute {signal}")
            try:
                order = Order(signal=signal, status="EXECUTED")
                session.add(order)
                session.commit()
            finally:
                session.close()
        else:
            # 실제 거래소 API 호출(실거래)
            logger.info(f"execute {signal}")
            # TODO: 실제 거래소 API 연동 및 체결 결과 기록
            session.close()


@dataclass
class OrderEvent:
    signal: str


class OrderWorker:
    """aio_pika 기반 비동기 RabbitMQ 주문 소비 워커."""

    def __init__(self):
        self._queue = SystemConfig.get("ORDERS_QUEUE", "orders")
        self._rabbit_url = SystemConfig.get("RABBIT_URL", "amqp://guest:guest@localhost:5672/")
        self._connection = None
        self._channel = None
        self._task = None

    async def _on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            order_data = json.loads(message.body)
            event = OrderEvent(signal=order_data["signal"])
            logger.info("주문 처리: %s", event.signal)
            session = SessionLocal()
            try:
                session.add(Order(signal=event.signal, status="PENDING"))
                session.commit()
            finally:
                session.close()

    async def start(self):
        self._connection = await aio_pika.connect_robust(self._rabbit_url)
        self._channel = await self._connection.channel()
        queue = await self._channel.declare_queue(self._queue, durable=True)
        logger.info("RabbitMQ 주문 소비 시작(aio_pika 비동기)")
        self._task = asyncio.create_task(queue.consume(self._on_message))

    async def stop(self):
        if self._task:
            self._task.cancel()
        if self._connection:
            await self._connection.close()
