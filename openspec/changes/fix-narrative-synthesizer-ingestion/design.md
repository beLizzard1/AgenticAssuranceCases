## Context

The narrative synthesizer already exists as a human-facing summary agent plus a context-generation mode. The regression is conceptual rather than structural: its ingest path needs to be explicitly parser-first so it does not drift back toward treating `.axml` files as plain text.

## Goals / Non-Goals

**Goals:**
- Make the narrative synthesizer explicitly ingest assurance cases through `parse_assurance_case`.
- Keep executive briefs and system briefs grounded in parser output.
- Preserve the shared context handoff for downstream agents.
- Keep the fix narrow to the narrative agent and its prompt contract.

**Non-Goals:**
- Changing the parser's graph model.
- Adding new storage beyond the existing in-memory brief.
- Redesigning the executive summary format.

## Decisions

- Treat `parse_assurance_case` as the only supported ingest entrypoint for narrative synthesis.
  - Rationale: the parser already normalizes schema-aware graph data, which is the correct source of truth for both narrative modes.
  - Alternative considered: allow direct file/text reads as a fallback. That would be easier to describe, but it would reintroduce brittle, layout-dependent behavior.

- Keep both narrative modes operating on parsed graph data.
  - Rationale: the executive briefing and system-context brief should be derived from the same structured case view.
  - Alternative considered: let the context brief be built from raw text while the briefing uses parsed data. That would create inconsistency between the two outputs.

- Keep `set_system_context` as the only write path for the shared brief.
  - Rationale: the context brief is meant for reuse, not for ad hoc prompt stuffing.
  - Alternative considered: return the brief only in the agent response. That would be simpler, but less reusable.

- Update the agent prompt to state the required ingest behavior directly.
  - Rationale: the agent prompt is where this workflow is enforced in practice.
  - Alternative considered: rely on convention alone. That would be easier to maintain incorrectly.

## Risks / Trade-offs

- The agent may still be tempted to inspect files directly if the prompt is vague -> Make the parser requirement explicit and testable.
- Parser output may miss a detail the narrator wants -> Use the graph plus neighborhood context, not raw text, to recover needed structure.
- Context brief drift can make downstream agents inconsistent -> Regenerate the brief from the same parser output whenever needed.
- Tight prompt constraints can reduce flexibility -> Keep the briefing structure fixed but allow explicit follow-up questions.

## Migration Plan

1. Update the narrative-synthesizer prompt to require `parse_assurance_case` for both modes.
2. Verify the prompt no longer instructs raw file reading or text ingestion.
3. Validate both narrative modes against the sample `.axml` file and confirm the shared brief still persists.
4. Roll back by restoring the previous prompt wording if the parser-first flow becomes too restrictive.

## Open Questions

- Should the prompt mention `get_system_context` explicitly in the context-generation flow?
- Do we want to add an explicit negative instruction against direct `.axml` text reads?
- Should the executive briefing use the full graph or only a summary of root claims and immediate supporting structure?
