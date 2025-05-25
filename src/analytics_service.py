import asyncio
import json
import logging
from typing import Any, Dict

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel

from src.historical_data_loader import HistoricalDataLoader
from src.strategy_tester import StrategyTester
from src.simulator_executor import SimulatorExecutor
from src.performance_reporter import PerformanceReporter
from src.report_repository import ReportRepository

logger = logging.getLogger(__name__)

class AnalyticsWorker:
    def __init__(
        self,
        rabbitmq_url: str = "amqp://guest:guest@localhost/",
        queue_name: str = "backtest",
    ):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue = None
        self.report_repo = ReportRepository()

    async def connect(self):
        """RabbitMQ에 연결하고 큐를 설정합니다."""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True
        )

    async def process_task(self, task: Dict[str, Any]) -> None:
        """작업을 처리하고 결과를 저장합니다."""
        task_type = task.get('type')
        params = task.get('params', {})
        
        try:
            if task_type == 'historical_data_load':
                result = await HistoricalDataLoader().run(**params)
            elif task_type == 'strategy_test':
                result = await StrategyTester().run(**params)
            elif task_type == 'simulation':
                result = await SimulatorExecutor().run(**params)
            elif task_type == 'performance_report':
                result = await PerformanceReporter().run(**params)
            else:
                logger.error(f"Unknown task type: {task_type}")
                return

            report_id = self.report_repo.save_report(task_type, result)
            logger.info(f"Task {task_type} completed, report_id={report_id}")
            
        except Exception as e:
            logger.error(f"Error processing task {task_type}: {str(e)}")
            raise

    async def start(self):
        """워커를 시작하고 메시지를 처리합니다."""
        await self.connect()
        
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        task = json.loads(message.body.decode())
                        await self.process_task(task)
                    except json.JSONDecodeError:
                        logger.error("Failed to decode message body")
                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}")

    async def close(self):
        """연결을 종료합니다."""
        if self.connection:
            await self.connection.close()

async def main():
    worker = AnalyticsWorker()
    try:
        await worker.start()
    finally:
        await worker.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
