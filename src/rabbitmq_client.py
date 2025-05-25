try:
    import aio_pika
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    aio_pika = None


class RabbitMQ:
    """RabbitMQ 비동기 인터페이스."""

    def __init__(
        self, url: str = "amqp://guest:guest@localhost/", queue: str = "ticks"
    ) -> None:
        self.url = url
        self.queue_name = queue
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.Channel | None = None
        self.queue: aio_pika.Queue | None = None

    async def __aenter__(self) -> "RabbitMQ":
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def _connect(self) -> None:
        if aio_pika is None:
            raise RuntimeError("aio_pika is not installed")
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            self.queue = await self.channel.declare_queue(
                self.queue_name, durable=False
            )

    async def publish(self, queue: str, message: str) -> None:
        await self._connect()
        assert self.channel is not None
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()), routing_key=queue
        )

    async def consume(self, queue: str):
        await self._connect()
        assert self.queue is not None
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    yield message.body.decode()

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.queue = None
