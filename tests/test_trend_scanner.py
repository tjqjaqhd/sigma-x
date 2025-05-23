from sigma.core.trend_scanner import TrendScanner


def test_trend_scanner_init():
    ts = TrendScanner()
    assert hasattr(ts, "scan")
