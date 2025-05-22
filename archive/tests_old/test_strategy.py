from sigma.core.strategies import DummyStrategy


def test_dummy_strategy_signals():
    strategy = DummyStrategy()
    signals = list(strategy.generate_signals({"price": 1}))
    assert signals == ["BUY", "SELL"] * 5
