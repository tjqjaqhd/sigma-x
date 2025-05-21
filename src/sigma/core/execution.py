import asyncio
from dataclasses import dataclass
import pika
import json

from src.sigma.utils.logger import logger
from src.sigma.data.models import Order, SystemConfig
from src.sigma.db.database import SessionLocal


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
    """RabbitMQ 기반 주문 소비 워커."""

    def __init__(self):
        self._connection = None
        self._channel = None
        self._queue = SystemConfig.get("ORDERS_QUEUE", "orders")
        self._rabbit_url = SystemConfig.get("RABBIT_URL", "amqp://guest:guest@localhost:5672/")

    def _callback(self, ch, method, properties, body):
        order_data = json.loads(body)
        event = OrderEvent(signal=order_data["signal"])
        logger.info("주문 처리: %s", event.signal)
        session = SessionLocal()
        try:
            session.add(Order(signal=event.signal, status="PENDING"))
            session.commit()
        finally:
            session.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        params = pika.URLParameters(self._rabbit_url)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self._queue, on_message_callback=self._callback)
        logger.info("RabbitMQ 주문 소비 시작")
        self._channel.start_consuming()

    def stop(self):
        if self._channel:
            self._channel.stop_consuming()
        if self._connection:
            self._connection.close()
