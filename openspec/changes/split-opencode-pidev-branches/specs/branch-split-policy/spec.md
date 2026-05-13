## ADDED Requirements

### Requirement: Repository MUST define a branch-split policy
The repository SHALL document the policy that specifies which artifacts belong in `master` (shared) versus agent branches (agent-specific). The policy SHALL include naming conventions, merge procedures, and ownership.

#### Scenario: Developer reviews policy
- **WHEN** a developer reads the repository CONTRIBUTING.md
- **THEN** they can find the branch-split policy and rules for where to place agent-specific changes

### Requirement: Branch protection for agent branches
Agent branches SHALL have branch protection rules that prevent direct pushes and require PR approvals from CODEOWNERS for agent-specific files.

#### Scenario: Enforce protection
- **WHEN** a developer opens a PR modifying agent-specific files
- **THEN** the PR must require at least one approval from the appropriate code owner and pass CI checks
