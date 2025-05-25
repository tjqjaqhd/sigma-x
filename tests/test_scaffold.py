import sys
from pathlib import Path

import yaml

from scripts.scaffold import generate


def test_scaffold(tmp_path, monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = repo_root / "specs" / "example.yaml"
    with spec_path.open() as f:
        spec = yaml.safe_load(f)

    monkeypatch.chdir(tmp_path)
    generate(spec_path)

    for container in spec.get("containers", []):
        for comp in container.get("components", []):
            module_file = tmp_path / "src" / f"{comp['name']}.py"
            test_file = tmp_path / "tests" / f"test_{comp['name']}.py"
            assert module_file.exists()
            assert test_file.exists()
