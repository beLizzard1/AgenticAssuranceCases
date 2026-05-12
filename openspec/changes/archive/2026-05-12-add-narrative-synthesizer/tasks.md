## 1. MCP Shared Context

- [x] 1.1 Add `set_system_context` and `get_system_context` MCP tools in `mcp-server/asce_parser.py` for in-memory shared brief storage.
- [x] 1.2 Ensure the MCP server exposes the shared-context tools under the same provider used by the assurance workflows.
- [x] 1.3 Validate that the context brief can be saved and retrieved without affecting graph parsing.

## 2. Narrative Synthesizer Agent

- [x] 2.1 Add `.opencode/agents/narrative-synthesizer.md` with executive briefing and context-generation modes.
- [x] 2.2 Grant the agent permission to call the parser and shared-context MCP tools.
- [x] 2.3 Confirm the agent name, file name, and tool references are consistent with the repo's existing OpenCode conventions.

## 3. Validation

- [x] 3.1 Run the executive briefing mode against a representative assurance case and confirm it produces the requested narrative sections.
- [x] 3.2 Run the context-generation mode and confirm the saved system brief can be reused by downstream agents.
