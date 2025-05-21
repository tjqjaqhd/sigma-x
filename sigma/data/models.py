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



class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    side = Column(String)
    qty = Column(Float)
    price = Column(Float)
    status = Column(String)


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    qty = Column(Float)
    avg_price = Column(Float)


class StrategyParam(Base):
    __tablename__ = "strategy_param"

    name = Column(String, primary_key=True)
    value = Column(String)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    level = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime)


__all__ = ["MarketData", "SystemConfig", "Order", "Position", "StrategyParam", "Alert"]
