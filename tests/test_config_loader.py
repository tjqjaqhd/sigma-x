from sigma.common.config_loader import ConfigLoader


def test_config_loader_init():
    cl = ConfigLoader()
    assert hasattr(cl, "load")
