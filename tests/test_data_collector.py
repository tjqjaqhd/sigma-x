import asyncio
import sys
from pathlib import Path

import pytest
import websockets

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.data_collector import DataCollector


@pytest.mark.asyncio
async def test_data_collector_run(fake_redis):
    messages = ["1", "2", "3"]

    async def handler(ws):
        for msg in messages:
            await ws.send(msg)
        await ws.close()

    server = await websockets.serve(handler, "localhost", 8765)
    async with server:
        collector = DataCollector(url="ws://localhost:8765", redis_client=fake_redis)
        await collector.run(limit=len(messages))

    assert fake_redis.channels["ticks"] == messages
