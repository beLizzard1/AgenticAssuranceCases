## ADDED Requirements

### Requirement: PBA Orchestrator and Specialist Agents
The system SHALL provide a `PBAOrchestrator` and specialist Socratic sub-agents for NCSC PBA scoping: `ProvenanceInquisitor`, `ArchitectureInquisitor`, and `ResilienceInquisitor`.

#### Scenario: Orchestrator routes to specialist agent
- **WHEN** a scoping session receives input about build provenance, runtime boundaries, or lifecycle resilience
- **THEN** the orchestrator routes the conversation to the matching specialist agent

### Requirement: Dual-Route Ingestion
The system SHALL support document-driven processing and greenfield interview processing as distinct intake routes.

#### Scenario: Intake route is selected by input type
- **WHEN** the user uploads unstructured documents
- **THEN** the system performs document-driven preprocessing before Socratic questioning begins

### Requirement: Three-Phase Socratic Workflow
The system SHALL guide each scoping session through Claim Extraction, Strategy Decomposition, and Activity Mapping in that order.

#### Scenario: Session progresses through required phases
- **WHEN** the scoper provides either a document-driven or greenfield input
- **THEN** the agent first extracts claims and bounds, then challenges decomposition sufficiency, then maps intrinsic activities only as downstream evidence generators

### Requirement: Claim Extraction Coverage
The system SHALL elicit the top-level claim, operational bounds, governing references, and whether the claim is explicit or intrinsic to customer intent.

#### Scenario: Extraction captures claim framing fields
- **WHEN** the session is in Claim Extraction
- **THEN** the agent asks for top-level claim statement, applicable operating conditions/documents, and explicit-versus-intrinsic classification

### Requirement: Principle-Class Mapping
The system SHALL map scoped assertions to NCSC PBA principle classes and retain those mappings in the scaffold.

#### Scenario: Assertion is assigned a principle class
- **WHEN** a claim is grounded in build provenance, runtime design, or through-life resilience
- **THEN** the system tags the claim with the relevant NCSC principle class and principle reference where known

### Requirement: Four-Layer Assurance Cube
The system SHALL categorize every scoped claim or gap by abstraction layer: Component, Functional Cluster, System, or Scenario.

#### Scenario: Claim receives a layer tag
- **WHEN** the system extracts or refines a claim
- **THEN** the system assigns a primary abstraction layer tag and may assign a secondary layer note if the claim spans multiple layers

### Requirement: Strategy Sufficiency Challenge
During Strategy Decomposition, the system SHALL challenge whether proposed sub-claims are jointly sufficient and SHALL capture assumptions that may need formal representation.

#### Scenario: Decomposition includes sufficiency and assumptions
- **WHEN** the scoper proposes a decomposition strategy
- **THEN** the agent asks what failure modes remain if all sub-claims are proven and requests basis for assumptions such as trusted components

### Requirement: Activity-to-Claim Mapping
During Activity Mapping, the system SHALL map each scoped sub-claim to intrinsic properties or evidence-generating activities without recommending commercial deliverables.

#### Scenario: Activity mapping stays non-commercial
- **WHEN** a sub-claim is identified as implementation-relevant
- **THEN** the agent records the intrinsic property under question and whether secondary justification is needed for sufficiency

### Requirement: Layered Confidence Challenge
When a user supplies evidence at one abstraction layer, the system SHALL ask about the next higher layer if the confidence gap remains unresolved.

#### Scenario: Evidence at component level triggers upward challenge
- **WHEN** the user provides component-level evidence such as code review or unit test results
- **THEN** the agent asks how the claim behaves in the functional cluster or system context before accepting confidence as sufficient

### Requirement: Socratic Heuristics Enforcement
The system SHALL apply specificity, evidence-gap, and scope-creep challenge heuristics during scoping to reduce ambiguous, ungrounded, or out-of-scope branches.

#### Scenario: Heuristics trigger challenge questions
- **WHEN** a claim uses vague terms, maps activity without a property, or proposes out-of-scope work
- **THEN** the agent asks the corresponding sting question before accepting the branch

### Requirement: Anti-Activity Guardrail
The system SHALL reject generation of commercial activities, deliverables, or delivery-day estimates when the user mentions tools, assessment types, or service labels, and SHALL invert the prompt toward the intrinsic claim or engineering property being defended.

#### Scenario: Activity mention triggers inversion
- **WHEN** the user mentions a pentest, audit, code review, or day-based consulting request
- **THEN** the system refuses to generate that activity and asks what underlying property or claim it would prove

### Requirement: Structured Scaffold Output
The system SHALL produce a normalized scaffold artifact in JSON containing goals, strategies, contexts, assumptions, principle references, and unsupported leaf goals.

#### Scenario: Session completion emits reusable scaffold
- **WHEN** the scoper finalizes the Socratic session
- **THEN** the system emits a structured scaffold that downstream agents can consume without manual transcript rewriting, including abstraction-layer tags for each claim and gap

### Requirement: Unsupported Leaf Flags
The system SHALL flag leaf goals with `unsupported: true` when the scaffold identifies a claim gap that lacks evidence or sufficient justification.

#### Scenario: Leaf claim is marked unsupported
- **WHEN** a leaf goal has no current evidence or justification
- **THEN** the scaffold marks that goal as unsupported and records its commercial gap type, abstraction layer, or equivalent gap classification

### Requirement: Layer-Aware Consultant Reporting
The system SHALL report unresolved gaps to the consultant with both the principle mapping and the abstraction layer where the confidence gap exists.

#### Scenario: Consultant receives layer-aware gap summary
- **WHEN** the session ends with unsupported claims
- **THEN** the system reports each gap as a principle-layer pair with a brief explanation of whether the gap is component, functional cluster, system, or scenario level

### Requirement: Downstream Handoff Compatibility
The system SHALL provide handoff-compatible outputs so the resulting scaffold can be used by bootstrap, narrative synthesis, top-down architecture flows, and downstream SoW mapping.

#### Scenario: Scaffold is consumable by downstream flows
- **WHEN** the Socratic session output is passed to downstream orchestration
- **THEN** required claim and activity fields are present and parseable for those agents

### Requirement: Bounded Questioning
The system SHALL ask no more than two questions at a time in a single agent turn.

#### Scenario: Question budget is enforced
- **WHEN** the agent composes a Socratic turn
- **THEN** the turn contains at most two questions

### Requirement: Layered Decomposition Prompting
The system SHALL use the four abstraction layers as a Socratic decomposition guide when refining claims.

#### Scenario: High-level claim is drilled down
- **WHEN** the user provides a scenario-level claim
- **THEN** the agent asks for supporting component, functional cluster, and system evidence until the breaking point of the argument is identified
