import os
from typing import AsyncIterator, Dict, Any


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

    async def run(self, **params: Dict[str, Any]) -> Dict[str, Any]:
        """과거 데이터를 로드하고 결과를 반환합니다."""
        symbol = params.get('symbol', 'BTC/USD')
        start_date = params.get('start_date', '2024-01-01')
        end_date = params.get('end_date', '2024-03-20')
        
        # 실제 구현에서는 여기서 데이터베이스나 API에서 데이터를 가져와야 합니다.
        # 현재는 간단한 예시 데이터를 생성합니다.
        import datetime
        
        # 간단한 시뮬레이션 데이터 생성
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days
        
        data = {
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'total_days': days,
            'sample_prices': [100.0 + i for i in range(min(10, days))]  # 샘플 가격 데이터
        }
        
        return data
