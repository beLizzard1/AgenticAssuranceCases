## Why

The repo now expresses the same OpenSpec lifecycle in several places: OpenCode prompts, Pi prompts, GitHub workflows, and OpenSpec change artifacts. That duplication makes drift likely, especially around shared branch semantics, archive behavior, and leftover split-harness wording.

## What Changes

- Define one canonical workflow contract for OpenSpec apply/archive behavior.
- Add a shared validator that checks `.opencode`, `.pi`, and `.github` artifacts against that contract.
- Remove harness-specific split wording and normalize everything to the same shared change-branch lifecycle.
- Fail CI when the documented workflow diverges from the contract.
- Keep the contract readable as source-of-truth, not generated noise.

## Capabilities

### New Capabilities
- `workflow-contract`: Shared lifecycle rules for OpenSpec apply/archive behavior across all entrypoints.
- `workflow-contract-validation`: Shared validator that checks OpenCode, Pi, and GitHub workflow artifacts against the contract.

### Modified Capabilities
- None.

## Impact

- Affected code: workflow docs, prompt files, GitHub workflow files, and a shared validation script.
- APIs/contracts: CI should surface contract drift clearly enough for humans to fix the workflow text.
- Dependencies: the validator becomes a shared local check invoked from GitHub Actions.
- Systems/process: one policy, multiple entrypoints, with less risk of branch/lifecycle drift.
