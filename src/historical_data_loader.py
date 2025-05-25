import os
from typing import AsyncIterator, Dict, Any
import pandas as pd


class HistoricalDataLoader:
    """과거 시세 데이터를 순차적으로 로드하는 간단한 로더."""

    def __init__(self, source: str | None = None) -> None:
        self.source = source or os.getenv("SIGMA_HISTORY_CSV", "history.csv")

    async def load(self) -> AsyncIterator[float]:
        """CSV 파일에서 가격을 비동기적으로 읽어 들인다."""
        if not os.path.exists(self.source):
            return
        with open(self.source) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield float(line)

    async def run(self, **params: Dict[str, Any]) -> pd.DataFrame:
        """과거 데이터를 로드하고 DataFrame으로 반환합니다."""
        symbol = params.get('symbol', 'BTC/USD')
        start_date = params.get('start_date', '2024-01-01')
        end_date = params.get('end_date', '2024-03-20')
        
        # 실제 구현에서는 여기서 데이터베이스나 API에서 데이터를 가져와야 합니다.
        # 현재는 간단한 예시 데이터를 생성합니다.
        dates = pd.date_range(start=start_date, end=end_date, freq='1min')
        prices = pd.Series(range(len(dates)), index=dates)
        
        df = pd.DataFrame({
            'timestamp': dates,
            'price': prices
        })
        
        return df
