## Context

Current assurance-case scoping in high-consequence domains often defaults to checklist and activity-first framing, which weakens traceability from customer risk statements to defensible argument structure. This design introduces a Principles-Based Assurance (PBA) Socratic multi-agent component that converts discovery inputs into a normalized GSN scaffold and explicitly marks unsupported claims for downstream commercial mapping.
The refinement adds an Assurance Cube model so each gap is categorized by principle, abstraction layer (Component, Functional Cluster, System, Scenario), and case state (Claim, Strategy, Context, Unsupported Gap).

## Goals / Non-Goals

**Goals:**
- Add a `PBAOrchestrator` plus class-specialist Inquisitors that run justification-led scoping under NCSC PBA.
- Enforce dual-route ingestion (document-driven and greenfield interview) with deterministic routing and state management.
- Enforce anti-activity constraints that invert delivery/tool mentions into intrinsic claim-property questions.
- Produce normalized GSN scaffold JSON with explicit G/S/C/A nodes, `unsupported` flags, `commercial_gap_type` metadata, and abstraction-layer tags.
- Let consultants see where confidence breaks across layers so a strong component-level case does not mask a scenario-level gap.
- Preserve clear handoff boundaries: this component identifies unsupported claims but does not recommend billable activities.

**Non-Goals:**
- Automatically generating full evidence nodes or running verification activities.
- Generating Statement of Work line items from unsupported claims inside this agent.
- Replacing bootstrap, narrative synthesis, or top-down architecture agents.
- Defining domain-specific claim taxonomies for every vertical/customer.

## Decisions

1. Use a coordinator-specialist topology (`PBAOrchestrator`, `ProvenanceInquisitor`, `ArchitectureInquisitor`, `ResilienceInquisitor`).
   - Rationale: dense engineering inputs are better decomposed by principle class, reducing prompt drift and concentrating expertise.
   - Alternative considered: single monolithic inquisitor; rejected due to lower consistency and weaker principle coverage.

2. Implement dual-route ingestion with a state-machine triage.
   - Rationale: consultants operate in both document-heavy and blank-canvas sessions; explicit routing avoids conversational dead ends.
   - Alternative considered: single conversational path; rejected because uploaded-document sessions need preprocessing and omission analysis.

3. Keep the three-phase Socratic questioning model inside both routes (Claim Extraction, Strategy Decomposition, Activity Mapping).
   - Rationale: preserves the logic-of-confidence progression and standardizes output quality.
   - Alternative considered: unconstrained free-form questioning; rejected due to inconsistent branch quality.

4. Enforce an anti-activity guardrail with Socratic inversion.
   - Rationale: when users mention activities (for example pentest or audit), the agent must not generate deliverables and must ask what intrinsic property is being defended.
   - Alternative considered: soft warning only; rejected because it allows activity creep during scoping.

5. Represent output as normalized JSON scaffold package (top claim, sub-claims, assumptions, contexts, mapped principles, unsupported flags, gap type).
   - Rationale: downstream agents need machine-readable and human-readable artifacts to continue the pipeline with minimal friction.
   - Alternative considered: transcript-only output; rejected because consumers would need additional parsing and interpretation.

6. Encode reusable Socratic "stings" as first-class prompt rules.
   - Rationale: repeated challenge prompts (specificity, evidence-gap, scope-creep) harden reasoning and reduce ungrounded claims.
   - Alternative considered: optional heuristic hints; rejected because optionality reduces scoping rigor.

7. Add orchestration hooks for handoff to bootstrap, narrative, and SoW mapping agents.
   - Rationale: the scoping phase should end with actionable outputs for existing workflows rather than isolated dialogue transcripts, and layer-aware gaps need to survive the handoff.
   - Alternative considered: leave handoff manual; rejected due to additional operator burden and inconsistency.

8. Add layer-aware confidence reporting to the consultant-facing response.
   - Rationale: the consultant needs to see which abstraction layer is missing evidence and where to drill up or down next.
   - Alternative considered: flat unsupported-claim flags only; rejected because they hide whether the gap is component, cluster, system, or scenario level.

## Risks / Trade-offs

- [Over-questioning may increase scoping time] -> Mitigation: add stop conditions (atomic claim threshold, max rounds per branch, operator override to finalize scaffold).
- [Question-only behavior may frustrate users expecting guidance] -> Mitigation: allow reflective restatement and options framing while still avoiding direct answers.
- [Overly strict anti-activity filters may block legitimate context] -> Mitigation: classify mentions as context vs recommendation and only block recommendation generation.
- [Outputs may still vary across domains] -> Mitigation: use normalized scaffold schema plus mandatory fields for claim, context source, and activity mapping.
- [Layer classification may be ambiguous for hybrid claims] -> Mitigation: allow a primary layer plus secondary layer note when a claim straddles component/cluster/system/scenario boundaries.
- [Handoff mismatch with downstream consumers] -> Mitigation: define and validate a stable scaffold contract before enabling by default.
- [Scope creep from enthusiastic decomposition] -> Mitigation: enforce explicit in-scope/out-of-scope checks per branch using the scope-creep sting.

## Migration Plan

1. Add `PBAOrchestrator` and class-specialist Inquisitor agent definitions behind a feature flag.
2. Implement route triage and document preprocessing (entity extraction, principle-class mapping, omission hypothesis generation).
3. Implement phased questioning, anti-activity inversion, and scaffold serialization.
4. Add layer classification and confidence-gap reporting across Component, Functional Cluster, System, and Scenario levels.
5. Add adapter layer to hand off scaffold artifacts to bootstrap, narrative, and SoW mapping flows.
6. Validate with representative scoping scenarios across both routes and compare output quality versus current process.
7. Roll out as default for scoping workflows after acceptance; keep fallback to existing flow during transition.

## Open Questions

- Should the scaffold contract be persisted as AXML-native structures immediately or as an intermediate format with later conversion?
- What quantitative acceptance signals should gate default rollout (e.g., reduction in missing assumptions, faster downstream tasking, fewer re-scoping cycles)?
- Do we need domain-tuned sting variants (e.g., security-heavy vs safety-heavy contexts) in the first iteration?
- Should `commercial_gap_type` use a controlled taxonomy now or remain extensible/free-form in v1?
- Should consultant-facing reports show a single dominant layer or multiple layer tags when the evidence gap spans levels?
