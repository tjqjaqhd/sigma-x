"""RabbitMQ 기반 태스크 큐 모듈.

``docs/4_development/module_specs/infrastructure/RabbitMQQueue_Spec.md`` 을 따른다.
"""

from __future__ import annotations

import json
import logging
from typing import Any, AsyncGenerator, Dict, Optional

import aio_pika


class RabbitmqQueue:
    def __init__(
        self,
        queue_name: str = "sigma",
        url: str = "amqp://localhost",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.queue_name = queue_name
        self.url = url
        self.logger = logger or logging.getLogger(__name__)
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.abc.AbstractChannel] = None
        self.queue: Optional[aio_pika.Queue] = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        self.logger.debug("RabbitMQ 연결 완료: %s", self.url)

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()

    async def send(self, task: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        assert self.channel
        body = json.dumps({"task": task, "payload": payload}).encode()
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=body), routing_key=self.queue_name
        )
        self.logger.debug("큐 전송: %s", body)
        return {"task": task, "status": "queued"}

    async def listen(self) -> AsyncGenerator[Dict[str, Any], None]:
        assert self.queue
        async with self.queue.iterator() as iterator:
            async for message in iterator:
                async with message.process():
                    yield json.loads(message.body.decode())

