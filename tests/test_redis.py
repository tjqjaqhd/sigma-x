import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))  # noqa: E402

from src.redis_client import Redis  # noqa: E402
from tests.conftest import FakeRedis


def test_redis_run():
    obj = Redis()
    assert obj.run() is None


@pytest.mark.asyncio
async def test_pubsub_flow():
    store = FakeRedis()
    pubsub = store.pubsub()
    await pubsub.subscribe("chan")
    await store.publish("chan", "msg")
    message = await anext(pubsub.listen())
    assert message["data"] == "msg"


@pytest.mark.asyncio
async def test_basic_ops(mocker, fake_redis):
    async def fake_connect(self):
        self.client = fake_redis
        return fake_redis

    mocker.patch.object(Redis, "_connect", fake_connect)
    store = Redis()
    await store.publish("chan", "hello")
    pubsub = store.pubsub()
    await pubsub.subscribe("chan")
    await store.publish("chan", "world")
    msg = await anext(pubsub.listen())
    assert msg["data"] == "world"
    await store.rpush("orders", "BUY")
    assert await store.lrange("orders", 0, -1) == ["BUY"]
