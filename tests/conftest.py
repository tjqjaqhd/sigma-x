import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class FakePubSub:
    def __init__(self, redis):
        self.redis = redis
        self.queue: asyncio.Queue = asyncio.Queue()

    async def subscribe(self, channel: str) -> None:
        self.redis.subscribers.setdefault(channel, []).append(self.queue)

    async def unsubscribe(self, channel: str) -> None:
        if channel in self.redis.subscribers:
            self.redis.subscribers[channel].remove(self.queue)

    async def listen(self):
        while True:
            data = await self.queue.get()
            yield {"type": "message", "data": data}

    async def close(self) -> None:
        return None


class FakeRedis:
    def __init__(self) -> None:
        self.channels: dict[str, list[str]] = {}
        self.subscribers: dict[str, list[asyncio.Queue]] = {}
        self.lists: dict[str, list[str]] = {}
        self.hashes: dict[str, dict[str, str]] = {}

    async def publish(self, channel: str, message: str) -> None:
        self.channels.setdefault(channel, []).append(message)
        for q in self.subscribers.get(channel, []):
            await q.put(message)

    def pubsub(self) -> FakePubSub:
        return FakePubSub(self)

    async def rpush(self, key: str, value: str) -> None:
        self.lists.setdefault(key, []).append(value)

    async def lrange(self, key: str, start: int, end: int):
        end = None if end == -1 else end + 1
        return self.lists.get(key, [])[start:end]

    async def hset(self, key: str, mapping: dict[str, str]) -> None:
        self.hashes[key] = mapping

    async def hgetall(self, key: str):
        return self.hashes.get(key, {})

    async def close(self) -> None:
        return None


class FakeRabbitMQ:
    def __init__(self) -> None:
        self.queue: asyncio.Queue = asyncio.Queue()

    async def publish(self, queue: str, message: str) -> None:
        await self.queue.put(message)

    async def consume(self, queue: str):
        while True:
            msg = await self.queue.get()
            yield msg

    async def close(self) -> None:
        return None


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def fake_rabbitmq():
    return FakeRabbitMQ()
