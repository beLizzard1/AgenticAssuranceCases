## Why

The current OpenSpec apply/archive flow is easy to reason about for artifacts, but it leaves the git strategy implicit and spread across different mental models. We need the change lifecycle itself to be branch-oriented so each change can be worked, reviewed, and archived with clearer isolation and less ambiguity about what gets merged where. The important part is that both OpenCode and the Pi agent should work on the same change branch, not separate branches.

## What Changes

- Make `/opsx-apply` create or switch to a dedicated branch for the selected change before implementation starts.
- Make `/opsx-archive` finalize work on that change branch and move or record the completed change from a branch-aware state.
- Define branch naming, branch ownership, and handoff behavior so change work stays isolated from the main branch until the lifecycle step is complete.
- Keep both OpenCode and the Pi agent on the same shared change branch.
- Retain completed change branches after archive so cleanup stays explicit.
- Preserve the existing OpenSpec artifact flow while changing the git transport strategy behind it.

## Capabilities

### New Capabilities
- `branch-based-change-lifecycle`: Branch-aware apply and archive workflow for OpenSpec changes, including branch creation, branch selection, and archive-time branch completion rules.

### Modified Capabilities
- None.

## Impact

- Affected code: OpenSpec workflow commands, branch orchestration, archive handling, and any state tracking that assumes a single main-branch working model.
- APIs/contracts: change lifecycle commands may need to expose the active branch and branch transition state.
- Dependencies: git branch operations become part of the workflow contract.
- Systems/process: change work becomes isolated per branch, reducing cross-change interference and clarifying when a change is ready to merge or archive. OpenCode and Pi agent both operate on the same branch, and completed branches remain available for manual cleanup or inspection.
