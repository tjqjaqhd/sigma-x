"""SQLAlchemy ORM 모델 정의.

`docs/4_development/module_specs/common/DBModels_Spec.md` 사양을 따른다.
"""

from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """모든 ORM 모델의 베이스 클래스."""


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)
    side = Column(String(4), nullable=False)
    size = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=func.now())


class Fill(Base):
    __tablename__ = "fills"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    filled_size = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=func.now())


class StrategyResult(Base):
    __tablename__ = "strategy_results"

    id = Column(Integer, primary_key=True)
    strategy = Column(String(50), nullable=False)
    result = Column(String, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=func.now())
