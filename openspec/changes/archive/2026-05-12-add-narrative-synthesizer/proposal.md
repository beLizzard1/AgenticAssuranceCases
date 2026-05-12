## Why

The repository can already parse and traverse assurance-case graphs, but it does not yet provide a human-facing narrative layer that answers the stakeholder question: "So what is this, and why should I care?" Adding a narrative synthesizer makes the same assurance data usable both as an executive briefing and as shared context for other agents.

## What Changes

- Add a new primary OpenCode agent that turns an assurance-case graph into a plain-English executive narrative.
- Add a second mode that generates a concise system context brief for downstream builder agents.
- Add MCP helpers for saving and retrieving the shared system context in memory.
- Keep the agent focused on synthesis and context generation, not graph editing.
- **BREAKING**: downstream workflows that want the synthesized system brief should use the new shared-context path rather than relying on ad hoc prompt text.

## Capabilities

### New Capabilities
- `narrative-synthesizer`: Executive-level assurance-case summaries and shared system context generation.

### Modified Capabilities

- None.

## Impact

- New `.opencode/agents/narrative-synthesizer.md` file.
- Updates to `mcp-server/asce_parser.py` to expose shared-context tools.
- Possible updates to OpenCode permissions or MCP tool naming if the new agent needs explicit access.
- No schema changes are expected.
