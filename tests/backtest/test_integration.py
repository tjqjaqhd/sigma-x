import pytest
import asyncio
from backtest.strategy_tester import StrategyTester
from backtest.simulator_executor import SimulatorExecutor
from backtest.performance_reporter import PerformanceReporter
from run_bot import run_backtest_mode

@pytest.mark.asyncio
async def test_run_backtest_mode():
    """run_backtest_mode의 통합 테스트."""
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_balance": 100000,
    }

    # 백테스트 실행
    await run_backtest_mode(params=params)

    # 결과 검증 (예: 로그 출력, DB 저장 여부 등)
    # TODO: 실제 검증 로직 추가
