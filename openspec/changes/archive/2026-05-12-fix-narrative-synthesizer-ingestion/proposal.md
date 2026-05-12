## Why

The narrative synthesizer should not read `.axml` files as raw text when a schema-aware MCP parser already exists. Using the parser as the ingest path makes the summary more reliable, keeps the workflow aligned with the rest of the repo, and prevents the agent from depending on XML layout details.

## What Changes

- Update the narrative synthesizer so both modes ingest assurance cases through `parse_assurance_case` instead of direct file/text reading.
- Keep the executive-briefing mode focused on human-readable synthesis from parsed graph data.
- Keep the context-generation mode focused on producing and saving a reusable system brief from parsed graph data.
- Preserve the shared-context MCP path so downstream agents can reuse the brief.
- **BREAKING**: the narrative synthesizer is expected to use MCP-based `.axml` ingestion rather than ad hoc file reads.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `narrative-synthesizer`: Change the ingest path for both briefing and context-generation modes to use MCP parsing.

## Impact

- Updates to `.opencode/agents/narrative-synthesizer.md`.
- Potential small updates to `mcp-server/asce_parser.py` if the ingest or context tools need to be clarified.
- No schema changes are expected.
