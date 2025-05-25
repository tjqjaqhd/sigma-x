from pathlib import Path
import argparse

from scripts.utils import load_yaml


def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in {"-", "_"} else "_" for c in name)


def _build_lines(container: dict) -> list[str]:
    lines = [f"subgraph {container['name']} [\"{container['description']}\"]"]
    for comp in container.get("components", []):
        lines.append(f"    {comp['name']}[\"{comp['name']} ({comp['type']})\"]")
    lines.append("end")
    for flow in container.get("flows", []):
        lines.append(f"    {flow['from']} -->|{flow['channel']}| {flow['to']}")
    return lines


def generate(spec_path: Path, output: Path, split: bool = False) -> None:
    spec = load_yaml(spec_path)
    containers = spec.get("containers", [])

    lines = ["```mermaid", "flowchart TD"]
    for container in containers:
        lines.extend(_build_lines(container))
    lines.append("```")
    output.write_text("\n".join(lines))
    print(f"Mermaid diagram saved to {output}")

    if split:
        out_dir = output.parent
        for container in containers:
            sanitized_name = sanitize_filename(container["name"])
            out_file = out_dir / f"{sanitized_name}_diagram.mmd"
            sub_lines = ["```mermaid", "flowchart TD"]
            sub_lines.extend(_build_lines(container))
            sub_lines.append("```")
            out_file.write_text("\n".join(sub_lines))
            print(f"Mermaid diagram saved to {out_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mermaid 다이어그램 생성기")
    parser.add_argument(
        "--spec",
        default="specs/sigma_system.yaml",
        help="YAML 명세 파일 경로",
    )
    parser.add_argument(
        "--output",
        default="docs/sigma_system_diagram.mmd",
        help="전체 다이어그램 출력 경로",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="컨테이너별 다이어그램도 개별 파일로 저장",
    )
    args = parser.parse_args()

    generate(Path(args.spec), Path(args.output), args.split)


if __name__ == "__main__":
    main()
