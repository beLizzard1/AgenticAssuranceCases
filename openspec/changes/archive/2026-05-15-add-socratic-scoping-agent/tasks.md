## 1. PBA Multi-Agent Foundation

- [x] 1.1 Add `PBAOrchestrator` and class-specialist agents (`ProvenanceInquisitor`, `ArchitectureInquisitor`, `ResilienceInquisitor`) to the registry/config.
- [x] 1.2 Implement system prompt contracts for each sub-agent with NCSC PBA class focus and strict G/S/C/A extraction behavior.
- [x] 1.3 Add automated checks/tests that fail if agents emit solution recommendations or direct service/activity proposals.
- [x] 1.4 Add abstraction-layer taxonomy support for Component, Functional Cluster, System, and Scenario.

## 2. Dual-Route Ingestion and Session Orchestration

- [x] 2.1 Implement route triage state machine for document-driven processing vs greenfield interview mode.
- [x] 2.2 Implement document preprocessing for entity extraction, boundary mapping, and omission-driven claim hypothesis generation.
- [x] 2.3 Implement the three-phase session flow (Claim Extraction -> Strategy Decomposition -> Activity Mapping) and recursive loop controls.
- [x] 2.4 Add next-layer-up challenge logic so component evidence triggers cluster/system questioning and scenario claims trigger drill-down support checks.

## 3. Guardrails and Socratic Challenge Logic

- [x] 3.1 Implement anti-activity inversion guardrail that intercepts activity/tool terms and asks for the intrinsic claim/property being defended.
- [x] 3.2 Implement specificity and evidence-gap sting prompts with explicit NCSC principle mapping requirements.
- [x] 3.3 Implement scope-creep sting prompts and enforce a maximum of two questions per agent turn.
- [x] 3.4 Add layer-aware sting prompts that differentiate component, cluster, system, and scenario confidence gaps.

## 4. Scaffold Data Model and Handoffs

- [x] 4.1 Define and implement normalized scaffold JSON with G/S/C/A node typing, principle references, abstraction-layer tags, and parent-child structure.
- [x] 4.2 Add required leaf metadata fields (`unsupported`, `commercial_gap_type`, `abstraction_layer`) for downstream SoW mapping.
- [x] 4.3 Add adapter/serialization logic so scaffold output is consumable by bootstrap, narrative synthesis, top-down architecture, and SoW mapping workflows.
- [x] 4.4 Add consultant-facing confidence-gap summary output grouped by principle and abstraction layer.

## 5. Validation and Rollout

- [x] 5.1 Create test scenarios for both routes (document dump and blank-canvas) and validate phase coverage, guardrail behavior, principle tagging, and layer tagging.
- [x] 5.2 Compare output quality against current scoping flow and document acceptance criteria tied to unsupported-claim clarity, layer diagnostics, and handoff readiness.
- [x] 5.3 Roll out behind a feature flag, add fallback path to legacy scoping flow, and document consultant/operator usage guidance for layer-aware reporting.
