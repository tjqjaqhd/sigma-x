import pytest
from sigma.core.order_executor import OrderExecutor


@pytest.mark.asyncio
async def test_execute():
    oe = OrderExecutor()
    order = {"size": 1, "price": 100}
    result = await oe.execute(order)
    assert "order_id" in result
    assert result["filled_size"] == 1
    assert result["price"] == 100
