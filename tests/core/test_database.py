from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Order, init_db


def test_init_db(tmp_path):
    db_url = f"sqlite:///{tmp_path}/t.db"
    session = init_db(db_url)
    session.add(Order(side="BUY", price=10))
    session.commit()
    session.close()

    Session = sessionmaker(bind=create_engine(db_url))
    with Session() as new_session:
        orders = new_session.query(Order).all()
        assert len(orders) == 1
        assert orders[0].side == "BUY"
