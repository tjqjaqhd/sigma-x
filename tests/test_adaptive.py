from sqlalchemy import create_engine

from sigma.core.adaptive import ParamAdjuster, RegimeDetector
from sigma.db import database
from sigma.db.database import Base, SessionLocal
from sigma.data.models import StrategyParam


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    database.echo_engine = engine
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_param_adjuster_updates():
    setup_db()
    adjuster = ParamAdjuster()
    adjuster.update_param("alpha", "1")
    session = SessionLocal()
    assert session.get(StrategyParam, "alpha").value == "1"
    session.close()


def test_regime_detector():
    detector = RegimeDetector()
    assert detector.detect({"price": 10}) == "bull"
    assert detector.detect({"price": -1}) == "bear"
