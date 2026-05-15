## Why

In high-consequence domains, pre-sales scoping often collapses into compliance checklist thinking and activity-first estimates instead of argument-first engineering. We need a Principles-Based Assurance (PBA) Socratic agent that transforms unstructured discovery inputs into a defensible assurance scaffold, exposing unsupported claims before any commercial activity is proposed. The refinement adds an Assurance Cube so every gap is located by principle, abstraction layer, and case state.

## What Changes

- Add a `Socratic PBA Agent` (working title: `The Inquisitor`) that is explicitly justification-led and constrained to claim/strategy/context/assumption extraction.
- Implement a coordinator-specialist topology:
  - `PBAOrchestrator` as session router/compiler and state manager.
  - `ProvenanceInquisitor` for NCSC Class 1 principles.
  - `ArchitectureInquisitor` for NCSC Class 2 principles.
  - `ResilienceInquisitor` for NCSC Class 3 principles.
- Support dual-route ingestion:
  - Document-driven route for unstructured inputs with entity extraction, boundary mapping, and omission-driven Socratic challenge.
  - Greenfield interview route for blank-canvas discovery with anchor-claim-first progression.
- Add the four-layer Assurance Cube model for gap location:
  - Principles as the vertical dimension.
  - Abstraction layers as the horizontal dimension: Component, Functional Cluster, System, Scenario.
  - Case state as the depth dimension: Claim -> Strategy -> Context -> Unsupported Gap.
- Enforce anti-activity prompt safety constraints so tool/service mentions are inverted into claim-property questions rather than deliverable generation.
- Produce normalized GSN-like scaffold JSON with explicit `unsupported: true` leaf-goal flags, abstraction-layer tags, and `commercial_gap_type` categorization for downstream SoW mapping.
- Integrate scaffold handoff to downstream bootstrap/narrative/top-down workflows while keeping commercial activity generation outside this agent.

## Capabilities

### New Capabilities
- `socratic-scoping-agent`: Provides a PBA-aligned multi-agent Socratic scoping workflow that converts ambiguous customer requirements into a normalized assurance case scaffold with unsupported-claim gap tagging.
- `socratic-scoping-agent`: Provides a PBA-aligned multi-agent Socratic scoping workflow that converts ambiguous customer requirements into a normalized assurance case scaffold with unsupported-claim gap tagging and layer-aware confidence reporting.

### Modified Capabilities
- None.

## Impact

- Affected code: new orchestrator/sub-agent definitions, state-machine routing for dual-route ingestion, anti-activity guardrail logic, layer classification, and scaffold serialization.
- APIs/contracts: structured output contract for G/S/C/A nodes with `unsupported`, `commercial_gap_type`, and `abstraction_layer` fields consumable by downstream SoW pipeline stages.
- Dependencies: no mandatory external dependency; includes embedded NCSC PBA mapping metadata in agent prompt/config artifacts.
- Systems/process: pre-sales scoping shifts from activity-sales framing to defensible risk-architecture framing; unsupported claims become direct, auditable commercial gap inputs with explicit layer attribution.
