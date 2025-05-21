from sigma.data.collector import DataCollector
from .strategies import BaseStrategy
from .execution import OrderExecutor
import pika
import json
from sigma.data.models import SystemConfig
import asyncio
import redis.asyncio as redis_asyncio


class TradingBot:
    """실시간 Redis Pub/Sub 기반 자동매매 봇. is_simulation 플래그로 실거래/시뮬레이션 모드 통합 관리."""

    def __init__(
        self,
        strategy: BaseStrategy,
        redis_url: str | None = None,
        is_simulation: bool = True,
    ) -> None:
        self.strategy = strategy
        self.redis_url = redis_url or SystemConfig.get("REDIS_URL", "redis://localhost:6379/0")
        self.is_simulation = is_simulation
        self.executor = OrderExecutor(is_simulation=is_simulation)

    async def process_market_data(self, data: dict, order_queue=None) -> None:
        rabbit_url = SystemConfig.get("RABBIT_URL", "amqp://guest:guest@localhost:5672/")
        queue_name = SystemConfig.get("ORDERS_QUEUE", "orders")
        params = pika.URLParameters(rabbit_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        for signal in self.strategy.generate_signals(data):
            order_msg = json.dumps({"signal": signal})
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=order_msg,
                properties=pika.BasicProperties(delivery_mode=2),
            )
        connection.close()

    async def run(self) -> None:
        """Redis Pub/Sub에서 실시간 데이터를 받아 전략을 실행한다."""
        redis = redis_asyncio.from_url(self.redis_url)
        pubsub = redis.pubsub()
        await pubsub.subscribe("prices")
        async for msg in pubsub.listen():
            if msg["type"] != "message":
                continue
            data = json.loads(msg["data"])
            await self.process_market_data(data)

    def execute_order(self, signal: str) -> None:
        self.executor.execute(signal)
