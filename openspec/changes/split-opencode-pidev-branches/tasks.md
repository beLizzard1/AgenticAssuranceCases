## Tasks

This section lists the implementation steps required to make the branch-split policy live.

1. Audit repository for agent-specific artifacts

- [ ] Audit the repository and produce a list of agent-specific files with suggested ownership (opencode or pidev)
  - Owner: repo maintainers
  - Output: list of files with suggested agent ownership (opencode or pidev)

2. Create long-lived branches

- [ ] Create `opencode` branch and push to origin
- [ ] Create `pidev` branch and push to origin
  - Owner: repo maintainers
  - Steps:
    - git checkout -b opencode
    - git push -u origin opencode
    - git checkout -b pidev
    - git push -u origin pidev

3. Move agent-specific files into agent directories (per branch)

- [ ] Create `agents/<agent>/` directories and move agent-specific manifests/configs for opencode
- [ ] Create `agents/pidev/` and add packaging metadata and build scripts for pidev
  - Owner: agent teams
  - Steps (per branch):
    - Create `agents/<agent>/` directory where missing
    - Move manifests/configs into `agents/<agent>/` or leave in place if historical reasons demand
    - Commit changes and open PRs if needed

4. Add `agents.md` documentation

- [ ] Add `agents.md` that documents branch-split policy, agent layout, and examples
  - Owner: repo maintainers
  - Content: branch-split policy, examples, how to structure files, examples of PRs

5. Implement openspec validation rule

- [ ] Add a validation script `scripts/validate-branch-split.sh` that checks modified files against policy
- [ ] Integrate the validation script with openspec/CI so PRs run the check
  - Owner: infra team
  - Steps:
    - Add a validation script that checks modified files against policy
    - Integrate with `openspec` by adding a hook or a check command used in CI

   - Add a validation that also checks for presence and correctness of pi packaging metadata when changes occur in `agents/pidev/`.

6. Update GitHub CI workflows

- [ ] Add branch-aware workflows that run the validation script on PRs
- [ ] Ensure PRs to master run the validation script to prevent agent-specific files landing in master
  - Owner: infra team
  - Steps:
    - Add branch-aware workflows in `.github/workflows/` that run the validation script
    - Ensure that PRs to master run the validation script to prevent agent-specific files landing in master

7. Create CODEOWNERS and branch protection rules

- [ ] Add CODEOWNERS entries for `agents/opencode/` and `agents/pidev/`
- [ ] Configure branch protection rules for `opencode` and `pidev` to require PRs and approvals
  - Owner: repo maintainers
  - Steps:
    - Add CODEOWNERS entries for `agents/opencode/` and `agents/pidev/`
    - Configure branch protection rules for `opencode` and `pidev` to require PRs and approvals

8. Update contributing docs and developer onboarding

- [ ] Update CONTRIBUTING.md with branch workflow guidance
- [ ] Add examples to `agents.md` for both clone-and-run and pi package consumption
  - Owner: repo maintainers
  - Steps:
    - Add notes to CONTRIBUTING.md about branch workflow
    - Add examples to `agents.md`

9. Run integration tests and iterate

- [ ] Open PRs in both branches, run CI, and fix any issues found
  - Owner: infra and agent teams
  - Steps:
    - Open PRs in both branches, run CI, and fix any issues

10. Finalize and communicate

- [ ] Announce branch policy, link docs, and provide support window for teams to migrate
  - Owner: repo maintainers
  - Steps: Announce branch policy, link docs, and provide support window for teams to migrate
