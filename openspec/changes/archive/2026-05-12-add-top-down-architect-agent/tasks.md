## 1. MCP Navigation Tools

- [x] 1.1 Add a `get_node_children` MCP tool in `mcp-server/asce_parser.py` that returns the immediate child nodes for a given parent node ID.
- [x] 1.2 Add a `get_root_claims` MCP tool in `mcp-server/asce_parser.py` that returns the root starting points for top-down traversal.
- [x] 1.3 Verify the new MCP tools work against the sample `.axml` file in `examples/`.

## 2. Top-Down Architect Agent

- [x] 2.1 Add `.opencode/agents/top-down-architect.md` with the root-first traversal workflow and recursive delegation rules.
- [x] 2.2 Grant the agent permission to call the new MCP navigation tools and the existing specialist subagents.
- [x] 2.3 Confirm the agent name, filename, and routing references are consistent.

## 3. Validation

- [x] 3.1 Run the top-down architect against a representative assurance case branch and confirm it walks from root to leaf.
- [x] 3.2 Confirm unsupported branches delegate to the intended specialist subagent and resume traversal afterward.
