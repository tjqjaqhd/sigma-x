from datetime import datetime
import sys

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sigma.db.database import Base

print("MODELS MODULE ID:", id(sys.modules[__name__]), __name__)


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime)


class SystemConfig(Base):
    """시스템 설정을 저장하는 테이블.
    RABBIT_URL: RabbitMQ 접속 URL (예: amqp://guest:guest@localhost:5672/)
    ORDERS_QUEUE: 주문 큐 이름 (예: orders)
    """

    __tablename__ = "system_config"

    key = Column(String, primary_key=True)
    value = Column(Text)

    @classmethod
    def get(cls, key: str, default=None):
        from sigma.db.database import SessionLocal
        session = SessionLocal()
        try:
            row = session.query(cls).filter_by(key=key).first()
            if row:
                return row.value
            return default
        finally:
            session.close()


class StrategyParam(Base):
    """전략 파라미터를 저장하는 테이블."""

    __tablename__ = "strategy_param"

    name = Column(String, primary_key=True)
    value = Column(Text)


class Order(Base):
    """주문 정보를 저장하는 테이블."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    signal = Column(String)
    status = Column(String, default="PENDING")
    timestamp = Column(DateTime, default=datetime.utcnow)


class Position(Base):
    """포지션 상태를 저장하는 테이블."""

    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    amount = Column(Float)
    entry_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """알림 메시지를 저장하는 테이블."""

    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String, index=True)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


__all__ = [
    "MarketData",
    "SystemConfig",
    "StrategyParam",
    "Order",
    "Position",
    "Alert",
]
