import asyncio
import json
import os
import aio_pika
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_test_message():
    # RabbitMQ 연결
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq:5672/"
    )
    
    async with connection:
        # 채널 생성
        channel = await connection.channel()
        
        # 테스트 메시지 생성
        test_message = {
            "type": "historical_data_load",
            "params": {
                "symbol": "BTC/USD",
                "start_date": "2024-01-01",
                "end_date": "2024-03-20"
            }
        }
        
        # 메시지 전송
        queue_name = os.getenv("SIGMA_ANALYTICS_QUEUE", "analytics_tasks")
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(test_message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name
        )
        
        logger.info("Test message sent successfully!")

if __name__ == "__main__":
    asyncio.run(send_test_message()) 