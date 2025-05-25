import asyncio

import pytest

from src.order_executor import OrderExecutor
from src.risk_manager import RiskManager
from src.simulator_executor import SimulatorExecutor


@pytest.mark.asyncio
async def test_risk_manager():
    rm = RiskManager(max_position=1)
    assert rm.check("BUY") is True
    rm.apply("BUY")
    assert rm.check("BUY") is False
    assert rm.check("SELL") is True
    rm.apply("SELL")
    assert rm.position == 0


@pytest.mark.asyncio
async def test_order_executor(fake_redis):
    sim = SimulatorExecutor()
    executor = OrderExecutor(redis_client=fake_redis, simulator=sim)
    await executor.execute("BUY", 10)
    assert fake_redis.lists["orders"] == ["BUY"]
    assert sim.orders[0]["side"] == "BUY"
