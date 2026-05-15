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

server_dir="$repo_root/extern/MITREThreatGraph"
cli_module="$server_dir/src/mitremcp/cli.py"

if [[ ! -d "$server_dir" ]]; then
  printf 'MITREThreatGraph MCP startup failed: missing submodule at %s\n' "$server_dir" >&2
  exit 1
fi

if [[ ! -f "$cli_module" ]]; then
  printf 'MITREThreatGraph MCP startup failed: missing CLI module at %s\n' "$cli_module" >&2
  exit 1
fi

if command -v python >/dev/null 2>&1; then
  interpreter="python"
elif command -v python3 >/dev/null 2>&1; then
  interpreter="python3"
else
  printf 'MITREThreatGraph MCP startup failed: neither python nor python3 is available in PATH\n' >&2
  exit 1
fi

export PYTHONUNBUFFERED=1
export PYTHONPATH="$server_dir/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$interpreter" -m mitremcp.cli --config "$server_dir/config/default.json" serve-mcp
