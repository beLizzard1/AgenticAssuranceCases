## Context

This change refines an existing assurance-case workflow spanning configuration, agent prompts, and a local parser service. The goal is to keep `.axml` handling token-efficient and make claim routing explicit rather than embedding everything in one prompt or script.

## Goals / Non-Goals

**Goals:**
- Parse `.axml` into a compact semantic representation for downstream agent use.
- Represent the assurance case as a directed graph so agents can request neighborhood context around a claim.
- Route claims through the existing primary agent using the Helping Hand decision flow.
- Keep the implementation local and easy to run inside the existing OpenCode setup.
- Support targeted write-back edits to the source `.axml` file for approved modifications.
- Use the schema definition in `schemas/ASCAD 2.0.xml` to validate node types, status fields, and link labels.
- Normalize the agent file naming so configured agent names and file names stay aligned.

**Non-Goals:**
- Building new UI surfaces.
- Integrating external evidence systems or issue trackers.
- Designing a general-purpose assurance-case editor.

## Decisions

- Use the existing OpenCode agent markdown files instead of creating a new orchestrator. This keeps routing logic in prompts where the framework already expects it. An alternative would be a single code-driven orchestrator, but that would be harder to maintain and less aligned with the repo structure.
- Implement a local MCP parser for `.axml` rather than passing raw XML to the model. This reduces token waste and makes structure extraction deterministic. The alternative is direct model parsing, but that is brittle and expensive.
- Use `networkx.DiGraph` as the in-memory model so neighborhood queries are cheap and predictable. A custom tree structure would be simpler, but it would make local context extraction more ad hoc.
- Keep the parser focused on node titles, stripped HTML annotations, and relationship links. A broader object model would be more complete, but it would add complexity without improving the initial workflow.
- Provide a write-back tool that edits only targeted nodes/annotations in-place. Rewriting the entire file from an abstract graph would be more general, but it would increase the risk of losing ASCE-specific structure.
- Use the schema file to map ASCAD numeric type codes and status-field names into stable labels. Hardcoding all field names would be simpler, but it would be less robust against schema-driven conventions.
- Rename inconsistent agent filenames to kebab-case where needed so task routing is predictable. Leaving the typos in place would preserve the current state, but it makes maintenance and references error-prone.

## Risks / Trade-offs

- Parser fidelity may miss edge cases in ASCE variants → Start with the common structure and expand only when needed.
- Graph reconstruction may lose non-essential XML details → Preserve unknown attributes and round-trip the original tree where possible.
- Schema interpretation may be incomplete for uncommon ASCAD constructs → Keep schema parsing data-driven and preserve unknown fields rather than dropping them.
- Agent routing may drift from the intended decision tree → Keep the primary agent minimal and make the route conditions explicit.
- Local dependency/config drift may make setup brittle → Document the MCP server entrypoint and keep configuration centralized.
- Filename mismatches between agent references and actual files may confuse routing → Normalize filenames and update references together.

## Migration Plan

1. Add the MCP parser and any missing configuration.
2. Update the existing agent markdown files and normalize filenames where needed.
3. Validate that `.axml` files are parsed through the tool path in the assurance workflow.
4. Roll back by reverting the parser/config changes and restoring the prior filenames if needed.

## Open Questions

- Should the parser support multiple ASCE schema variants from day one?
- How aggressively should HTML annotation content be stripped versus preserved?
- Do we need any additional metadata fields for future evidence retrieval workflows?
