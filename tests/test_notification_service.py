import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.notification_service import send_alert  # noqa: E402


@pytest.mark.asyncio
async def test_send_alert(mocker):
    async def fake_post(url, json):
        fake_post.called = True
        assert json == {"text": "hi"}
        return None

    fake_post.called = False
    mocker.patch("httpx.AsyncClient.post", side_effect=fake_post)
    await send_alert("hi", webhook_url="http://example.com")
    assert fake_post.called
