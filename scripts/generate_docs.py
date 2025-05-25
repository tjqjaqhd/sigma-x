import inspect
import importlib.util
from pathlib import Path
import sys

from scripts.utils import load_yaml


def load_docstring(module_path: Path) -> str:
    if not module_path.exists():
        return ""
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        return ""
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_path.stem] = module
    spec.loader.exec_module(module)
    # 우선 모듈 독스트링을 사용하고, 클래스가 존재하면 첫 번째 클래스 독스트링 사용
    doc = inspect.getdoc(module) or ""
    classes = [member for name, member in inspect.getmembers(module, inspect.isclass)]
    if classes:
        class_doc = inspect.getdoc(classes[0])
        if class_doc:
            doc = class_doc
    return doc or ""


def generate_component_docs(spec_path: Path, output_path: Path) -> None:
    spec = load_yaml(spec_path)

    lines = ["# 컴포넌트 설명", ""]
    for container in spec.get("containers", []):
        lines.append(f"## 컨테이너: {container['name']} - {container.get('description', '')}")
        lines.append("")
        lines.append("| 이름 | 타입 | 이미지 | 설명 |")
        lines.append("| --- | --- | --- | --- |")
        for comp in container.get("components", []):
            name = comp.get("name", "")
            ctype = comp.get("type", "")
            image = comp.get("image", "")
            module_path = Path("src") / f"{name}.py"
            doc = load_docstring(module_path)
            doc = doc.replace("\n", " ") if doc else "-"
            lines.append(f"| {name} | {ctype} | {image} | {doc} |")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown 문서 갱신: {output_path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    spec_path = root / "specs" / "sigma_system.yaml"
    docs_path = root / "docs" / "components.md"
    # 다이어그램 갱신
    diagrams_script = root / "scripts" / "generate_diagrams.py"
    if diagrams_script.exists():
        import subprocess

        subprocess.run([sys.executable, str(diagrams_script)], check=True)
    generate_component_docs(spec_path, docs_path)


if __name__ == "__main__":
    main()
