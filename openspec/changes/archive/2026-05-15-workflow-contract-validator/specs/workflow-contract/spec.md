## ADDED Requirements

### Requirement: Canonical Workflow Contract
The system SHALL define a canonical workflow contract that describes OpenSpec apply/archive behavior once and treats that contract as the source of truth for entrypoints.

#### Scenario: Shared contract is available
- **WHEN** a maintainer inspects the workflow rules for OpenSpec apply/archive behavior
- **THEN** there is one canonical contract describing the expected branch and archive lifecycle

### Requirement: Shared Change Branch Semantics
The system SHALL require OpenCode, Pi agent, and GitHub workflows to operate on the same change branch for a given OpenSpec change.

#### Scenario: Multiple entrypoints use one branch
- **WHEN** the same change is started from OpenCode, Pi agent, or a GitHub workflow
- **THEN** all entrypoints refer to the same change branch rather than separate entrypoint-specific branches

### Requirement: Branch Transition Semantics
The system SHALL describe branch creation, archive transition, and return-to-base behavior as part of the workflow contract.

#### Scenario: Archive follows the shared contract
- **WHEN** a completed change is archived
- **THEN** the workflow contract states how the active branch transitions back to the base branch and how the change branch is retained or cleaned up

### Requirement: No Split-Harness Wording
The system SHALL avoid workflow language that implies OpenCode and Pi agent use separate lifecycle branches for the same change.

#### Scenario: Wording stays aligned
- **WHEN** a workflow prompt or GitHub check describes change lifecycle behavior
- **THEN** it uses shared branch lifecycle language rather than split-harness wording
