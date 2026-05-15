## ADDED Requirements

### Requirement: Shared Workflow Validator
The system SHALL provide a shared validator that checks OpenCode prompts, Pi prompts, and GitHub workflows against the canonical workflow contract.

#### Scenario: Validator scans all surfaces
- **WHEN** the validator runs
- **THEN** it checks the relevant workflow artifacts from `.opencode`, `.pi`, and `.github`

### Requirement: Drift Detection
The system SHALL fail validation when a workflow artifact diverges from the canonical workflow contract.

#### Scenario: Drift is caught
- **WHEN** a prompt or workflow file reintroduces split-harness wording or contradicts branch semantics
- **THEN** the validator reports the mismatch and exits non-zero

### Requirement: CI Enforcement
The system SHALL run the shared validator in GitHub CI so contract drift is blocked before merge.

#### Scenario: Pull requests are checked
- **WHEN** a pull request changes workflow-related files
- **THEN** GitHub Actions executes the shared validator and reports the result to the PR

### Requirement: Actionable Validation Output
The system SHALL report which file and which rule failed so the maintainer can correct the workflow without guessing.

#### Scenario: Validation explains the mismatch
- **WHEN** validation fails
- **THEN** the output identifies the file path and the contract rule that was violated
