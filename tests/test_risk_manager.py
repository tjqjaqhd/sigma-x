import pytest
from sigma.core.risk_manager import RiskManager


@pytest.mark.asyncio
async def test_validate_order():
    rm = RiskManager(balance=1000, max_size=10)
    order = {"size": 1, "price": 100}
    result = await rm.validate_order(order)
    assert result["valid"]
    order2 = {"size": 100, "price": 100}
    result2 = await rm.validate_order(order2)
    assert not result2["valid"]
