from src.sigma.data.collector import DataCollector
from .strategies import BaseStrategy
from .execution import OrderExecutor
import pika
import json
from src.sigma.data.models import SystemConfig


class TradingBot:
    """단순 자동매매 봇. is_simulation 플래그로 실거래/시뮬레이션 모드 통합 관리."""

    def __init__(
        self,
        strategy: BaseStrategy,
        collector: DataCollector | None = None,
        is_simulation: bool = True,
    ) -> None:
        self.strategy = strategy
        self.collector = collector or DataCollector()
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

    def run(self, iterations: int = 1) -> None:
        """시장 데이터를 수집하고 전략을 실행합니다."""
        for _ in range(iterations):
            data = self.collector.fetch_market_data()
            self.executor.execute(next(self.strategy.generate_signals(data)))

    def execute_order(self, signal: str) -> None:
        self.executor.execute(signal)
