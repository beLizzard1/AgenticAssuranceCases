## Why

The current graph-edit surface can create and inspect assurance case structure, but it does not expose the two mutation paths the red-team and concretion workflows need most: appending defeater attacks and rewriting an existing node's text in place. Adding these tools now makes the edit model precise, safer, and easier to delegate from specialized subagents.

## What Changes

- Add a dedicated MCP tool for creating a Type 8 defeater node and its Type 5 defeats link in one operation.
- Add a targeted node-rewrite tool for updating the text of an existing `.axml` node without restructuring the surrounding graph.
- Keep both tools narrow in scope so they can be used by specific subagents without broad graph mutation privileges.
- Preserve existing node identifiers, link structure, and unrelated metadata during mutation.
- **BREAKING**: the red-team and concretion workflows are expected to use the new mutation tools rather than ad hoc XML edits.

## Capabilities

### New Capabilities
- `defeater-edit-tools`: Atomic defeater creation and in-place node rewriting for assurance-case mutation workflows.

### Modified Capabilities

- None.

## Impact

- Updates to `mcp-server/asce_parser.py` and its exposed MCP tools.
- Updates to the `rebutting-defeater`, `undercutting-defeater`, `undermining-defeater`, and `concretion` agent permissions or prompts.
- Possible changes to OpenCode agent wiring if tool names are exposed explicitly.
- No schema changes are expected.
