import asyncio
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.trade_executor import TradeExecutor  # noqa: E402


@pytest.mark.asyncio
async def test_trade_executor_run(fake_rabbitmq, fake_redis):
    executor = TradeExecutor(
        rabbitmq_client=fake_rabbitmq,
        redis_client=fake_redis,
        short_window=2,
        long_window=3,
    )

    async def feed():
        for price in [1, 2, 3, 4]:
            await fake_rabbitmq.publish("ticks", str(price))

    task = asyncio.create_task(executor.run(limit=4))
    await asyncio.sleep(0.1)
    await feed()
    await task

    assert fake_redis.lists["orders"] == ["BUY", "BUY"]


@pytest.mark.asyncio
async def test_trade_executor_db(fake_rabbitmq, fake_redis, tmp_path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from src.database import Base, Order

    db_url = f"sqlite:///{tmp_path}/test.db"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    executor = TradeExecutor(
        rabbitmq_client=fake_rabbitmq,
        redis_client=fake_redis,
        short_window=2,
        long_window=3,
        db_session=session,
    )

    async def feed():
        for price in [1, 2, 3, 4]:
            await fake_rabbitmq.publish("ticks", str(price))

    task = asyncio.create_task(executor.run(limit=4))
    await asyncio.sleep(0.1)
    await feed()
    await task

    orders = session.query(Order).all()
    assert [o.side for o in orders] == ["BUY", "BUY"]
