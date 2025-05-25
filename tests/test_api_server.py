import sys
from pathlib import Path

import pytest
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
