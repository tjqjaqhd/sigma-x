import pytest
from sigma.core.optimization_module import OptimizationModule


@pytest.mark.asyncio
async def test_run():
    om = OptimizationModule()
    params = {"a": [1, 2], "b": [3, 4]}
    result = await om.run("strat", params)
    assert result["strategy_id"] == "strat"
    assert "best_params" in result
