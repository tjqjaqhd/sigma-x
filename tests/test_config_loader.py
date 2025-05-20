from sigma.config_loader import load_db_config


def test_load_db_config_defaults():
    conf = load_db_config()
    assert "url" in conf
