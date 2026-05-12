## Context

The repository already supports AXML graph inspection, traversal, defeaters, shared context, evidence-provider discovery, and targeted write-back. What is missing is a first-pass synthesis workflow that can start from a system description and produce a defensible assurance-case scaffold.

This change spans the agent layer, MCP server capabilities, and reusable assurance patterns. It also introduces a new architectural flow: system context first, argument strategy second, graph synthesis third.

## Goals / Non-Goals

**Goals:**
- Create an initial assurance-case scaffold from system context and assurance intent.
- Preserve explicit uncertainty through assumptions, evidence gaps, and defeaters.
- Keep the generated case sparse and reviewable.
- Make the bootstrap strategy visible in the graph.
- Support reusable bootstrap patterns for common assurance contexts.

**Non-Goals:**
- Producing a certification-ready or complete assurance case.
- Replacing later human refinement or detailed evidence curation.
- Encoding one fixed assurance methodology for every system.
- Changing existing traversal or mutation semantics beyond what bootstrap requires.

## Decisions

1. **Use an orchestration workflow rather than a single generation step.**
   The bootstrap process should sequence context capture, strategy selection, graph synthesis, evidence binding, defeater generation, and summary output. This keeps each step reviewable and lets later stages reuse existing MCP primitives. A single prompt-to-XML step would be harder to validate and more likely to hide uncertainty.

2. **Represent shared context inside the case graph.**
   The system identity, operational context, assurance scope, threats, and assets should become first-class graph material rather than a sidecar document. This keeps the bootstrap output navigable, mutable, and available to later traversal. A separate document would be easier to lose alignment with the case.

3. **Make the assurance strategy explicit.**
   The workflow should attach a strategy node or equivalent metadata before claim synthesis. That makes the decomposition choice inspectable and gives reviewers a handle for changing the argument style later. Hidden strategy selection would make the scaffold harder to trust.

4. **Prefer sparse scaffolding over invented completeness.**
   The bootstrap graph should include claims, arguments, assumptions, contexts, evidence placeholders, and defeaters, but only where there is enough basis to justify them. Missing support must remain visible. A denser tree would look more mature but would be less honest.

5. **Implement reusable patterns as templates, not hard-coded trees.**
   Common assurance contexts should be instantiated from pattern templates that adapt to the supplied system context. This gives consistency without forcing every case into the same shape. Hard-coded trees would be brittle and would not scale across domains.

6. **Extend MCP with additive creation and review primitives.**
   New MCP operations should support case creation, claim/context/evidence placeholder creation, semantic linking, unresolved-gap discovery, and summary generation. This keeps bootstrap logic close to the graph layer and avoids embedding write logic in the agent alone.

## Risks / Trade-offs

- [Risk] Over-generic bootstrap output → Mitigation: require explicit context fields and strategy selection before synthesis.
- [Risk] Inflated confidence in the initial case → Mitigation: mandate sparse scaffolding, visible evidence gaps, and defeaters.
- [Risk] Template sprawl across domains → Mitigation: start with a small pattern set and keep templates parameterized.
- [Risk] MCP/API surface growth → Mitigation: keep new primitives narrowly scoped to bootstrap creation and review.
- [Risk] Inconsistent graph shape across runs → Mitigation: define bootstrap requirements around stable concepts rather than a fixed tree shape.

## Migration Plan

1. Add the bootstrap capability as a new change path without altering existing case workflows.
2. Implement new MCP primitives behind additive APIs.
3. Add the orchestration agent to coordinate bootstrap synthesis.
4. Introduce one or two starter templates and validate them against the new spec.
5. Reconstruct and inspect a generated case before expanding the pattern library.

Rollback is straightforward: disable the new bootstrap entrypoint and leave existing traversal/mutation flows untouched.

## Open Questions

- Which graph node types or attributes should represent context, evidence placeholders, and strategy most cleanly?
- Should bootstrap templates live in a dedicated pattern registry or alongside other case assets?
- How much of the workflow should be delegated to specialist agents versus a single orchestrator?
- What should the initial starter pattern set include beyond the most common security/safety cases?
