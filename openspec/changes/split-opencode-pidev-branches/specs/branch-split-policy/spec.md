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

### Requirement: Agents documentation and skills SHALL be consistent across branches
The repository SHALL ensure that agent documentation (agents.md) and skills documentation (.opencode/skills/*) are identical across agent branches and master where applicable. Any intentional divergence MUST be documented and approved.

#### Scenario: Docs consistency
- **WHEN** a PR modifies agents.md or files under .opencode/skills/
- **THEN** CI MUST validate that the changes maintain consistency with the canonical copies or include an explicit rationale for divergence
