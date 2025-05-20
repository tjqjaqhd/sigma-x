import pandas as pd
from sqlalchemy.orm import Session

from ..models import Price
from ..strategies.base import BaseStrategy


def run_backtest(strategy: BaseStrategy, db: Session, symbol: str = "BTCUSDT") -> pd.DataFrame:
    prices = (
        db.query(Price)
        .filter(Price.symbol == symbol)
        .order_by(Price.time.asc())
        .all()
    )
    df = pd.DataFrame([
        {"time": p.time, "close": p.close} for p in prices
    ])
    signals = []
    for i in range(len(df)):
        signal = strategy.generate_signal(df.iloc[: i + 1])
        signals.append(signal)
    df["signal"] = signals
    return df
