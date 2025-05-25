#!/usr/bin/env python3
"""YAML 정의를 읽어 기본 모듈과 테스트 파일을 생성하는 스크립트."""

import argparse
import subprocess
from pathlib import Path

from scripts.utils import load_yaml


def snake_to_camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def create_module(name: str, description: str = "") -> Path:
    src_dir = Path("src")
    src_dir.mkdir(exist_ok=True)
    (src_dir / "__init__.py").touch(exist_ok=True)
    module_path = src_dir / f"{name}.py"
    if module_path.exists():
        return module_path

    class_name = snake_to_camel(name)
    content = (
        f"class {class_name}:\n"
        f'    """{description}"""\n\n'
        "    def run(self) -> None:\n"
        "        pass\n"
    )
    module_path.write_text(content)
    return module_path


def create_test(name: str) -> Path:
    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)
    test_path = tests_dir / f"test_{name}.py"
    if test_path.exists():
        return test_path

    class_name = snake_to_camel(name)
    content = (
        f"from src.{name} import {class_name}\n\n\n"
        f"def test_{name}_run():\n"
        f"    obj = {class_name}()\n"
        "    assert obj.run() is None\n"
    )
    test_path.write_text(content)
    return test_path


def format_files(*paths: Path) -> None:
    files = [str(p) for p in paths if p.exists()]
    if files:
        subprocess.run(["black", *files], check=False)


def generate(spec_path: Path) -> None:
    spec = load_yaml(spec_path)

    for container in spec.get("containers", []):
        for comp in container.get("components", []):
            mod = create_module(comp["name"], comp.get("description", ""))
            test = create_test(comp["name"])
            format_files(mod, test)


def main() -> None:
    parser = argparse.ArgumentParser(description="모듈 스캐폴드 생성기")
    parser.add_argument(
        "yaml_path",
        nargs="?",
        default="specs/sigma_system.yaml",
        help="YAML 경로",
    )
    args = parser.parse_args()
    generate(Path(args.yaml_path))


if __name__ == "__main__":
    main()
