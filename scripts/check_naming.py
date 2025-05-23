#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

SRC_ROOT = Path("src/sigma")
SPECS_ROOT = Path("docs/4_development/module_specs")


# 파일명(확장자 제거) 추출
def list_module_files(root):
    files = set()
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".py") and not f.startswith("__"):
                files.add(Path(f).stem)
    return files


def list_spec_files(root):
    files = set()
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith("_Spec.md"):
                files.add(Path(f).stem.replace("_Spec", ""))
    return files


# 클래스명 추출 (class FooBar:)
def extract_class_names(pyfile):
    names = set()
    with open(pyfile, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\s*class\s+([A-Za-z0-9_]+)\s*[:(]", line)
            if m:
                names.add(m.group(1))
    return names


def extract_spec_names(mdfile):
    names = set()
    with open(mdfile, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*\d+\s*\|\s*([A-Za-z0-9_]+)\s*\|", line)
            if m:
                names.add(m.group(1))
    return names


def main():
    code_files = list_module_files(SRC_ROOT)
    spec_files = set()
    for d in SPECS_ROOT.iterdir():
        if d.is_dir():
            spec_files |= list_spec_files(d)
    # 파일명 기준 불일치
    only_code = sorted(code_files - spec_files)
    only_spec = sorted(spec_files - code_files)
    if only_code:
        print("[코드에만 존재, 사양서 없음]:", ", ".join(only_code))
    if only_spec:
        print("[사양서에만 존재, 코드 없음]:", ", ".join(only_spec))
    # 클래스명 기준 불일치
    code_classes = set()
    for dirpath, _, filenames in os.walk(SRC_ROOT):
        for f in filenames:
            if f.endswith(".py") and not f.startswith("__"):
                code_classes |= extract_class_names(os.path.join(dirpath, f))
    spec_classes = set()
    for d in SPECS_ROOT.iterdir():
        if d.is_dir():
            for dirpath, _, filenames in os.walk(d):
                for f in filenames:
                    if f.endswith("_Spec.md"):
                        spec_classes |= extract_spec_names(os.path.join(dirpath, f))
    only_code_cls = sorted(code_classes - spec_classes)
    only_spec_cls = sorted(spec_classes - code_classes)
    if only_code_cls:
        print("[코드 클래스에만 존재, 사양서 없음]:", ", ".join(only_code_cls))
    if only_spec_cls:
        print("[사양서 클래스에만 존재, 코드 없음]:", ", ".join(only_spec_cls))
    # 불일치 있으면 실패
    if only_code or only_spec or only_code_cls or only_spec_cls:
        sys.exit(1)
    print("네이밍 일치: 코드와 사양서가 완전히 동기화됨")


if __name__ == "__main__":
    main()
