from sigma.core.strategy_selector import StrategySelector


class DummyManager:
    async def initialize(self):
        pass


def test_strategy_selector_init():
    sel = StrategySelector(DummyManager())
    assert hasattr(sel, "current_strategy")
