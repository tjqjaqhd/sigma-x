import os
from sigma.server_config import load_server_spec, DEFAULT_SPEC, ServerSpec


def test_load_server_spec_defaults():
    spec = load_server_spec()
    assert spec == DEFAULT_SPEC


def test_load_server_spec_env(monkeypatch):
    monkeypatch.setenv("SIGMA_SERVER_NAME", "custom-sigma")
    spec = load_server_spec()
    assert spec.server_name == "custom-sigma"
    assert spec.public_ip == DEFAULT_SPEC.public_ip
