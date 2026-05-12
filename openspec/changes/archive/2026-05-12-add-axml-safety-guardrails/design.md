## Context

`.axml` assurance cases are compliance artifacts, so the system needs stronger guardrails than ordinary project files. The current risk is that an agent can either directly manipulate XML state through general file tools or overwrite the latest case without an immediate recovery path.

## Goals / Non-Goals

**Goals:**
- Block native agent file access to `.axml` state.
- Ensure every mutating assurance-case operation creates a local backup first.
- Keep the recovery path simple and deterministic.

**Non-Goals:**
- Git-based versioning or remote backup storage.
- Redesigning the assurance-case XML schema.
- Changing non-`.axml` file handling.

## Decisions

- Use OpenCode permission frontmatter for the denial boundary instead of relying on prompt instructions. This is stricter and reduces the chance of accidental tool use.
- Apply the same permission policy across primary agents and subagents so there is no weaker path that can bypass the restriction.
- Implement backups inside the Python MCP server, immediately before mutation logic runs. This keeps recovery co-located with the write path and avoids depending on callers to remember to back up first.
- Use timestamped `.bak` files in a hidden `.backups/` directory beside the target file. This preserves the latest state while keeping backups easy to find and clean up.

## Risks / Trade-offs

- [Permission misconfiguration could block legitimate workflows] → Keep the denial scope limited to `*.axml` and explicitly allow MCP tool access.
- [Backups may accumulate over time] → Store them in a dedicated hidden directory so cleanup can be automated later without affecting live files.
- [Backup creation can fail if the filesystem is unavailable] → Treat backup failure as a hard stop before mutation so the assurance case is never overwritten without recovery.
