## 1. Project Infrastructure
- [x] 1.1 Create the `mcp-server/` directory.
- [x] 1.2 Verify `opencode.json` points at the local MCP parser entrypoint.

## 2. MCP Server Implementation
- [x] 2.1 Add `mcp-server/requirements.txt` with `mcp`, `networkx`, and `beautifulsoup4`.
- [x] 2.2 Implement `mcp-server/asce_parser.py` to extract nodes, annotations, and links into a schema-aware NetworkX graph.
- [x] 2.3 Expose the parser as the `parse_assurance_case` MCP tool.
- [x] 2.4 Add a neighborhood-context tool that returns the local subgraph around a claim node.
- [x] 2.5 Add a write-back tool that persists targeted `.axml` edits without dropping schema-defined fields.

## 3. Agent Definitions
- [x] 3.1 Review and update `.opencode/agents/assurance-evaluator.md` with any parser/tool reference changes.
- [x] 3.2 Normalize `.opencode/agents/evidence_incorporation.md` to `.opencode/agents/evidence-incorporation.md` if the file is still referenced that way.
- [x] 3.3 Normalize `.opencode/agents/substituion.md` to `.opencode/agents/substitution.md`.
- [x] 3.4 Review existing `.opencode/agents/calculation.md`, `.opencode/agents/decomposition.md`, and `.opencode/agents/concretion.md` for consistency.

## 4. Validation
- [x] 4.1 Verify the parser returns the expected schema-aware semantic graph for a representative `.axml` file.
- [x] 4.2 Verify the primary agent routes claims to the intended specialist prompts.
