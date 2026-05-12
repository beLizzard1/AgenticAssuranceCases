## ADDED Requirements

### Requirement: Adversarial Graph Scanning
The system MUST analyze the assurance case graph as an adversarial red-team pass that searches for defeaters.

#### Scenario: Red-team workflow starts
- **GIVEN** a parsed assurance-case graph
- **WHEN** the adversarial evaluator runs
- **THEN** it MUST use the MCP parser output to select candidate claims, arguments, evidence, and links for attack

### Requirement: Defeater Strategy Routing
The system MUST route weaknesses to the correct defeater strategy.

#### Scenario: Claim attack selection
- **GIVEN** a target claim node
- **WHEN** the adversarial evaluator determines the claim is false or vulnerable
- **THEN** it MUST invoke the rebutting-defeater subagent

#### Scenario: Inference attack selection
- **GIVEN** a target argument or inference link
- **WHEN** the adversarial evaluator determines the reasoning does not hold in context
- **THEN** it MUST invoke the undercutting-defeater subagent

#### Scenario: Evidence attack selection
- **GIVEN** a target evidence node
- **WHEN** the adversarial evaluator determines the evidence is weak, stale, or untrustworthy
- **THEN** it MUST invoke the undermining-defeater subagent

### Requirement: Defeater Node Drafting
The system MUST draft defeater outputs in a schema-compatible form suitable for insertion into the `.axml` network.

#### Scenario: Defeater generation completes
- **GIVEN** a defeater strategy returns a weakness
- **WHEN** the adversarial workflow prepares the result for persistence
- **THEN** it MUST format the output as a Defeater node and preserve the target link context
