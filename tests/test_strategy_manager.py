from sigma.core.strategy_manager import StrategyManager


def test_strategy_manager_init():
    sm = StrategyManager()
    assert hasattr(sm, "strategies")
