from datetime import datetime

from sqlalchemy import create_engine

from sigma.data.models import Base, Alert
from sigma.db import database
from sigma.db.database import SessionLocal
from sigma.system import notification_service


def test_notify_records_alert(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path/'db.sqlite'}")
    database.echo_engine = engine
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    sent = []

    class DummySlack:
        def send_message(self, text: str) -> None:
            sent.append(text)

    monkeypatch.setattr(notification_service, "notifier", DummySlack())

    notification_service.notify("INFO", "hello")

    session = SessionLocal()
    try:
        alert = session.query(Alert).first()
        assert alert.message == "hello"
        assert alert.level == "INFO"
        assert isinstance(alert.timestamp, datetime)
    finally:
        session.close()

    assert sent == ["[INFO] hello"]
