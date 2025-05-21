# flake8: noqa

import pytest
from sigma.core.bot import TradingBot
from sigma.core.strategies import DummyStrategy

@pytest.mark.skip(reason="실제 Redis 서버가 없는 환경에서는 통합 테스트를 건너뜀")
def test_bot_runs():
    bot = TradingBot(strategy=DummyStrategy())
    # 실제 run()은 Redis 서버가 필요하므로, smoke test만 진행
    assert isinstance(bot, TradingBot)
