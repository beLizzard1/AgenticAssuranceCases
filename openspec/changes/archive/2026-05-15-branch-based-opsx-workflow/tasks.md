## 1. Branch Lifecycle Foundations

- [x] 1.1 Define the branch naming convention and lifecycle rules for OpenSpec changes.
- [x] 1.2 Update apply orchestration so each change starts on a dedicated branch.
- [x] 1.3 Update status/reporting so the active branch or transition state is visible.

## 2. Archive Completion Flow

- [x] 2.1 Update archive orchestration to finalize work from the change branch.
- [x] 2.2 Define how the workflow returns to the base branch after archive.
- [x] 2.3 Retain completed change branches after archive and document the manual cleanup path.

## 3. Validation and Guidance

- [x] 3.1 Add tests for branch creation, branch selection, and archive transition behavior.
- [x] 3.2 Add conflict/error handling for dirty worktrees or branch creation failures.
- [x] 3.3 Add validation for both OpenCode and Pi agent entrypoints so they operate on the same branch.
- [x] 3.4 Document the branch-based workflow so users understand when to expect branch switches.
