from sigma.system.plugin_loader import load_plugins


def test_load_plugins(tmp_path, monkeypatch):
    plugins = tmp_path / "sigma" / "plugins"
    plugins.mkdir(parents=True)
    (plugins.parent / "__init__.py").write_text("")
    (plugins / "__init__.py").write_text("")
    (plugins / "p.py").write_text("name='x'")
    loaded = []

    def info(msg, *args, **kwargs):
        loaded.append(msg)

    monkeypatch.setattr("sigma.system.plugin_loader.logger.info", info)
    load_plugins(str(plugins))
    assert any("플러그인 로드" in m for m in loaded)
