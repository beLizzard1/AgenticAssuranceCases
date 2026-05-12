## Context

The current MCP server parses `.axml` into a schema-aware graph and also supports targeted in-place mutations. That works for small edits, but it is fragile when links, references, or other identity-sensitive structures must be preserved across repeated edits. This change introduces a reconstruction path that treats the parsed graph plus schema metadata as the source of truth for emitted output.

## Goals / Non-Goals

**Goals:**
- Recreate `.axml` output from the graph model and schema metadata.
- Avoid stale link reuse by rebuilding relationships from graph edges.
- Keep output generation deterministic enough to compare and validate.
- Preserve stable node identity where the graph already defines it.
- Hand off the reconstructed file as the active path for future MCP calls.

**Non-Goals:**
- Rewriting the entire parser or graph extraction layer.
- Adding a new case editor UI.
- Guaranteeing byte-for-byte preservation of the original XML formatting.
- Preserving every unknown vendor-specific XML extension unless explicitly modeled.

## Decisions

- Use a graph-to-XML reconstruction step as the primary output path for this capability.
  - Rationale: a rebuild step avoids carrying forward broken or stale link elements from prior edits.
  - Alternatives considered: in-place patching of existing XML, and a hybrid patch/rebuild approach. Both keep legacy structure around longer and make identity bugs easier to retain.

- Generate links from graph edges rather than reusing serialized link nodes.
  - Rationale: links are derived structure, so rebuilding them from relationships keeps the XML aligned with the graph.
  - Alternatives considered: mutate existing link nodes or preserve link objects across edits. Those approaches are more fragile when endpoints move or are deleted.

- Treat schema metadata as the serialization contract.
  - Rationale: the schema already defines the node, link, and status-field shape the parser understands.
  - Alternatives considered: ad hoc serializer rules or relying on previously emitted XML as a template. Those approaches drift from the source schema over time.

- Track the active `.axml` path in MCP session state after reconstruction.
  - Rationale: future parse/query/edit operations should continue from the regenerated file instead of accidentally reading the stale source.
  - Alternatives considered: leaving path selection to callers, or relying only on shared context. Those approaches make follow-up operations easy to misroute.

- Validate reconstructed output before write-back.
  - Rationale: reconstruction can fail silently if required fields are omitted or ordered incorrectly.
  - Alternatives considered: write first, validate later. That makes broken artifacts harder to catch and rollback.

## Risks / Trade-offs

- [Formatting drift] -> The regenerated XML may not match the original byte-for-byte. Mitigation: focus tests on structural equivalence and schema validity, not raw text identity.
- [Unknown metadata loss] -> Unmodeled extensions may be omitted during reconstruction. Mitigation: preserve passthrough containers where possible and document unsupported fields explicitly.
- [Identity churn] -> Rebuilt links and derived elements may receive new identifiers. Mitigation: use deterministic allocation where possible and keep node IDs stable.
- [Migration friction] -> Existing workflows that expect in-place edits may need to switch. Mitigation: keep the parser/read path unchanged while introducing reconstruction as an explicit capability.
- [Session drift] -> Subsequent MCP calls may still target the old file if the active path is not updated. Mitigation: make path promotion part of the reconstruction handoff.
