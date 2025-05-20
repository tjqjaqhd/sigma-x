import pandas as pd
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Price
from ..strategies.base import BaseStrategy
from ..notify import send_message


class TradingBot:
    def __init__(self, strategy: BaseStrategy, db: Session | None = None):
        self.strategy = strategy
        self.db = db or SessionLocal()

    def run_once(self, symbol: str = "BTCUSDT") -> None:
        prices = (
            self.db.query(Price)
            .filter(Price.symbol == symbol)
            .order_by(Price.time.asc())
            .all()
        )
        if not prices:
            return
        df = pd.DataFrame([
            {
                "time": p.time,
                "open": p.open,
                "high": p.high,
                "low": p.low,
                "close": p.close,
                "volume": p.volume,
            }
            for p in prices
        ])
        signal = self.strategy.generate_signal(df)
        if signal:
            self.execute_order(signal)

    def execute_order(self, signal: str) -> None:
        # 실제 주문 대신 로그와 알림만 전송
        msg = f"주문 실행: {signal}"
        print(msg)
        send_message(msg)
