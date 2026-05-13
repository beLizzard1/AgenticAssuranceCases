# Agent Promotion Policy

When an agent branch (e.g., `opencode`, `pidev`) contains changes to non-packaging artifacts (code, shared docs, skills), these changes must be promoted to `main` (master) and reviewed before becoming canonical.

Promotion process

1. Developer opens a PR on the agent branch with their change.
2. CI will detect non-packaging changes and automatically open a promotion PR from the agent branch to `main`.
3. Reviewers evaluate the promotion PR on `main`. If accepted, reviewers merge it into `main` and master becomes the canonical source.
4. After merge, CI will attempt to propagate the master changes back into the agent branches via sync PRs.

Notes

- Packaging-only changes (e.g., `agents/pidev/pi.yaml`, build artifacts) may remain in the agent branch and do not require promotion.
- Intentional divergences to skills/docs must be documented in `agents.md` and approved via PR.
