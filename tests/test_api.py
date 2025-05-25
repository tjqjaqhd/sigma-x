import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.api import app


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_trade_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"symbol": "BTC", "side": "BUY", "price": 1.0, "quantity": 2.0}
        resp = await ac.post("/trade", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"received": payload}


@pytest.mark.asyncio
async def test_ws_echo():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.send_text("ping")
        data = ws.receive_text()
        assert data == "ping"
