## Context

The repository already defines a local MCP server in `opencode.json` and documents it as the way OpenCode should access `.axml` tooling. The reported regression is that the server does not appear to start when OpenCode opens the workspace, which leaves the session without the structured AXML tools.

The implementation should stay small and focused on startup reliability. This is not a parser rewrite or a change to the assurance-case model.

## Goals / Non-Goals

**Goals:**
- Make the local AXML MCP server start reliably during OpenCode workspace launch.
- Ensure startup failures are visible instead of silently degrading the session.
- Keep the change confined to startup/configuration behavior.

**Non-Goals:**
- Redesign the AXML parser or its tool surface.
- Change assurance-case data structures or `.axml` semantics.
- Add new MCP capabilities unrelated to startup.

## Decisions

- Keep the server configured as a local OpenCode MCP entry rather than moving startup into a separate orchestration layer.
  - Rationale: OpenCode already owns workspace-level MCP lifecycle, so the smallest fix is to make that existing path dependable.
  - Alternatives considered: a custom bootstrap daemon or manual launch instructions. Both add operational overhead and weaken the default experience.

- Make the launch command/path explicit and workspace-root aware.
  - Rationale: startup issues often come from ambiguous working directories or environment assumptions. A deterministic entrypoint is easier to reason about and diagnose.
  - Alternatives considered: rely on implicit shell resolution or hidden environment setup. That is less portable and harder to debug.

- Treat startup observability as part of the fix.
  - Rationale: if the server fails to start, users need a clear signal rather than a silent absence of tools.
  - Alternatives considered: retry-only behavior or no reporting. Those hide the problem and make the failure look like a tooling gap.

## Risks / Trade-offs

- [The local Python entrypoint may still depend on the user's environment] → Verify the command is stable from a clean workspace launch and document any required interpreter/dependency setup.
- [OpenCode may resolve relative paths differently than an interactive shell] → Keep the startup path explicit and validate it from the repo root.
- [Error reporting could be too noisy] → Limit startup diagnostics to launch/registration failures and keep successful startup quiet.

## Migration Plan

1. Update the startup configuration or entrypoint so OpenCode can launch the local AXML MCP server consistently.
2. Verify the server is registered on workspace open.
3. Confirm a failed launch produces a visible error instead of a silent missing tool.
4. Roll back by restoring the previous startup configuration if the new entrypoint is not reliable in practice.

## Open Questions

- Should the startup command continue to use the system `python` interpreter, or should it point to a repo-managed environment for more deterministic launches?
- Do we want explicit startup logging in the server process itself, or is OpenCode-side failure reporting sufficient?
