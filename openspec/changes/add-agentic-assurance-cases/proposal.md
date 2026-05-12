## Why

OpenCode can benefit from a structured way to inspect assurance cases instead of treating `.axml` files as opaque XML. This change gives agents a token-efficient view of the case structure and a clear routing model for evaluating claims with the Helping Hand approach.

## What Changes

- Add a local MCP parser for Adelard ASCE `.axml` files that extracts nodes, annotations, and relationships into a compact semantic form.
- Build the parser on `networkx` so the evaluator can request local neighborhood context around a claim.
- Add a write-back path so the MCP server can persist targeted `.axml` edits when the workflow needs to modify a case.
- Use the repository schema definitions as the source of truth for node types, status fields, and link semantics.
- Reuse and tighten the existing primary assurance-case agent and subagent markdown files so they match the intended Helping Hand workflow.
- Normalize agent filenames where needed so the configured agent names and file names are consistent.
- Register the MCP server and agent wiring in OpenCode configuration if any remaining gaps exist.
- **BREAKING**: `.axml` files are expected to be processed through the parser tool rather than read directly as raw XML in the assurance workflow.

## Capabilities

### New Capabilities
- `assurance`: Assurance case parsing and Helping Hand claim routing for `.axml`-based CAE workflows.

### Modified Capabilities

- None.

## Impact

- New parser code under `mcp-server/`.
- Updates to existing `.opencode/agents/*.md` files and possibly filename normalization.
- Existing `opencode.json` may need minor validation or adjustment depending on the parser entrypoint.
- New dependencies on NetworkX, BeautifulSoup4, and the MCP SDK for parsing, graph queries, and tool exposure.
- Schema-aware parsing depends on the existing `schemas/ASCAD 2.0.xml` definition.
