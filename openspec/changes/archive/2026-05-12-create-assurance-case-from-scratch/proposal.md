## Why

Current assurance-case workflows assume a case already exists. The repository is strong at inspection, traversal, defeaters, and targeted mutation, but it lacks a guided path from a system description and assurance intent to a defensible initial CAE graph.

## What Changes

- Add a greenfield assurance-case bootstrap workflow that turns item definition, operational context, assurance objectives, and evidence availability into an initial `.axml` case.
- Add explicit synthesis of shared system context, top-level claims, decomposition strategy, evidence gaps, assumptions, and defeaters.
- Add an orchestration agent to coordinate bootstrap steps and write the resulting case back through MCP.
- Extend MCP capabilities to support case creation, template instantiation, and unresolved-gap review.
- Add reusable bootstrap patterns/templates for common assurance contexts.

## Capabilities

### New Capabilities
- `assurance-case-bootstrap`: Create an initial assurance case from system context, assurance objectives, and available evidence.

### Modified Capabilities

- None

## Impact

- New OpenSpec change artifacts for bootstrap workflow, implementation design, and task breakdown.
- A new orchestration path in the agent and MCP layers.
- New or extended AXML graph operations for initial case synthesis and validation.
- Potentially new reusable templates for assurance-case patterns.
