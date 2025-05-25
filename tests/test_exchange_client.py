import re
import pytest
from aioresponses import aioresponses

from src.exchange_client import UpbitClient, BinanceFuturesClient


@pytest.mark.asyncio
async def test_upbit_place_order():
    client = UpbitClient("key", "secret", base_url="https://api.test")
    with aioresponses() as m:
        m.post("https://api.test/v1/orders", payload={"uuid": "1"})
        result = await client.place_order("buy", "KRW-BTC", 1)
        assert result["uuid"] == "1"
    await client.close()


@pytest.mark.asyncio
async def test_binance_place_order():
    client = BinanceFuturesClient("key", "secret", base_url="https://fapi.test")
    with aioresponses() as m:
        m.post(re.compile(r"https://fapi\.test/fapi/v1/order.*"), payload={"orderId": 123})
        result = await client.place_order("BUY", "BTCUSDT", 1)
        assert result["orderId"] == 123
    await client.close()
