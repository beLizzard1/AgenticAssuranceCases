## Context

The repository has multiple surfaces that describe the same lifecycle: OpenCode command docs, Pi prompt docs, GitHub workflows, and OpenSpec artifacts. Without a single contract and validator, those surfaces drift independently and reintroduce the exact split-harness model this repo is trying to move away from.

## Goals / Non-Goals

**Goals:**
- Define a canonical workflow contract for apply/archive behavior.
- Validate `.opencode`, `.pi`, and `.github` artifacts against that contract.
- Make drift visible in CI before it lands on `main`.
- Keep the validator simple enough to maintain alongside the repo.

**Non-Goals:**
- Generating prompts or workflows automatically.
- Replacing the OpenSpec artifact system.
- Introducing a new runtime service or daemon.
- Enforcing policy beyond the workflow surfaces in scope.

## Decisions

1. Keep the contract as a human-readable OpenSpec spec.
   - Rationale: the workflow rules need to be inspectable and reviewable, not hidden in generated code.
   - Alternatives considered: embedding the rules only in scripts; rejected because that makes the policy harder to review.

2. Implement the validator as a shared local script.
   - Rationale: one script can be invoked by GitHub Actions and by maintainers locally, reducing duplication.
   - Alternatives considered: separate validators per surface; rejected because it would recreate drift.

3. Validate semantic checkpoints, not every phrase.
   - Rationale: exact wording is brittle; a small set of required checkpoints is easier to keep stable.
   - Alternatives considered: strict string matching only; rejected because minor wording edits would create noise.

4. Make CI fail fast on drift.
   - Rationale: workflow policy is part of the repo’s contract and should block merge when it regresses.
   - Alternatives considered: warning-only checks; rejected because they let drift accumulate.

## Risks / Trade-offs

- [Validator checks may be too strict] -> Mitigation: validate semantic checkpoints and keep the contract small.
- [Contract may become the new source of duplication] -> Mitigation: treat it as the single source of truth and keep prompts/workflows thin.
- [CI can be noisy on wording changes] -> Mitigation: report file and rule context so fixes are obvious.
- [The validator may lag behind new workflow surfaces] -> Mitigation: update the contract whenever a new workflow entrypoint is added.

## Migration Plan

1. Add the canonical workflow contract spec.
2. Add the shared validator script.
3. Wire GitHub Actions to run the validator on pull requests and main pushes.
4. Update OpenCode and Pi workflow docs to match the contract.
5. Remove any stale split-harness wording that the validator catches.

## Open Questions

- Should the validator be shell-based, Python-based, or a small Node script?
- Which workflow checkpoints should be required in v1 versus deferred?
- Should contract checks run on every workflow-related file change or only in CI on PRs?
