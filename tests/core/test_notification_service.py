import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.notification_service import send_alert  # noqa: E402


@pytest.mark.asyncio
async def test_send_alert(mocker):
    # Mock the AsyncClient.post method
    mock_post = AsyncMock()
    mocker.patch("httpx.AsyncClient.post", mock_post)

    # Call the function
    await send_alert("hi", webhook_url="http://example.com")

    # Assert the post method was called with the correct arguments
    mock_post.assert_called_once_with("http://example.com", json={"text": "hi"})
