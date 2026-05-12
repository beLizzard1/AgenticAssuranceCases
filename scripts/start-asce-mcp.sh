#!/usr/bin/env bash
set -euo pipefail

script_source="${BASH_SOURCE[0]}"
script_dir="${script_source%/*}"
if [[ "$script_dir" == "$script_source" ]]; then
  script_dir="."
fi
repo_root="${script_dir%scripts}"
repo_root="${repo_root%/}"
if [[ -z "$repo_root" ]]; then
  repo_root="."
fi
parser="$repo_root/mcp-server/asce_parser.py"

if [[ ! -f "$parser" ]]; then
  printf 'ASCE MCP startup failed: missing parser at %s\n' "$parser" >&2
  exit 1
fi

if command -v python >/dev/null 2>&1; then
  interpreter="python"
elif command -v python3 >/dev/null 2>&1; then
  interpreter="python3"
else
  printf 'ASCE MCP startup failed: neither python nor python3 is available in PATH\n' >&2
  exit 1
fi

export PYTHONUNBUFFERED=1
exec "$interpreter" "$parser"
