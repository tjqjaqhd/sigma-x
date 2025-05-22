from sigma.system import plugin_loader
from sigma.plugins.plugin_base import PluginBase


def test_load_and_run_temp_plugin(tmp_path, monkeypatch):
    pkg = tmp_path / "mypkg"
    plugin_dir = pkg / "plugins"
    plugin_dir.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (plugin_dir / "__init__.py").write_text("")
    plugin_code = """
from sigma.plugins.plugin_base import PluginBase
class TempPlugin(PluginBase):
    def __init__(self):
        self.ran = False
    def run(self, *args, **kwargs):
        self.ran = True
"""
    (plugin_dir / "temp.py").write_text(plugin_code)

    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.chdir(tmp_path)
    plugin_loader.plugins.clear()

    plugin_loader.load_plugins("mypkg/plugins")
    assert len(plugin_loader.plugins) == 1

    plugin = plugin_loader.plugins[0]
    assert isinstance(plugin, PluginBase)
    assert not getattr(plugin, "ran")

    plugin_loader.run_all_plugins()
    assert plugin.ran
