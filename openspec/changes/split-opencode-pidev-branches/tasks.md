## Tasks

Implementation checklist for change: split-opencode-pidev-branches

1. Audit repository for agent-specific artifacts

- [x] Audit the repository and produce a list of agent-specific files with suggested ownership (opencode or pidev)
  - Output: openspec/changes/split-opencode-pidev-branches/audit-agent-files.md

2. Create long-lived branches

- [x] Create `opencode` branch and push to origin
- [x] Create `pidev` branch and push to origin

3. Move agent-specific files into agent directories (per branch)

- [x] Create `agents/opencode/` and move agent-specific manifests/configs for opencode
- [x] Create `agents/pidev/` and add packaging metadata and build scripts for pidev

4. Add `agents.md` documentation

- [x] Add `agents.md` that documents branch-split policy, agent layout, and examples

5. Implement openspec validation rule

- [x] Add a validation script `scripts/validate-branch-split.sh` that checks modified files against policy
- [x] Integrate the validation script with CI so PRs run the check (workflow added)

6. Update GitHub CI workflows

- [x] Add branch-aware workflows that run the validation script on PRs
- [ ] Ensure PRs to master run the validation script to prevent agent-specific files landing in master (workflow needs to be present on master)

7. Create CODEOWNERS and branch protection rules

- [ ] Add CODEOWNERS entries for `agents/opencode/` and `agents/pidev/`
- [ ] Configure branch protection rules for `opencode` and `pidev` to require PRs and approvals

8. Update contributing docs and developer onboarding

- [ ] Update CONTRIBUTING.md with branch workflow guidance
- [ ] Add examples to `agents.md` for both clone-and-run and pi package consumption

9. Run integration tests and iterate

- [ ] Open PRs in both branches, run CI, and fix any issues found

10. Finalize and communicate

- [ ] Announce branch policy, link docs, and provide support window for teams to migrate
