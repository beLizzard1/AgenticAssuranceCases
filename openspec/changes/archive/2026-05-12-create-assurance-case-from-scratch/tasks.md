## 1. Bootstrap foundation

- [x] 1.1 Add the new bootstrap capability folder and any supporting template assets for reusable assurance-case patterns.
- [x] 1.2 Define the initial bootstrap data model for shared context, strategy, evidence gaps, assumptions, and defeaters.
- [x] 1.3 Confirm the new capability maps cleanly to the existing AXML schema and graph conventions.

## 2. MCP graph primitives

- [x] 2.1 Add MCP operations for creating a fresh assurance case and inserting bootstrap-specific nodes.
- [x] 2.2 Add MCP operations for creating claims, contexts, assumptions, evidence placeholders, and semantic links.
- [x] 2.3 Add MCP operations for unresolved-gap discovery and concise case-summary generation.

## 3. Orchestration workflow

- [x] 3.1 Implement the bootstrap orchestration agent that captures system context before claim synthesis.
- [x] 3.2 Add strategy selection and explicit top-level claim synthesis to the bootstrap flow.
- [x] 3.3 Add evidence discovery, evidence binding, and placeholder creation to the workflow.
- [x] 3.4 Add defeater generation for major branches that depend on weak evidence or assumptions.

## 4. Templates and pattern reuse

- [x] 4.1 Add starter bootstrap templates for the first target assurance contexts.
- [x] 4.2 Parameterize templates so the generated graph reflects the supplied system context rather than a canned tree.

## 5. Verification and packaging

- [x] 5.1 Validate that a bootstrap run produces an initial `.axml` case with visible gaps and defeaters.
- [x] 5.2 Verify the generated case can be reconstructed and reloaded without losing the bootstrap structure.
- [x] 5.3 Document the bootstrap workflow and how to invoke `/opsx-apply` for implementation.
