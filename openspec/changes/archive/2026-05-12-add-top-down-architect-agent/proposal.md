## Why

The current assurance workflow is primarily bottom-up: claims are routed to specialist subagents once a claim is already under evaluation. A top-down orchestrator would make it easier to start from root claims, inspect what is already connected below them, and drive completion of the tree in a more systematic way.

## What Changes

- Add a new primary OpenCode agent for a top-down assurance workflow.
- Add a targeted MCP tool that returns the immediate children of a node so the agent can inspect local structure without parsing the entire file each time.
- Use the new tool to support recursive descent from root claims through claims, arguments, and evidence.
- Keep the orchestration local and aligned with the existing MCP-based assurance case parser.
- Normalize the agent prompt so it can spawn specialist subagents when a branch needs decomposition, substitution, concretization, or evidence incorporation.
- **BREAKING**: the new top-down workflow introduces a separate entrypoint for root-driven assurance traversal rather than reusing the current claim-first evaluator prompt.

## Capabilities

### New Capabilities
- `top-down-architect`: Root-driven assurance case traversal with immediate-child inspection and recursive subagent delegation.

### Modified Capabilities

- None.

## Impact

- New MCP tool in `mcp-server/asce_parser.py`.
- New primary agent markdown under `.opencode/agents/`.
- Possible updates to MCP permissions and OpenCode wiring.
- No changes to the existing schema files are expected.
