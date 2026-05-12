## 1. MCP Mutation Tools

- [x] 1.1 Add a `write_defeater` MCP tool in `mcp-server/asce_parser.py` that atomically creates a Type 8 defeater node and its Type 5 defeats link.
- [x] 1.2 Add an `update_node` / `rewrite_node` MCP tool in `mcp-server/asce_parser.py` that rewrites an existing node's text in place.
- [x] 1.3 Validate both mutation tools against the sample `.axml` file in `examples/` and confirm unrelated graph structure is preserved.

## 2. Agent Integration

- [x] 2.1 Update the red-team agent prompts and permissions so defeater subagents can use `write_defeater`.
- [x] 2.2 Update the concretion agent prompt and permissions so it can use `update_node` / `rewrite_node`.
- [x] 2.3 Confirm the tool names and agent references are consistent across OpenCode configuration files.

## 3. Validation

- [x] 3.1 Run a defeater write flow and confirm the returned identifiers and status are sufficient for chaining follow-up edits.
- [x] 3.2 Run a concretion rewrite flow and confirm the target node text changes without altering unrelated nodes or links.
