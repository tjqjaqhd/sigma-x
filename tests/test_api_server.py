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


def test_expired_token(fake_redis):
    server = APIServer(redis_client=fake_redis, token_expire_seconds=-1)
    client = TestClient(server.app)

    res = client.post("/token", json={"username": "admin", "password": "admin"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/strategies", headers=headers)
    assert res.status_code == 401
