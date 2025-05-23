from sigma.core.simulator_executor import SimulatorExecutor


def test_simulator_executor_init():
    se = SimulatorExecutor()
    assert hasattr(se, "simulate")
