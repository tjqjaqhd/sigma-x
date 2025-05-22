import logging
from sigma.core.execution import OrderExecutor


def test_executor_simulation(caplog):
    executor = OrderExecutor(is_simulation=True)
    with caplog.at_level(logging.INFO):
        executor.execute("BUY")
    assert "[SIM] execute BUY" in caplog.text


def test_executor_real(caplog):
    executor = OrderExecutor(is_simulation=False)
    with caplog.at_level(logging.INFO):
        executor.execute("BUY")
    assert "execute BUY" in caplog.text
