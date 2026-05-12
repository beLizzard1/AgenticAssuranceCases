## ADDED Requirements

### Requirement: Structured bootstrap context
The system SHALL derive a structured shared context from the supplied item definition, operational context, assurance scope, threat context, and assets before generating assurance claims.

#### Scenario: Context is captured first
- **WHEN** a user provides a system description and assurance intent
- **THEN** the system SHALL record the relevant context fields in a structured form
- **AND** the system SHALL defer claim synthesis until that context exists

### Requirement: Explicit assurance strategy
The system SHALL select and record an explicit assurance strategy for the bootstrap case, such as decomposition, lifecycle, threat-oriented, standards-oriented, capability-oriented, evidence-led, risk-oriented, or hybrid.

#### Scenario: Strategy is visible in the case
- **WHEN** the bootstrap workflow begins case synthesis
- **THEN** the system SHALL attach a strategy node or equivalent representation to the case
- **AND** the selected strategy SHALL be available for later review and refinement

### Requirement: Bounded top-level claim synthesis
The system SHALL synthesize one or more bounded top-level claims that include scope, context, proportionality, operational framing, and lifecycle framing.

#### Scenario: Claim avoids overstatement
- **WHEN** the system creates the initial top-level claim
- **THEN** the claim SHALL be limited to the described system and context
- **AND** the claim SHALL NOT imply completeness or certification readiness

### Requirement: Sparse initial graph generation
The system SHALL generate an initial assurance-case graph containing claims, arguments, assumptions, contexts, evidence placeholders, and defeaters, while remaining sparse enough to expose unresolved uncertainty.

#### Scenario: Missing evidence is not hidden
- **WHEN** the system lacks supporting evidence for a branch of the case
- **THEN** the system SHALL create an explicit evidence placeholder or gap node
- **AND** the system SHALL preserve the unresolved state instead of inventing support

### Requirement: Evidence discovery and binding
The system SHALL attach known evidence to the bootstrap case when available and SHALL classify or expose missing evidence needs when evidence is absent.

#### Scenario: Existing evidence is reused
- **WHEN** test reports, architecture documents, requirements, or similar artifacts are available
- **THEN** the system SHALL link them into the case as supporting evidence
- **AND** the system SHALL identify any remaining evidence gaps

### Requirement: Defeater generation
The system SHALL generate adversarial review material for major top-level branches, including rebutting, undercutting, or undermining defeaters where uncertainty or risk exists.

#### Scenario: Branches receive challenge material
- **WHEN** a major argument branch is synthesized
- **THEN** the system SHALL create at least one relevant defeater when the branch depends on assumptions, weak evidence, or contextual mismatch

### Requirement: Bootstrap summary output
The system SHALL produce a human-readable summary of the bootstrap case, including the assurance strategy, evidence needs, and unresolved gaps.

#### Scenario: Reviewers can inspect the result
- **WHEN** the bootstrap workflow completes
- **THEN** the system SHALL provide a concise summary suitable for a human reviewer
- **AND** the summary SHALL identify the main uncertainties that still require follow-up

### Requirement: Reusable pattern instantiation
The system SHALL support instantiating reusable bootstrap patterns or templates for common assurance contexts without hard-coding a single argument structure.

#### Scenario: Pattern is adapted to the system
- **WHEN** the user selects or the system infers a bootstrap pattern
- **THEN** the resulting case SHALL reflect the supplied system context rather than a generic canned tree
