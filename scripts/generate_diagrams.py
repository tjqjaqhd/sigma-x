import yaml
from pathlib import Path


def main():
    spec_path = Path("specs/sigma_system.yaml")
    with spec_path.open() as f:
        spec = yaml.safe_load(f)

    container = spec.get("containers", [])[0]
    lines = ["```mermaid", "flowchart TD"]
    lines.append(f"subgraph {container['name']} ['{container['description']}']")
    for comp in container.get("components", []):
        lines.append(f"    {comp['name']}['{comp['name']} ({comp['type']})']")
    lines.append("end")

    for flow in container.get("flows", []):
        lines.append(f"    {flow['from']} -->|{flow['channel']}| {flow['to']}")
    lines.append("```")

    output_path = Path("docs/sigma_system_diagram.mmd")
    output_path.write_text("\n".join(lines))
    print(f"Mermaid diagram saved to {output_path}")


if __name__ == "__main__":
    main()
