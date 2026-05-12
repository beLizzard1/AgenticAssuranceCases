## Context

The repository already has specialized assurance agents and an MCP server that exposes graph-aware AXML tools. What is missing is a shared, reusable skill that tells agents when to use those tools, how to discover them, and when direct file edits are inappropriate. This change sits at the boundary between agent guidance and the MCP server contract.

## Goals / Non-Goals

**Goals:**
- Provide one canonical skill for AXML MCP usage across assurance-case tasks.
- Make the MCP server the default semantic interface for structural case work.
- Keep the skill focused on guidance and routing, not on implementing new server features.
- Encourage tool discovery and conservative fallback behavior when tool names or capabilities are uncertain.

**Non-Goals:**
- Adding new MCP server endpoints.
- Rewriting existing specialized agents.
- Mandating MCP for purely editorial text that is not tied to a formal assurance-case node.
- Defining every possible export format in detail inside the skill.

## Decisions

- Create a dedicated OpenCode skill instead of embedding the guidance only in existing agents.
  - Rationale: the MCP usage model should be reusable across multiple agents and future workflows.
  - Alternatives considered: duplicating instructions in each agent or relying on README prose. Both drift over time and are harder to keep consistent.

- Treat the AXML MCP server as the semantic source of truth for structural assurance-case work.
  - Rationale: parsing, validation, graph inspection, and structural mutation belong to the server, not freeform text edits.
  - Alternatives considered: allowing raw XML edits as an equal path. That weakens traceability and makes tooling behavior inconsistent.

- Require tool discovery before assuming exact tool names.
  - Rationale: MCP surfaces can change, and the skill should remain robust to renamed or extended tools.
  - Alternatives considered: hard-coding specific tool names in the skill. That is brittle and reduces portability.

- Keep a narrow exception for purely editorial changes outside formal assurance-case nodes.
  - Rationale: not every wording tweak needs graph-level semantics.
  - Alternatives considered: forcing all text changes through MCP. That would be unnecessarily heavy for documentation-only edits.

## Risks / Trade-offs

- [Overlapping guidance] -> The skill may partially duplicate existing agent docs. Mitigation: keep it focused on MCP selection and usage patterns, and reference specialized agents for domain-specific behavior.
- [Tool-name drift] -> The MCP server tool set may evolve. Mitigation: instruct discovery-first usage rather than assuming fixed names.
- [Overreach] -> Agents may try to route non-semantic edits through MCP. Mitigation: explicitly scope the skill to formal assurance-case structure and validation tasks.
- [Adoption gap] -> Agents may ignore the new skill if it is not surfaced in repo docs. Mitigation: add a short reference in README and existing agent guidance.

## Migration Plan

1. Add the AXML MCP skill file under `.opencode/skills/`.
2. Point the repo README and relevant agent docs at the new skill.
3. Keep existing MCP tools and agents unchanged so the new skill can be adopted incrementally.
4. If the skill needs refinement, update its guidance without changing the server contract.

## Open Questions

- Should the skill be named for the server (`axml-mcp-skill`) or for the broader workflow it enables?
- Should the skill explicitly mention export targets such as markdown, GSN, or SACM, or stay format-agnostic?
- Should existing agent files link directly to the skill, or should the README be the only user-facing pointer?
