## ADDED Requirements

### Requirement: Challenger Taxonomy Packet
The system MUST provide the challenger agent with a prompt-ready taxonomy packet organized into a taxonomy layer, a playbook layer, and concrete prompt examples.

#### Scenario: Challenger starts a defeater pass
- **WHEN** the challenger agent begins a defeater-generation pass
- **THEN** it MUST receive a packet that includes category definitions, cues, route mappings, example phrasing, execution rules, and concrete examples
- **AND THEN** it MUST be able to use that packet without needing to infer what the labels mean

### Requirement: Taxonomy Packet Structure
The system MUST provide the challenger agent with a prompt-ready defeater taxonomy packet that includes category names, definitions, look-for cues, typical defeater questions, example phrasing, and route mappings.

#### Scenario: Challenger receives taxonomy context
- **WHEN** the challenger agent starts a defeater-generation pass
- **THEN** it MUST receive a taxonomy packet with enough structure to interpret the categories without guessing their meaning
- **AND THEN** it MUST be able to use the packet as direct prompt context

### Requirement: Route-First Playbook
The system MUST provide a playbook that instructs the challenger to identify the argument route type first and then apply the most relevant defeater category.

#### Scenario: Challenger reviews an argument
- **WHEN** the challenger agent encounters a claim, argument, or evidence node
- **THEN** it MUST first identify the route type or argument step being used
- **AND THEN** it MUST select the matching defeater category before considering cross-cutting security or control overlays
- **AND THEN** it MUST prefer the most specific category and may generate one defeater per independent loss mode when needed

### Requirement: Concrete Challenger Examples
The system MUST include concrete prompt examples that show how the challenger should map an Architect claim to a route type, select the correct category, and draft a refutable defeater.

#### Scenario: Challenger uses the examples
- **WHEN** the challenger agent reads the packet examples
- **THEN** it MUST be able to follow the illustrated path from route detection to defeater drafting
- **AND THEN** it MUST preserve the "Unless ..." style of specific, refutable counter-claims

### Requirement: Specific Refutable Guardrails
The challenger MUST generate defeaters that are specific, refutable, and tied to a plausible loss, safety, security, or reliability impact.

#### Scenario: Challenger drafts a defeater
- **WHEN** the challenger writes a defeater
- **THEN** it MUST avoid generic statements like "this might be unsafe"
- **AND THEN** it MUST state a concrete condition that would make the claim unsupported or false
- **AND THEN** it MUST discard candidate defeaters that do not lead to a meaningful loss or assurance gap

### Requirement: Security and Control Overlays
The taxonomy MUST support cross-cutting overlays such as STRIDE-style security categories and STPA-Sec control scenarios when the claim involves external interfaces, data transfer, or control logic.

#### Scenario: Challenger inspects a system with interfaces or control actions
- **WHEN** the challenger agent sees a claim involving external interfaces, data transfer, or control actions
- **THEN** it MUST consider STRIDE-style or STPA-Sec categories in addition to the route-specific structural category
- **AND THEN** it MUST retain the most specific applicable defeater framing

### Requirement: Structured Defeater Taxonomy
The system MUST provide the challenger agent with a structured defeater taxonomy that categorizes common weakness patterns in assurance cases.

#### Scenario: Challenger begins an attack pass
- **WHEN** the challenger agent starts evaluating a claim, argument, or evidence node
- **THEN** it MUST receive a categorized defeater taxonomy as context
- **AND THEN** it MUST use that taxonomy to guide the search for counter-claims and weak points, including categories inspired by threat modeling techniques such as STRIDE and operational concerns such as resiliency and recovery

### Requirement: Literature-Backed Defeater Families
The taxonomy MUST include seven broad assurance defeater families derived from real-world assurance-case analysis: evidence gaps, reasoning fallacies, contextual assumptions, human and organizational factors, environmental dynamics, system evolution, and external threats.

#### Scenario: Challenger inspects a claim
- **WHEN** the challenger agent reviews a claim or sub-claim
- **THEN** it MUST be able to classify the weakness using one of the literature-backed defeater families
- **AND THEN** it MUST be able to surface evidence-gap, fallacy, assumption, environment, evolution, human/process, or external threat concerns as appropriate

### Requirement: Assurance 2.0 Step Routing
The taxonomy MUST include step-based challenge modes aligned with Assurance 2.0 argument construction steps.

#### Scenario: Challenger reviews an argument step
- **WHEN** the challenger agent encounters decomposition, substitution, concretion, evidence incorporation, or calculation in the assurance argument
- **THEN** it MUST be able to route the challenge to the corresponding defeater mode for that step
- **AND THEN** it MUST express the challenge in terms of incompleteness, invalid proxy, semantic gap, evidence deficit, or model error as appropriate

### Requirement: STPA-Sec Security Scenarios
The taxonomy MUST include STPA-Sec style loss scenarios as a security-oriented sub-taxonomy for transport and CNI assurance cases.

#### Scenario: Challenger reviews control-related claims
- **WHEN** the challenger agent evaluates resiliency or recovery claims in a control-heavy system
- **THEN** it MUST be able to frame defeaters using unsafe control action and loss-scenario language
- **AND THEN** it MUST distinguish these from generic external threats when the distinction matters

### Requirement: Taxonomy-Guided Challenger Reasoning
The system MUST use the defeater taxonomy to make challenger output more systematic than unconstrained zero-shot prompting.

#### Scenario: Challenger drafts a defeater
- **WHEN** the challenger agent generates a defeater draft
- **THEN** it MUST consider the taxonomy categories as part of its reasoning
- **AND THEN** it SHOULD align the draft with the most relevant defeater category before returning it

### Requirement: Taxonomy Extensibility
The defeater taxonomy MUST be easy to revise as the assurance workflow evolves.

#### Scenario: New weakness pattern is discovered
- **WHEN** a new class of assurance weakness becomes relevant
- **THEN** the taxonomy MUST be updateable without changing the challenger agent's core logic
- **AND THEN** the updated taxonomy MUST remain available as structured context for later challenger runs
