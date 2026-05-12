## Why

Agents need a consistent, discoverable way to use the AXML MCP server for assurance-case work instead of falling back to direct `.axml` editing. A dedicated skill gives them one authoritative operating model for graph inspection, semantic mutation, validation, and export workflows.

## What Changes

- Add a new AXML MCP skill for OpenCode that explains when to use the server and which operations belong in MCP versus direct file edits.
- Define the MCP server as the semantic source of truth for assurance-case structure, traceability, and validation tasks.
- Provide explicit guidance for discovery, inspection, mutation, validation, comparison, and export workflows.
- Encourage agents to discover available MCP tools before assuming exact tool names.
- **BREAKING**: assurance-case structural edits are expected to go through MCP-capable workflows rather than ad hoc raw XML editing.

## Capabilities

### New Capabilities
- `axml-mcp-skill`: An OpenCode skill that guides agents to use the AXML MCP server for assurance-case creation, inspection, mutation, validation, comparison, and export.

### Modified Capabilities
- 

## Impact

- New skill documentation under `.opencode/skills/`.
- Possible updates to agent guidance docs so they point at the new skill for assurance-case operations.
- README/docs may need a short reference to the skill and its intended usage.
- No changes to the MCP server API are required by this proposal itself, but the skill will assume the existing AXML tools are available.
