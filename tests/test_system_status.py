import pytest
from sigma.core.system_status import SystemStatus


@pytest.mark.asyncio
async def test_report_status():
    ss = SystemStatus()
    result = await ss.report_status()
    assert "cpu" in result
    assert "memory" in result
