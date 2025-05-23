import logging
import os
import sys
import asyncio
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from sigma.market_data_websocket import DummyRedis


def test_dummyredis_publish_logs(caplog):
    logger = logging.getLogger("test")
    dummy = DummyRedis(logger=logger)
    with caplog.at_level(logging.DEBUG):
        asyncio.run(dummy.publish("chan", "msg"))
    assert "chan: msg" in caplog.text
