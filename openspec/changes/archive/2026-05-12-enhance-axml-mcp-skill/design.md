## Context

The repository already has an AXML MCP skill, but it is broad and under-specified for the current `asce_tools` server shape. The enhanced version needs to reflect the actual tool surface, the current agent architecture, and the repo's preference for graph-based assurance-case work over direct XML editing.

## Goals / Non-Goals

**Goals:**
- Replace generic skill guidance with repo-specific MCP-first operating rules.
- Make discovery-first usage explicit so agents do not assume unavailable tools.
- Distinguish structural assurance-case edits from purely editorial changes.
- Keep the skill aligned with current `asce_tools` capabilities and permissions.

**Non-Goals:**
- Adding new MCP server endpoints.
- Reworking the parser or reconstruction implementation.
- Mandating MCP for unrelated prose or documentation-only edits.
- Turning the skill into a full server reference manual.

## Decisions

- Keep the skill as a standalone OpenCode skill under `.opencode/skills/`.
  - Rationale: the AXML guidance needs to be reusable across all assurance-case agents.
  - Alternatives considered: duplicating guidance in every agent file or keeping it only in the README. Both are harder to keep in sync.

- Describe the current repository tool surface explicitly, not a generic MCP wishlist.
  - Rationale: the repo's `asce_tools` server currently exposes graph parsing, neighborhood traversal, root/child discovery, shared context, evidence-provider lookup, defeater creation, targeted updates, and reconstruction-oriented workflows.
  - Alternatives considered: listing only abstract capabilities or hypothetical operations. That would make the skill less actionable.

- Use MCP-first semantics for structural changes and targeted write-back.
  - Rationale: assurance-case structure is graph-like and benefits from semantic operations.
  - Alternatives considered: treating raw `.axml` edits as equivalent. That would weaken traceability and increase drift.

- Keep a narrow raw-edit exception for comments, unsupported metadata, and emergency recovery.
  - Rationale: the repo still needs a practical escape hatch for non-semantic content and failures.
  - Alternatives considered: banning all direct edits. That would be unnecessarily rigid for documentation and recovery scenarios.

- Point repo docs at the skill rather than duplicating the full guidance everywhere.
  - Rationale: the skill should remain the authoritative place for AXML MCP behavior, while docs provide discovery.
  - Alternatives considered: copying the whole skill into README and agent docs. That would create maintenance overhead and drift.

## Risks / Trade-offs

- [Guidance drift] -> If the skill and server evolve separately, the guidance may become inaccurate. Mitigation: keep the skill's capability list narrow and repo-specific.
- [Over-prescription] -> Agents may overuse MCP for trivial editorial edits. Mitigation: preserve the explicit non-semantic exceptions.
- [Under-documentation] -> The skill may be too terse for new users. Mitigation: keep README pointers and agent doc references.
- [Server mismatch] -> The skill may mention operations not currently exposed by `asce_tools`. Mitigation: verify against the parser implementation and current permissions before release.

## Migration Plan

1. Replace the existing skill text with the enhanced repository-specific version.
2. Update the README and assurance-agent docs to point to the skill.
3. Validate the skill wording against the current `asce_tools` surface.
4. If the server gains new tools later, update the skill in place rather than spreading guidance across multiple files.

## Open Questions

- Should the skill mention the reconstructed active path as a first-class concept, or keep that detail implicit in the workflow?
- Should a small contract doc be added alongside the skill for future tool-surface changes?
- Should the README include a one-line usage recommendation for the skill, or only a path reference?
