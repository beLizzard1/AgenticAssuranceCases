## Context

The repository already has a schema-aware MCP parser and several specialist assurance agents. This change adds a complementary narrative layer that can explain the case to humans and generate a short shared context brief for other agents to consume.

## Goals / Non-Goals

**Goals:**
- Add a primary agent that can turn a CAE graph into an executive narrative.
- Add a second mode that produces a compact system brief for other agents.
- Keep the shared context small, local, and easy to query.
- Reuse the existing parser rather than introducing a new data model.

**Non-Goals:**
- Replacing the assurance evaluator or red-team workflows.
- Building long-lived persistence or external memory storage.
- Adding graph editing behavior.

## Decisions

- Keep the shared context in memory inside the MCP server.
  - Rationale: the brief is advisory context, not durable domain state, so local state is enough and avoids a new dependency.
  - Alternative considered: external storage. That would survive restarts, but it would complicate the setup and add failure modes that the current workflow does not need.

- Expose explicit `set_system_context` and `get_system_context` MCP tools.
  - Rationale: the synthesizer needs one write path and one read path so other agents can reuse the same brief without scraping prompts.
  - Alternative considered: keep the brief only in agent memory. That would be simpler, but it would not be shareable across runs.

- Make the narrative synthesizer primarily read-only except for saving the shared brief.
  - Rationale: its job is synthesis, not mutation of the assurance graph.
  - Alternative considered: allow editing of the `.axml` content. That would blur responsibilities and raise the risk of unintended changes.

- Structure the executive response into a fixed set of sections.
  - Rationale: stakeholders need consistency, and a stable shape makes the output easier to scan.
  - Alternative considered: free-form summaries. That could be more expressive, but it would be less reliable across different cases.

- Keep the context brief under a hard size target.
  - Rationale: downstream agents need concise state that fits comfortably into prompt context.
  - Alternative considered: store the full parsed graph summary. That would be richer, but it would be too verbose to reuse efficiently.

## Risks / Trade-offs

- In-memory context is lost on restart -> Accept that limitation because the brief is disposable and can be regenerated.
- Narrative quality may vary across different case shapes -> Use the graph parser plus a fixed response structure to reduce drift.
- Shared context could become stale if the underlying case changes -> Regenerate the brief whenever the source case is updated.
- The synthesizer may over-summarize important nuance -> Keep the executive format concise but allow explicit requests for deeper detail.

## Migration Plan

1. Add the new MCP context tools to `mcp-server/asce_parser.py`.
2. Add the narrative synthesizer agent with the two operating modes.
3. Validate executive brief generation and shared-context save/retrieve behavior.
4. If needed, remove the new tools and revert to prompt-only summarization.

## Open Questions

- Should the shared context brief be stored as a single string or as structured fields later?
- Do we need a guardrail to prevent unrelated agents from overwriting the context brief?
- Should the executive mode include explicit confidence language or stay purely descriptive?
