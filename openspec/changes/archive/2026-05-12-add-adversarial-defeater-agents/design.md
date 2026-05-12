## Context

The repository already has a schema-aware AXML parser and a helping-hand builder workflow. This change adds the complementary red-team side: a dedicated pass that tries to break the assurance case by generating defeaters and attaching them back into the graph.

## Goals / Non-Goals

**Goals:**
- Add a primary adversarial router that selects the right defeater strategy.
- Support rebutting, undercutting, and undermining defeaters as separate subagents.
- Use the existing NetworkX-backed MCP tools for local context and write-back edits.
- Keep defeater generation explicit and schema-aware.

**Non-Goals:**
- Building a generic theorem prover or argument-mining engine.
- Replacing the existing builder-pass agents.
- Creating a new UI for visualizing defeaters.

## Decisions

- Use a peer primary agent instead of folding red-team logic into the builder agent. That keeps the two-pass workflow clear and avoids blending confirmatory and adversarial behavior.
- Reuse the existing parser and write-back tools rather than adding a second graph model. This keeps the red-team pass aligned with the same source of truth as the builder pass.
- Model defeaters as separate subagents because rebutting, undercutting, and undermining attacks have different prompts, evidence needs, and failure modes. A single generic red-team agent would be easier to build but harder to tune.
- Draft defeater nodes in schema terms so the output can be inserted into the `.axml` network without translation. Free-form text would be cheaper to produce, but it would be less useful for downstream editing.

## Risks / Trade-offs

- Adversarial prompts may become overly aggressive or noisy → Keep each subagent narrowly scoped to its defeater class.
- Write-back edits may corrupt structure if misapplied → Restrict edits to schema-aware node and link updates only.
- Red-team results may overlap with builder-pass content → Preserve clear agent separation and label defeaters explicitly.

## Migration Plan

1. Add the adversarial agent markdown files.
2. Wire the agent permissions to the existing MCP tools.
3. Validate that defeater nodes can be generated from parsed graphs and written back safely.
4. Roll back by removing the red-team agent files if the workflow proves too noisy.

## Open Questions

- Should defeaters be inserted automatically or only drafted for user approval?
- Do we want one generic defeater node shape or distinct metadata per defeater class?
- Should the red-team pass run after every builder pass, or only on demand?
