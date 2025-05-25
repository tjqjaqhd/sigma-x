import asyncio
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.data_collector import DataCollector


@pytest.mark.asyncio
async def test_data_collector_run(fake_redis, mocker):
    messages = ["1", "2", "3"]

    class FakeWebSocket:
        def __init__(self, msgs):
            self._msgs = msgs

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def __aiter__(self):
            async def gen():
                for m in self._msgs:
                    yield m

            return gen()

    mocker.patch("websockets.connect", return_value=FakeWebSocket(messages))

    collector = DataCollector(redis_client=fake_redis)
    await collector.run(limit=len(messages))

    assert fake_redis.channels["ticks"] == messages
