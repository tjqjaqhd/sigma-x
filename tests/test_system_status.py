import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.system_status import SystemStatus  # noqa: E402


@pytest.mark.asyncio
async def test_report_and_get(fake_redis):
    status = SystemStatus(redis_client=fake_redis)
    await status.report("api", "running")
    data = await status.get("api")
    assert data["status"] == "running"
