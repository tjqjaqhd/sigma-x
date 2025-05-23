from sigma.common.plugin_loader import PluginLoader


def test_plugin_loader_init():
    pl = PluginLoader()
    assert hasattr(pl, "load")
