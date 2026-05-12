# Case Bootstrap Workflow

This repository now includes a greenfield assurance-case bootstrap path.

## Flow
1. Capture item definition, operational context, assurance scope, and threats.
2. Select a bootstrap pattern and assurance strategy.
3. Create a fresh `.axml` case.
4. Add the top-level claim, context, assumptions, evidence placeholders, and defeaters.
5. Bind known evidence and leave unresolved gaps visible.
6. Reconstruct and validate the result.

## Implementation Entry Point
- Use `/opsx-apply` to implement an OpenSpec change after its proposal, design, specs, and tasks are complete.
- Use `/opsx-propose` when you want to create a new change from a description.

## MCP Tools
The bootstrap workflow is backed by MCP tools in `mcp-server/asce_parser.py` for case creation, node creation, pattern instantiation, gap discovery, summary generation, and validation.
