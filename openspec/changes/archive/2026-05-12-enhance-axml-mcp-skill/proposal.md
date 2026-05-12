## Why

The current AXML MCP skill is too generic for the way this repository actually uses assurance-case tooling. The new guidance needs to be stricter about MCP-first structural work, discovery-first tool use, active-path handoff, and validation-oriented write-back so agents behave consistently across traversal, mutation, defeater creation, and reconstruction workflows.

## What Changes

- Replace the existing AXML MCP skill text with a more operational skill tailored to this repository's `asce_tools` server.
- Make MCP the default semantic interface for assurance-case structure, with raw `.axml` edits reserved for narrow non-semantic exceptions.
- Add explicit guidance for discovery, traversal, shared context, mutation, defeater creation, evidence-provider lookup, and reconstruction.
- Clarify the current repository capabilities and the distinction between current server surface and broader MCP deployments.
- Update repository guidance so agents know where the skill lives and when to load it.
- **BREAKING**: agents are expected to follow the new MCP-first rule for structural assurance-case edits rather than treating raw `.axml` updates as equivalent.

## Capabilities

### New Capabilities
- `axml-mcp-skill`: A repository-specific skill for using the local `asce_tools` AXML MCP server as the semantic interface for assurance-case work.

### Modified Capabilities
- 

## Impact

- `.opencode/skills/axml-mcp-skill/SKILL.md` will be replaced with the enhanced skill text.
- Repository docs and agent guidance should point at the skill and describe its MCP-first operating model.
- The skill will need to stay aligned with the current `asce_tools` tool surface and permissions model.
- No MCP server API change is required by this proposal, but the guidance will assume the existing parser, traversal, context, evidence-provider, defeater, and write-back tools are available.
