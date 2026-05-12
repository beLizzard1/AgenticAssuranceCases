## Context

The repository already has a schema-aware MCP parser and a bottom-up assurance evaluator. This change adds a complementary top-down mode that starts from roots, inspects immediate children, and recurses until the tree is complete enough to hand off to specialist subagents.

## Goals / Non-Goals

**Goals:**
- Add a downward-navigation MCP tool for immediate child inspection.
- Add a root-driven OpenCode agent that walks assurance cases top-down.
- Keep orchestration local and prompt-driven rather than introducing a separate controller service.
- Make recursive delegation to existing specialist subagents explicit.

**Non-Goals:**
- Replacing the existing assurance evaluator.
- Building a graphical tree editor or UI.
- Performing automatic proof synthesis without subagent delegation.

## Decisions

- Add dedicated MCP navigation tools instead of teaching the agent to re-parse the entire `.axml` file.
  - Rationale: immediate-child queries are cheap on the existing NetworkX model and keep the agent token-efficient.
  - Alternative considered: let the agent call `parse_assurance_case` and filter children itself. That duplicates graph logic and scales poorly.

- Add root discovery alongside child discovery as a lightweight graph query.
  - Rationale: a top-down walker needs stable entry points, and root identification should live in the parser layer where structural knowledge already exists.
  - Alternative considered: hard-code root selection in the prompt. That would be brittle and file-specific.

- Keep the top-down architect as a primary OpenCode agent that spawns specialist subagents through `task` permissions.
  - Rationale: the repo already uses prompt-level routing for assurance work, so this keeps the architecture consistent.
  - Alternative considered: a code-driven orchestrator loop. That would centralize control but make the workflow harder to evolve.

- Represent direct descendants as a compact payload that includes node metadata and link type.
  - Rationale: the agent only needs enough structure to decide whether a branch is complete or needs decomposition.
  - Alternative considered: return the full neighborhood graph each time. That is more general, but wastes context for a local traversal.

- Treat unsupported branches as delegation points rather than forcing the architect to invent content itself.
  - Rationale: the point of the agent is structural navigation and gap detection, not replacing the specialist subagents.
  - Alternative considered: let the architect write missing nodes directly. That would blur responsibilities and make review harder.

## Risks / Trade-offs

- Root detection may misclassify unusual ASCE structures -> Use schema-aware structural rules and validate against the example `.axml` file.
- Recursive traversal can revisit nodes in cyclic or densely linked graphs -> Track visited node IDs and impose a depth limit.
- Prompt drift could make the architect too eager or too passive -> Keep the workflow explicit and narrow, with clear stop conditions.
- Adding a second orchestration mode could confuse users -> Name the agent distinctly and document the difference from the existing evaluator.

## Migration Plan

1. Add the MCP child/root navigation tools to the parser service.
2. Add the new `top-down-architect.md` agent and permissions.
3. Validate the agent on the sample `.axml` file and confirm the recursive traversal stays within the intended branch.
4. If needed, remove the new agent file and MCP helpers to roll back.

## Open Questions

- Should the root finder use strict schema rules or a more permissive structural heuristic?
- Do we want the architect to stop at evidence, or also classify unsupported evidence branches for downstream repair?
- Should the recursive loop enforce a maximum depth by default, or leave that to agent judgment?
