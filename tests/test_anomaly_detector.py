import pytest
from sigma.core.anomaly_detector import AnomalyDetector


class DummyNotifier:
    def __init__(self):
        self.alerts = []

    async def notify(self, alert):
        self.alerts.append(alert)


@pytest.mark.asyncio
async def test_scan_anomaly():
    notifier = DummyNotifier()
    detector = AnomalyDetector(window=3, threshold=1.0, notifier=notifier)
    # 정상값 3개 입력
    await detector.scan("latency", 1.0, 1.0)
    await detector.scan("latency", 1.1, 2.0)
    await detector.scan("latency", 1.2, 3.0)
    # 이상값 입력
    alert = await detector.scan("latency", 5.0, 4.0)
    assert alert is not None
    assert alert["metric"] == "latency"
    assert alert["level"] == "warning"
    assert notifier.alerts  # notify가 호출되어야 함
