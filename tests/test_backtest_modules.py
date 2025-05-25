import pytest

from src.historical_data_loader import HistoricalDataLoader
from src.strategy_tester import StrategyTester
from src.simulator_executor import SimulatorExecutor
from src.performance_reporter import PerformanceReporter
from src.database import Base, Order, BacktestResult
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.mark.asyncio
async def test_historical_loader(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text("1\n2\n3\n")
    loader = HistoricalDataLoader(str(csv))
    data = [p async for p in loader.load()]
    assert data == [1.0, 2.0, 3.0]


@pytest.mark.asyncio
async def test_backtest_pipeline(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text("1\n2\n3\n4\n5\n4\n3\n2\n1\n")

    engine = create_engine(f"sqlite:///{tmp_path}/t.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    loader = HistoricalDataLoader(str(csv))
    tester = StrategyTester(short_window=2, long_window=3)
    simulator = SimulatorExecutor(db_session=session)
    reporter = PerformanceReporter(db_session=session)

    async for signal, price in tester.run(loader.load()):
        await simulator.execute(signal, price)

    profit = reporter.report(simulator.orders)

    orders = session.query(Order).all()
    result = session.query(BacktestResult).one()

    assert len(orders) == len(simulator.orders)
    assert result.profit == pytest.approx(profit)
