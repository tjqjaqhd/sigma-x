import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.api_server import APIServer  # noqa: E402


def test_rest_endpoints(fake_redis):
    server = APIServer(redis_client=fake_redis)
    client = TestClient(server.app)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

    fake_redis.lists["orders"] = ["BUY"]
    res = client.get("/orders")
    assert res.json() == {"orders": ["BUY"]}


def test_websocket_echo(fake_redis):
    server = APIServer(redis_client=fake_redis)
    client = TestClient(server.app)
    with client.websocket_connect("/ws") as ws:
        ws.send_text("hi")
        assert ws.receive_text() == "hi"


def test_admin_endpoints(fake_redis):
    server = APIServer(redis_client=fake_redis)
    client = TestClient(server.app)

    res = client.post("/token", json={"username": "admin", "password": "admin"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/strategies", headers=headers)
    assert res.status_code == 200
    with client.websocket_connect("/ws") as ws:
        res = client.post("/notify", params={"message": "ALERT"}, headers=headers)
        assert res.status_code == 200
        assert ws.receive_text() == "ALERT"

    res = client.get("/pnl", headers=headers)
    assert res.status_code == 200
    assert res.json() == {"pnl": 0.0}

    res = client.get("/backtests", headers=headers)
    assert res.status_code == 200


def test_expired_token(fake_redis):
    server = APIServer(redis_client=fake_redis, token_expire_seconds=-1)
    client = TestClient(server.app)

    res = client.post("/token", json={"username": "admin", "password": "admin"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/strategies", headers=headers)
    assert res.status_code == 401


def test_pnl_and_backtests(fake_redis, tmp_path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.database import Base, BacktestResult

    engine = create_engine(f"sqlite:///{tmp_path}/t.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(BacktestResult(profit=1.0))
        session.add(BacktestResult(profit=2.0))
        session.commit()

        server = APIServer(redis_client=fake_redis, db_session=session)
        client = TestClient(server.app)
        res = client.post("/token", json={"username": "admin", "password": "admin"})
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        res = client.get("/pnl", headers=headers)
        assert res.json()["pnl"] == 3.0

        res = client.get("/backtests?limit=1", headers=headers)
        assert len(res.json()["results"]) == 1
