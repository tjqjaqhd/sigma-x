from sigma.core.performance_reporter import PerformanceReporter


def test_performance_reporter_init():
    pr = PerformanceReporter()
    assert hasattr(pr, "report")
