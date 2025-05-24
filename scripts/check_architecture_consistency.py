#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path

ARCH_PATH = Path("docs/1_architecture/SIGMA_Architecture_v1.4.md")
SPEC_ROOT = Path("docs/4_development/module_specs")
SRC_ROOT = Path("src/sigma")

def extract_edges_from_mermaid(md_path):
    in_mermaid = False
    edges = set()
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("```mermaid"):
                in_mermaid = True
                continue
            if line.strip().startswith("```") and in_mermaid:
                break
            if in_mermaid and "-->" in line:
                match = re.findall(r'([A-Za-z0-9_]+)/? *--+>? *([A-Za-z0-9_]+)', line)
                edges.update(match)
    return edges

def exists_spec(name):
    name = name.lower()
    for d in SPEC_ROOT.iterdir():
        if d.is_dir():
            for f in d.glob("*_Spec.md"):
                if name in f.name.lower():
                    return True
    return False

def exists_code(name):
    name = name.lower()
    for root, _, files in os.walk(SRC_ROOT):
        for f in files:
            if f.endswith(".py") and name in f.lower():
                return True
    return False

def main():
    if not ARCH_PATH.exists():
        print(f"[오류] 아키텍처 문서가 존재하지 않음: {ARCH_PATH}")
        sys.exit(1)

    edges = extract_edges_from_mermaid(ARCH_PATH)
    missing_spec = set()
    missing_code = set()

    for a, b in edges:
        for name in (a, b):
            if not exists_spec(name):
                missing_spec.add(name)
            if not exists_code(name):
                missing_code.add(name)

    if missing_spec:
        print("[사양서 없음]:", ", ".join(sorted(missing_spec)))
    if missing_code:
        print("[코드 없음]:", ", ".join(sorted(missing_code)))

    if not missing_spec and not missing_code:
        print("✅ 아키텍처 흐름 기반 사양서/코드 정합성 확인 완료.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
