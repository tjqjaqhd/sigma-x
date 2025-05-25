#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v mmdc >/dev/null; then
  echo "mmdc (mermaid-cli) not found" >&2
  exit 1
fi
if ! command -v dot >/dev/null; then
  echo "dot (graphviz) not found" >&2
  exit 1
fi

find "$DOCS_DIR" -name '*.mmd' | while read -r file; do
  out="${file%.mmd}.svg"
  mmdc -i "$file" -o "$out" -b transparent
  echo "Generated $out"
done

find "$DOCS_DIR" \( -name '*.dot' -o -name '*.gv' \) | while read -r file; do
  out="${file%.*}.svg"
  dot -Tsvg "$file" -o "$out"
  echo "Generated $out"
done
