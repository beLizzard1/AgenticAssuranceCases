## ADDED Requirements

### Requirement: Agent-specific code SHALL be organized per-agent
Agent-specific configuration, manifests, and deployment code SHALL be placed under `agents/<agent-name>/` when feasible. This provides a clear boundary between shared and agent-specific artifacts.

#### Scenario: Developer creates agent artifact
- **WHEN** a developer adds a new deployment manifest for an agent
- **THEN** the file is placed under `agents/<agent-name>/` and the PR is validated against the branch-split policy

### Requirement: Shared libraries SHALL remain in master
Common libraries, utilities, and CI scripts SHALL be maintained in `master`. Agent branches may reference these but SHOULD NOT duplicate core functionality without strong justification.

#### Scenario: Reuse shared library
- **WHEN** an agent needs functionality from a shared library
- **THEN** they reference the shared library in master and document any agent-specific extensions
