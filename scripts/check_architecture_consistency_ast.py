#!/usr/bin/env python3
import re
import os
import sys
import ast
from pathlib import Path

ARCH_PATH = Path("docs/1_architecture/SIGMA_Architecture_v1.2.md")
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

def find_py_file(component_name):
    target = component_name.lower()
    for root, _, files in os.walk(SRC_ROOT):
        for f in files:
            if f.endswith(".py") and target in f.lower():
                return os.path.join(root, f)
    return None

def calls_component(source_path, target_name):
    if not source_path or not os.path.exists(source_path):
        return False
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and target_name in node.func.id:
                    return True
                elif isinstance(node.func, ast.Attribute) and target_name in node.func.attr:
                    return True
    except Exception:
        return False
    return False

def main():
    if not ARCH_PATH.exists():
        print(f"[오류] 아키텍처 문서가 존재하지 않음: {ARCH_PATH}")
        sys.exit(1)

    edges = extract_edges_from_mermaid(ARCH_PATH)
    missing_spec = set()
    missing_code = set()
    broken_calls = []

    for a, b in edges:
        # 파일/사양서 존재 여부 확인
        for name in (a, b):
            spec_ok = any(name.lower() in f.name.lower() for d in SPEC_ROOT.iterdir() if d.is_dir() for f in d.glob("*_Spec.md"))
            code_ok = any(name.lower() in f.lower() for _, _, files in os.walk(SRC_ROOT) for f in files if f.endswith(".py"))
            if not spec_ok:
                missing_spec.add(name)
            if not code_ok:
                missing_code.add(name)

        # 코드 내부 호출 여부 검사
        a_file = find_py_file(a)
        if a_file and not calls_component(a_file, b):
            broken_calls.append((a, b))

    if missing_spec:
        print("[사양서 없음]:", ", ".join(sorted(missing_spec)))
    if missing_code:
        print("[코드 없음]:", ", ".join(sorted(missing_code)))
    if broken_calls:
        for a, b in broken_calls:
            print(f"[호출 누락] {a} --> {b} 흐름이 코드상에서 구현되지 않음")

    if not missing_spec and not missing_code and not broken_calls:
        print("✅ 아키텍처 다이어그램 ↔ 사양서 ↔ 코드 흐름 완전 일치")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
