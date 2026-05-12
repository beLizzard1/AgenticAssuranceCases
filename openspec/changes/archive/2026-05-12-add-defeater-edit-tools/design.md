## Context

The repository already has schema-aware parsing, neighborhood inspection, and targeted write-back for limited fields. The missing piece is precise mutation: the red-team agents need a safe way to add defeaters, and the concretion workflow needs a way to rewrite existing node text without broader XML surgery.

## Goals / Non-Goals

**Goals:**
- Add atomic graph-edit tools for defeater insertion and node text rewriting.
- Keep the mutation API narrow enough for subagent use.
- Preserve existing identifiers, unrelated links, and schema-defined fields.
- Fit the new tools into the existing MCP server and OpenCode agent structure.

**Non-Goals:**
- Building a general-purpose `.axml` editor.
- Allowing arbitrary graph restructuring or bulk refactors.
- Changing the assurance schema itself.

## Decisions

- Implement `write_defeater` as an atomic operation that creates both the defeater node and its defeats link.
  - Rationale: the red-team workflow needs one action that is internally consistent, not two loosely coupled writes.
  - Alternative considered: expose node and link creation separately. That gives more flexibility, but it makes partially applied edits easier to produce.

- Treat `update_node` and `rewrite_node` as aliases for the same focused rewrite behavior.
  - Rationale: the concretion subagent needs a predictable way to change existing node text, and two separate names would likely drift into redundant semantics.
  - Alternative considered: separate tools for label rewrite and annotation rewrite. That would be more explicit, but it would also multiply the surface without a strong need yet.

- Restrict the rewrite tool to the node's primary textual content plus any explicitly selected text field.
  - Rationale: concretion is about clarifying wording, not mutating the rest of the node payload.
  - Alternative considered: allow free-form field patching. That would be broader, but it would undermine the safety goal.

- Validate target nodes and link endpoints against the parsed graph before writing.
  - Rationale: these operations should fail early on bad IDs rather than emit malformed XML.
  - Alternative considered: best-effort writes with later validation. That would be more forgiving, but riskier for a mutation path.

- Keep the outputs descriptive and stable so downstream agents can chain edits.
  - Rationale: red-team and concretion flows often need to verify what changed before deciding the next step.
  - Alternative considered: return only a success flag. That would be simpler, but not enough for multi-step orchestration.

## Risks / Trade-offs

- Atomic defeater creation may still need schema-specific placement rules -> Use schema metadata and validate link semantics before writing.
- Alias semantics for rewrite tools may confuse callers -> Document one canonical tool name and keep the alias purely for compatibility.
- Overly narrow rewrite behavior may not cover future mutation cases -> Start constrained, then expand only if a concrete workflow needs it.
- Mutation bugs can corrupt `.axml` files -> Preserve the original tree where possible and test against the sample assurance case.

## Migration Plan

1. Add the new MCP mutation tool(s) to `mcp-server/asce_parser.py`.
2. Update the red-team and concretion agent prompts or permissions to use the new tools.
3. Validate the tools on the sample `.axml` file and confirm the output still round-trips.
4. If necessary, remove the new tool bindings and fall back to the previous write-back path.

## Open Questions

- Should `write_defeater` accept a target node ID only, or also a target link/reference selector?
- Should the rewrite tool update annotation content separately from title/text content?
- Do we need to expose a direct rollback or delete path for defeater edits, or is overwrite enough for now?
