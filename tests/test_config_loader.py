from sqlalchemy import create_engine

from sigma.config_loader import load_db_config
from sigma.db import database
from sigma.db.database import Base, SessionLocal
from sigma.data.models import SystemConfig


def test_load_db_config_defaults():
    conf = load_db_config()
    assert "url" in conf


def test_load_db_config_reads_table():
    engine = create_engine("sqlite:///:memory:")
    database.echo_engine = engine
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    session.add(SystemConfig(key="SLACK_TOKEN", value="TEST"))
    session.commit()
    session.close()
    conf = load_db_config()
    assert conf.get("SLACK_TOKEN") == "TEST"
