from sqlalchemy import create_engine

from sigma.data.models import Order
from sigma.db import database
from sigma.db.database import Base, SessionLocal


def test_model_creation():
    engine = create_engine("sqlite:///:memory:")
    database.echo_engine = engine
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    session.add(Order(symbol="BTC", side="BUY", qty=1, price=10, status="NEW"))
    session.commit()
    assert session.query(Order).count() == 1
    session.close()
