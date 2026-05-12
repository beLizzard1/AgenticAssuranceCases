## Why

Assurance case `.axml` files are compliance artifacts, so accidental schema corruption or destructive edits can invalidate the record. This change adds hard safety boundaries and recoverability so AI-driven updates stay constrained and reversible.

## What Changes

- Deny native agent read/write access to `.axml` files through OpenCode permissions.
- Require MCP-backed mutation paths for assurance case updates.
- Add timestamped backups before any mutating `.axml` operation.
- Keep recovery artifacts local so the latest state can be restored quickly.

## Capabilities

### New Capabilities
- `safety`: Guardrails for `.axml` access, mutation safety, and pre-write recovery.

### Modified Capabilities

- None.

## Impact

- `.opencode/agents/` permission frontmatter.
- `mcp-server/` write paths for assurance case mutations.
- Local backup storage under `.backups/`.
