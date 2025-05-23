from sigma.core.trading_bot import TradingBot


def test_tradingbot_init():
    tb = TradingBot()
    assert hasattr(tb, "run")
