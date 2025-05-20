from datetime import datetime
import requests

from sqlalchemy.orm import Session

from ..models import Price
from ..database import SessionLocal


class DataCollector:
    """외부 거래소로부터 시세를 수집해 데이터베이스에 저장"""

    def __init__(self, db: Session | None = None):
        self.db = db or SessionLocal()

    def fetch_price(self, symbol: str = "BTCUSDT") -> dict:
        url = (
            "https://api.binance.com/api/v3/klines"
            f"?symbol={symbol}&interval=1m&limit=1"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()[0]
        return {
            "symbol": symbol,
            "time": datetime.fromtimestamp(data[0] / 1000),
            "open": float(data[1]),
            "high": float(data[2]),
            "low": float(data[3]),
            "close": float(data[4]),
            "volume": float(data[5]),
        }

    def collect(self, symbol: str = "BTCUSDT") -> None:
        record = self.fetch_price(symbol)
        self.db.add(Price(**record))
        self.db.commit()
