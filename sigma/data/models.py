from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from sigma.db.database import Base


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime)


class SystemConfig(Base):
    """시스템 설정을 저장하는 테이블."""

    __tablename__ = "system_config"

    key = Column(String, primary_key=True)
    value = Column(Text)


class StrategyParam(Base):
    """전략 파라미터를 저장하는 테이블."""

    __tablename__ = "strategy_param"

    name = Column(String, primary_key=True)
    value = Column(Text)


class Alert(Base):
    """알림 메시지를 저장하는 테이블."""

    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String, index=True)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


__all__ = ["MarketData", "SystemConfig", "StrategyParam", "Alert"]
