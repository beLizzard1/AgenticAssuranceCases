## Context

The current OpenSpec lifecycle keeps change artifacts organized, but the surrounding git strategy is implicit and easy to misread as a harness-specific boundary rather than a real branch-based workflow. That makes it harder to reason about isolation, review boundaries, and what branch a change actually lives on while it is being worked.

This change introduces a branch-first lifecycle for OpenSpec changes so `/opsx-apply` and `/opsx-archive` operate on explicit git branches instead of sharing one ambient working branch.
The same change branch must be shared across OpenCode and the Pi agent; there is no separate branch per entrypoint.

## Goals / Non-Goals

**Goals:**
- Create a dedicated git branch for each applied change.
- Make the active branch visible and deterministic during apply/archive.
- Preserve the existing OpenSpec artifact lifecycle while changing the git transport strategy.
- Keep archive behavior predictable: changes are completed on the change branch, then returned to the base branch state.
- Retain completed change branches after archive unless a human deletes them manually.

**Non-Goals:**
- Reworking the OpenSpec schema or artifact content model.
- Adding remote push/pull automation or hosted branch management.
- Replacing the archive-directory convention with a git-only history model.
- Solving unrelated worktree cleanliness or multi-user collaboration issues beyond the branch lifecycle.

## Decisions

1. Use a change-scoped git branch as the unit of work.
   - Rationale: the branch itself is the clearest isolation boundary and avoids inventing another lifecycle state store.
   - Alternatives considered: a single shared branch with metadata tags; rejected because it preserves the same ambiguity the user wants removed.

2. Keep the OpenSpec change directory structure intact.
   - Rationale: branching should change how work moves through git, not force a parallel artifact migration model.
   - Alternatives considered: moving artifacts into branch-specific directories; rejected because it couples source control concerns to filesystem layout.

3. Let archive complete on the base branch after validating the change branch.
   - Rationale: archive should remain the terminal lifecycle step and leave the repository in a stable default state.
   - Alternatives considered: leaving users on the change branch after archive; rejected because it makes the default continuation state unclear.

4. Keep the branch naming convention simple and change-derived.
   - Rationale: human-readable branch names make status, recovery, and cleanup easier.
   - Alternatives considered: opaque IDs or timestamp-only branch names; rejected because they are harder to map back to a change.

5. Treat the workflow client as an adapter, not a source of truth.
   - Rationale: branch state should live in git and OpenSpec artifacts, so multiple entrypoints can drive the same lifecycle.
   - Alternatives considered: client-specific branch state; rejected because it would recreate a fragmented mental model the proposal is trying to remove.

6. Retain local change branches after archive.
   - Rationale: archive should complete the lifecycle without destructive cleanup, leaving a recovery point intact.
   - Alternatives considered: automatic deletion; rejected because it raises the chance of losing a useful audit/recovery branch.

## Risks / Trade-offs

- [Branch creation can fail if the worktree has conflicting local changes] -> Mitigation: validate state before switching branches and surface a clear pause condition.
- [Archive may become confused with merge semantics] -> Mitigation: define a single completion path and avoid ambiguous “maybe merge, maybe move” behavior.
- [Users may still treat branching as an implementation detail] -> Mitigation: make branch state explicit in status and command output.
- [Branch cleanup may leave stale refs behind] -> Mitigation: document whether archive deletes, retains, or renames the change branch.
- [One client may drift from the other if branch rules are encoded separately] -> Mitigation: define the branch rules once in the OpenSpec workflow contract and require both OpenCode and Pi agent to operate on the same branch.
