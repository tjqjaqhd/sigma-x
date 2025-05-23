import pytest
from sigma.common.metrics import MetricsTracker


@pytest.mark.asyncio
async def test_metrics_collect():
    tracker = MetricsTracker("http://localhost:9091")
    tracker.collect_pnl(10)
    tracker.collect_latency(0.1)
    assert tracker.metrics["profit_total"] == 10
    assert tracker.metrics["latency_total"] == 0.1
