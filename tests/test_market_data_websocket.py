import logging
import asyncio
from sigma.common.logging_service import get_logger
from sigma.interfaces.market_data_websocket import MarketDataWebSocket, DummyRedis


def test_dummyredis_publish_logs(caplog):
    logger = get_logger("test")
    dummy = DummyRedis(logger=logger)
    with caplog.at_level(logging.DEBUG):
        asyncio.run(dummy.publish("chan", "msg"))
    assert "chan: msg" in caplog.text


def test_market_data_websocket_init():
    ws = MarketDataWebSocket("ws://localhost", ["BTC"])
    assert ws.url == "ws://localhost"
    assert ws.symbols == ["BTC"]
