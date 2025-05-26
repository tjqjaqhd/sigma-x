import os
import asyncio
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

from .historical_data_loader import HistoricalDataLoader
from .redis_client import Redis
from .rabbitmq_client import RabbitMQ

logger = logging.getLogger(__name__)

class SimReplay:
    def __init__(
        self,
        redis_client=None,
        rabbitmq_client=None,
        data_dir: str = "data",
        interval: float = 1.0,
    ):
        self.redis = redis_client
        self.rabbitmq = rabbitmq_client
        self.data_dir = data_dir
        self.interval = interval
        self.loader = HistoricalDataLoader()

    async def load_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """과거 데이터를 로드합니다."""
        params = {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
        }
        return await self.loader.run(**params)

    async def publish_tick(self, price: float, timestamp: datetime) -> None:
        """틱 데이터를 Redis/RabbitMQ에 발행합니다."""
        message = f"{price},{timestamp.isoformat()}"
        
        if self.rabbitmq is not None:
            await self.rabbitmq.publish("ticks", message)
        if self.redis is not None:
            await self.redis.publish("ticks", message)

    async def replay(self, data: pd.DataFrame) -> None:
        """데이터를 순차적으로 재생합니다."""
        for _, row in data.iterrows():
            await self.publish_tick(row["price"], row["timestamp"])
            await asyncio.sleep(self.interval)

    async def run(self) -> None:
        """시뮬레이션 재생을 실행합니다."""
        symbol = os.getenv("SIGMA_SYMBOL", "BTCUSDT")
        start_date = os.getenv("SIGMA_START_DATE", "2024-01-01")
        end_date = os.getenv("SIGMA_END_DATE", "2024-03-01")
        
        try:
            data = await self.load_data(symbol, start_date, end_date)
            logger.info(f"Loaded {len(data)} ticks for {symbol}")
            await self.replay(data)
        except Exception as e:
            logger.error(f"Error in sim replay: {e}")
            raise

async def main():
    # Redis 또는 RabbitMQ 클라이언트 초기화
    redis = Redis()
    rabbitmq = RabbitMQ()
    
    replay = SimReplay(
        redis_client=redis,
        rabbitmq_client=rabbitmq,
        interval=float(os.getenv("SIGMA_REPLAY_INTERVAL", "1.0")),
    )
    
    try:
        await replay.run()
    finally:
        await redis.close()
        await rabbitmq.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 