## 1. Canonical Contract

- [x] 1.1 Define the canonical workflow contract for OpenSpec apply/archive behavior.
- [x] 1.2 Capture the shared branch, archive, and retention semantics in spec form.

## 2. Shared Validator

- [x] 2.1 Implement a shared validator script for `.opencode`, `.pi`, and `.github` workflow artifacts.
- [x] 2.2 Make the validator report file-level and rule-level drift clearly.

## 3. CI Enforcement

- [x] 3.1 Wire the validator into GitHub Actions for pull requests and main-branch pushes.
- [x] 3.2 Remove or replace legacy split-harness checks with contract-based validation.

## 4. Workflow Alignment

- [x] 4.1 Update OpenCode workflow docs to match the canonical contract.
- [x] 4.2 Update Pi workflow docs to match the canonical contract.
- [x] 4.3 Update GitHub workflow files to reference the shared validator and shared contract.
