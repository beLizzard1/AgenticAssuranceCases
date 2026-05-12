## Why

Assurance 2.0 works best when claims are actively stress-tested rather than only confirmed. This change adds a red-team pass that searches for rebutting, undercutting, and undermining defeaters so assurance cases can be challenged with the same rigor used to build them.

## What Changes

- Add a primary adversarial agent that inspects the assurance graph and chooses a defeater strategy.
- Add three specialist defeater subagents for rebutting, undercutting, and undermining attacks.
- Reuse the existing schema-aware MCP parser and write-back path to target claims, arguments, evidence, and links.
- Allow the adversarial workflow to draft Defeater nodes for insertion into the `.axml` network.
- **BREAKING**: the assurance workflow becomes two-pass, with a builder pass and a red-team pass.

## Capabilities

### New Capabilities
- `adversarial-defeater-analysis`: Red-team scanning of CAE graphs to generate schema-aware defeaters and target weak claims, inferences, or evidence.

### Modified Capabilities

- None.

## Impact

- New `.opencode/agents/` markdown files for the adversarial router and subagents.
- Possible updates to agent wiring and permissions in OpenCode configuration.
- Existing MCP parser/write-back tooling is reused for graph inspection and editing.
