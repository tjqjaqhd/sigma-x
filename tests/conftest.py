import os
import sys
import pytest
from sigma.db.database import Base, SessionLocal
from sqlalchemy import create_engine
import prometheus_client

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(autouse=True, scope="session")
def setup_database():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def reset_prometheus_registry():
    prometheus_client.REGISTRY = prometheus_client.CollectorRegistry()
