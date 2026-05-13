## Context

The repo currently mixes shared framework code and agent-specific integrations. This design creates a branching strategy and repository layout that keeps shared components in `master` while allowing agent teams to maintain their own branches (`opencode` and `pidev`) for agent-specific code, configs, and deployment artifacts.

Constraints:
- Preserve history where possible; avoid deleting existing files in master unless clearly shared.
- Minimize disruption to CI; provide transitional compatibility where feasible.

## Goals / Non-Goals

**Goals:**
- Establish two agent branches: `opencode` and `pidev`.
- Define a clear rule-set for what belongs in `master` vs agent branches.
- Provide migration steps and CI updates to support branch-specific pipelines.

**Non-Goals:**
- Rewriting the entire repository structure. Focus on policy and selective movement of agent-specific artifacts.

## Decisions

- Branches: Create `opencode` and `pidev`. `master` holds shared code and infra.
- Directory layout: Keep existing layout in master. In agent branches, place agent-specific files under a top-level agent directory when feasible (e.g., `agents/opencode/`, `agents/pidev/`) or keep in their previous paths but gated by branch protection rules.
- CI: Add branch-aware workflows in .github/workflows that detect branch and run agent-specific steps. Keep common checks in shared workflows triggered on PRs to master.

- pi.dev integration: For the pidev branch, include packaging and metadata needed to publish a pi package. The package layout SHALL include metadata files (e.g., `pi.yaml` or equivalent), a build step to produce the package, and publishing instructions. Keep pi packaging artifacts isolated to the `pidev` branch and/or `agents/pidev/` directory to avoid exposing packaging metadata in master unless shared.

Alternatives considered:
- Using monorepo subfolders for agents vs branch separation. Chosen branch separation to allow divergent experimental changes per agent while preserving master for stable shared elements.

## Risks / Trade-offs

- [Risk] Developers may accidentally push agent-specific changes to master. → Mitigation: Add branch protection and CODEOWNERS entries; update contributing docs.
- [Risk] CI complexity increases as workflows become branch-aware. → Mitigation: Keep common checks centralized and modularize agent steps.
- [Risk] Some shared files may be duplicated across branches. → Mitigation: Prefer symlinks or scripts that assemble artifacts at build time; document clearly.

## Migration Plan

1. Audit repository to identify agent-specific files and owner suggestions (quick pass).
2. Create `opencode` and `pidev` branches from current HEAD.
3. In each branch, move agent-specific configs/manifests into `agents/<agent-name>/` or an agreed layout.
4. Update CI workflows to be branch-aware. Add gating rules and CODEOWNERS.
5. Create `branch-split-policy` and `agent-branch-structure` spec files (in this change's specs) and add documentation.
6. Run integration tests on both branches; iterate on CI fixes.
7. Communicate with teams and update developer onboarding docs.

Rollback: If issues occur, revert branch changes and revert CI workflow updates.

## Open Questions

- Should we enforce agent layout via automated lints or pre-commit hooks? Recommended yes, but requires scripting.
- Where to place agent-specific Docker images and registries—central or per-agent? Leave to team preference.

## Enforcement

To make the policy effective, enforce it at three levels:

- openspec validation: Add a ruleset or validation hooks in the repository's OpenSpec configuration so that `openspec` commands can detect policy violations (e.g., agent files modified in master). This may be implemented as extra spec checks or a validation script invoked by openspec tooling.
- agents.md: Add a top-level `agents.md` (or `docs/agents.md`) that documents the policy, agent directory layout, and examples. This file will be referenced by CI and by developer onboarding.
- GitHub CI rules: Add branch-aware workflows and a lightweight validation step (script) that runs on PRs to master and agent branches. The validation step should fail the PR if files violating the branch-split policy are detected.

These enforcement mechanisms together reduce accidental policy violations and make the workflow discoverable for developers.
