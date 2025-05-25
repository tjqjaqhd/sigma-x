import asyncio
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) in sys.path:
    sys.path.remove(str(SRC_DIR))  # Remove SRC_DIR to avoid conflicts with other modules during resolution.
sys.path.insert(0, str(ROOT_DIR))  # Prioritize ROOT_DIR for module resolution to ensure local imports are used first.
sys.path.append(str(SRC_DIR))  # Add SRC_DIR back to allow access to source files, but with lower priority.

import fakeredis.aioredis

from src.redis import Redis


@pytest.mark.asyncio
async def test_redis_basic():
    fake = fakeredis.aioredis.FakeRedis()
    store = Redis()
    store.client = fake

    await store.set("foo", "bar")
    assert await store.get("foo") == "bar"

    messages = []

    async def reader():
        async for msg in store.subscribe("chan"):
            messages.append(msg)
            if len(messages) >= 2:
                break

    task = asyncio.create_task(reader())
    await asyncio.sleep(0.1)
    await store.publish("chan", "1")
    await store.publish("chan", "2")
    await task

    assert messages == ["1", "2"]
