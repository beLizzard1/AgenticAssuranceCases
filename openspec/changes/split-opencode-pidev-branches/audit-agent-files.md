# Audit: Agent-specific files

This audit was generated during implementation of the `split-opencode-pidev-branches` change. It lists files that appear agent-specific or related to agents and recommends ownership (opencode / pidev / shared).

Recommendations (quick pass):

- opencode (clone-and-run; existing agent files under .opencode):
  - .opencode/agents/* (all agent docs and skills) — these are opencode agent materials and should remain accessible from the opencode branch and master for shared docs as appropriate.
  - .opencode/commands/* — CLI/docs for opsx commands (shared but closely tied to opencode workflows)

- pidev (pi package related — none exist yet):
  - (none detected) — create agents/pidev/ and add packaging metadata (pi.yaml) and build scripts when ready.

- shared (master):
  - README.md — shared repository README
  - docs/* — shared documentation
  - .github/workflows/* — CI (will be updated to be branch-aware)
  - mcp-server/*, scripts/*, schemas/* — shared infrastructure and tooling

Notes:
- The repository currently contains a rich `.opencode/agents` directory that documents many agents; treat these as opencode-provided agent definitions.
- No existing pi packaging metadata or agents/pidev/ directory was found; this will be created as part of the pidev packaging task.
