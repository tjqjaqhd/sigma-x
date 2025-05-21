from sigma.core.adaptation import (
    RegimeDetector,
    ParamAdjuster,
    QualityAssessment,
    FeedbackMechanism,
)
from sigma.db.database import SessionLocal
from sigma.data.models import StrategyParam, Base
from sqlalchemy import create_engine
import pytest


def test_regime_detector():
    detector = RegimeDetector()
    assert detector.detect([1, 2, 3]) == "bull"
    assert detector.detect([3, 2, 1]) == "bear"
    assert detector.detect([1]) == "unknown"


def test_param_adjuster(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path/'db.sqlite'}")
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    adjuster = ParamAdjuster(SessionLocal)
    adjuster.update_parameter("alpha", "0.1")

    session = SessionLocal()
    try:
        param = session.get(StrategyParam, "alpha")
        assert param.value == "0.1"
    finally:
        session.close()


def test_quality_assessment_and_feedback():
    qa = QualityAssessment()
    fb = FeedbackMechanism()
    metric = qa.evaluate([1, -1, 3])
    fb.record(metric)
    assert metric == pytest.approx(1.0)
    assert fb.records == [metric]
