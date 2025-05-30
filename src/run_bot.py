import os
import asyncio
import logging
from typing import Optional

from .data_collector import DataCollector
from .trade_executor import TradeExecutor
from .historical_data_loader import HistoricalDataLoader
from .strategy_tester import StrategyTester
from .simulator_executor import SimulatorExecutor
from .performance_reporter import PerformanceReporter
from .exchange_client import ExchangeClient
from .simulator import Simulator

logger = logging.getLogger(__name__)

async def run_live_mode(
    redis_client=None,
    rabbitmq_client=None,
    exchange_client: Optional[ExchangeClient] = None,
) -> None:
    """실제 거래 모드로 실행합니다."""
    collector = DataCollector(redis_client=redis_client, rabbitmq_client=rabbitmq_client)
    executor = TradeExecutor(
        redis_client=redis_client,
        rabbitmq_client=rabbitmq_client,
        exchange_client=exchange_client,
    )
    
    try:
        await asyncio.gather(
            collector.run(),
            executor.run(),
        )
    except Exception as e:
        logger.error(f"Error in live mode: {e}")
        raise

async def run_sim_mode(
    redis_client=None,
    rabbitmq_client=None,
) -> None:
    """시뮬레이션 모드로 실행합니다."""
    simulator = Simulator()
    collector = DataCollector(redis_client=redis_client, rabbitmq_client=rabbitmq_client)
    executor = TradeExecutor(
        redis_client=redis_client,
        rabbitmq_client=rabbitmq_client,
        simulator=simulator,
    )
    
    try:
        await asyncio.gather(
            collector.run(),
            executor.run(),
        )
    except Exception as e:
        logger.error(f"Error in sim mode: {e}")
        raise

async def run_backtest_mode(
    params: dict,
) -> dict:
    """백테스트 모드로 실행합니다."""
    try:
        # 1. 과거 데이터 로드
        loader = HistoricalDataLoader()
        data = await loader.run(**params)
        
        # 2. 전략 테스트
        tester = StrategyTester()
        strategy_result = await tester.run(data=data, **params)
        
        # 3. 시뮬레이션 실행
        simulator = SimulatorExecutor()
        sim_result = await simulator.run(strategy_result=strategy_result, **params)
        
        # 4. 성과 리포트 생성
        reporter = PerformanceReporter()
        report = await reporter.run(sim_result=sim_result, **params)
        
        logger.info(f"Backtest completed: {report}")
        return report
        
    except Exception as e:
        logger.error(f"Error in backtest mode: {e}")
        raise

async def main() -> None:
    """MODE 환경 변수에 따라 적절한 모드로 실행합니다."""
    mode = os.getenv("MODE", "live").lower()
    
    if mode == "live":
        await run_live_mode()
    elif mode == "sim":
        await run_sim_mode()
    elif mode == "backtest":
        params = {
            "symbol": os.getenv("SIGMA_SYMBOL", "BTCUSDT"),
            "start_date": os.getenv("SIGMA_START_DATE", "2024-01-01"),
            "end_date": os.getenv("SIGMA_END_DATE", "2024-03-01"),
        }
        await run_backtest_mode(params)
    else:
        raise ValueError(f"Unknown mode: {mode}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 