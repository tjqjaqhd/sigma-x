import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("SIGMA_DB_URL", "sqlite:///./sigma.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    side = Column(String, nullable=False)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True)
    profit = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db(url: str | None = None) -> Session:
    db_url = url or DATABASE_URL
    eng = create_engine(db_url)
    Base.metadata.create_all(eng)
    global SessionLocal
    SessionLocal = sessionmaker(bind=eng)
    return SessionLocal()
