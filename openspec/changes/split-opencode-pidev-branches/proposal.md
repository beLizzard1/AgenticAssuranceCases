## Why

The repository currently contains a single branch that mixes framework and agent-specific elements for OpenCode. We need to formally split the work so there are two agent-focused branches: one remaining as the current opencode branch and another tracking the https://pi.dev/ agent. The master branch should retain only common, shared elements. This separation enables independent development, clearer ownership, and easier deployments for each agent while keeping shared infrastructure and policies centralized.

Note on pi.dev: pi.dev enables distribution of "pi packages" that allow sharing and discovery of agents without requiring consumers to clone the repository. The current system requires developers to clone this repo and follow the README; part of this change is to add support for pi packages (for the pidev agent) while preserving the existing clone-and-run developer workflow for opencode.

## What Changes

- Create two long-lived branches: `opencode` (existing layout) and `pidev` (for https://pi.dev/ integration).
- Move agent-specific code, configs, and deployment manifests into their respective branches.
- Keep shared libraries, CI configuration, documentation, and policy in `master`.
- Add documentation and gating rules to ensure future agent-specific changes are developed in their branch and merged into master only for shared changes.

**BREAKING**: Branch naming and workflow changes. Existing CI workflows and deployment scripts that assume a single main branch will need to be updated.

## Capabilities

### New Capabilities
- `branch-split-policy`: Define the branching policy, naming conventions, and rules for what stays in master vs agent branches.
- `agent-branch-structure`: Directory and file placement guidelines for agent-specific vs shared code. This becomes a spec that enforces what can be modified in agent branches.

- `pidev-integration`: Guidelines and requirements for creating and publishing pi packages so the pidev agent can be consumed via pi.dev instead of cloning the repo.

- `opencode-integration`: Ensure the opencode agent continues to support the existing clone-and-run workflow; optionally document packaging or distribution mechanisms if desired.

### Modified Capabilities
- `ci-workflows`: CI workflows will be adapted to handle branch-specific pipelines. (Requires updating existing workflow specs.)

## Impact

- Affected code: repo layout, deployment manifests, CI workflows, documentation, and any scripts that reference the default branch.
- Dependencies: CI/CD pipelines, deployment tooling, and external integration point at https://pi.dev/.
- Systems: Build and release processes will need small updates to produce agent-specific artifacts.
