Packaging definition and repository evaluation

Goal

Define what we consider "packaging" vs "non-packaging" changes for the opencode/pidev branch split, evaluate the current repository contents against these definitions, and recommend enforcement to protect shared artifacts (agents.md, .opencode/skills/) while allowing packaging differences where appropriate.

Summary definitions

- Packaging changes: files and artifacts whose only purpose is to publish or distribute an agent (metadata, package manifests, build scripts, release manifests). Packaging changes are allowed to differ between agent branches and master where needed.
  - Representative globs:
    - agents/*/pi.yaml
    - agents/*/package.yaml
    - agents/*/build/**
    - agents/*/dist/**
    - agents/*/Dockerfile
    - any file under agents/<agent>/ that is explicitly a packaging artifact (README.md describing package is ok but not normative)

- Non-packaging changes: source code, integration logic, shared libraries, documentation describing the project and skills, CI scripts (unless packaging-only), and any behavioral change. These MUST be synchronized across branches (opencode, pidev, master) unless there is a documented, approved divergence.
  - Representative globs:
    - src/**, mcp-server/**, scripts/**
    - README.md, docs/**, CONTRIBUTING.md
    - .opencode/skills/**
    - .opencode/agents/** (agent docs/content) — treated as agent-surface but should be kept consistent unless intentionally divergent
    - .github/workflows/** (CI correctness is shared; branch-aware workflows may vary but shared checks should remain consistent)

Current repository evaluation (quick pass)

- Packaging artifacts found:
  - agents/pidev/pi.yaml (packaging stub added as part of the change)
  - agents/pidev/README.md

- Packaging artifacts not found:
  - No other explicit package manifests (no agents/*/build/ or dist/ or Dockerfile were found in the repository root in this scan).

- Non-packaging and shared artifacts found:
  - .opencode/skills/* (existing skills docs)
  - README.md, docs/*, mcp-server/*, scripts/*, schemas/* — all shared infra and documentation
  - .opencode/agents/* moved into agents/opencode/* on the opencode branch (these are agent docs / definitions and should be kept consistent across branches where applicable)

Implications and recommended rules

1) Canonical shared artifacts

  - agents.md and .opencode/skills/** are canonical, shared artifacts. They should be identical across branches unless an explicit, approved deviation exists. CI must validate this and the required behavior is:
    - On PRs to any branch, run a skills/docs consistency check comparing .opencode/skills/** and agents.md to master (or canonical branch). If they differ and no documented rationale exists, the check should fail.

2) Packaging isolation

  - Packaging artifacts (files matching packaging globs above) are allowed to be added/modified in agent branches (e.g., agents/pidev/pi.yaml). These should not be considered a trigger for cross-branch sync.

3) Non-packaging change sync

  - Any change that touches non-packaging artifacts (source, shared docs, skills) MUST trigger a sync action. We implemented a CI step that creates an issue when non-packaging changes are detected in a PR/commit so maintainers will manually (or automatically, if configured) propagate those changes to the other branches.
  - Optionally, after approval, the CI can be extended to create sync PRs automatically (requires a write token and precise conflict strategy).

4) Enforcement in CI (recommended)

  - Add branch-split validation workflow to master so PRs to master are validated (already created in pidev; we should merge it into master).
  - Make the skills/docs consistency check blocking (fail the job) after teams agree on the canonical policy.
  - Keep packaging checks non-blocking for agent branches, but document packaging metadata requirements in specs/pidev-integration/spec.md.
  - The sync-trigger script should create issues on detection of non-packaging changes; consider adding an optional automatic PR flow.

5) Ownership and CODEOWNERS

  - Add CODEOWNERS entries for agents/opencode/ and agents/pidev/ to ensure PR approvals for agent-specific files.
  - Add owners for shared directories (docs/, .opencode/skills/) so changes require approval and are reviewed for cross-branch impacts.

6) Process recommendations

  - Before any PR that changes shared artifacts is merged, create corresponding sync PRs to the other branches or use an automated process to do so and attach those PR references in the main PR description.
  - Document the expected procedure in agents.md and CONTRIBUTING.md: how to handle packaging changes vs non-packaging, how to request syncs, and how to document intentional divergences.

Next steps I can take for you

- Produce a draft CODEOWNERS file and open a PR
- Open a PR to merge the branch-split validation workflow into master
- Make the skills/docs check blocking and update the workflow accordingly
- Implement automatic sync PR creation (requires GH token with write access) — I can prepare a safe draft for review

If you want, I will now create the packaging-definition file in the change (done) and can draft the CODEOWNERS and PRs with the options above. Which of the next steps should I take? (short answer: pick one or more)
