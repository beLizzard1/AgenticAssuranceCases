---
name: axml-mcp-skill
description: Use the local asce_tools AXML MCP server for schema-aware assurance-case graph inspection, traversal, targeted mutation, defeater creation, shared context, evidence-provider discovery, reconstruction, and validation-oriented write-back.
license: MIT
compatibility: Requires OpenCode and the local asce_tools MCP server configured in opencode.json.
metadata:
  author: Agentic Assurance Cases
  version: "1.1"
---

# AXML MCP Skill

Use this skill whenever an agent works with Adelard ASCE `.axml` assurance-case files, Helping Hand notation, CAE structures, claim trees, evidence links, defeaters, shared system context, or assurance-case graph traversal.

The local MCP server is configured as `asce_tools` in `opencode.json`. Treat that server as the semantic interface to the assurance case. Do not treat `.axml` files as ordinary XML unless the required operation is not supported by MCP.

## Core Rule

Agents MUST prefer MCP operations over raw file edits for assurance-case structure.

Raw `.axml` editing is only acceptable for:
- documentation examples
- comments
- unsupported metadata
- emergency recovery when MCP is unavailable and the user explicitly accepts non-semantic editing

Structural assurance-case changes include:
- creating, deleting, or modifying claims
- creating, deleting, or modifying arguments
- creating, deleting, or modifying evidence nodes
- adding or changing links
- creating defeaters
- changing node status fields
- reconstructing or canonicalising an assurance case
- updating targeted node content

## Repository Context

This repository uses:

- OpenCode agents in `.opencode/agents/`
- this skill in `.opencode/skills/axml-mcp-skill/SKILL.md`
- the MCP server configured in `opencode.json`
- the MCP startup script at `scripts/start-asce-mcp.sh`
- the MCP implementation at `mcp-server/asce_parser.py`
- the ASCAD schema at `schemas/ASCAD 2.0.xml`
- sample `.axml` files under `examples/`

The MCP server name is `asce_tools`.

## When to Use

Use this skill when the user asks to:

- inspect an `.axml` assurance case
- explain the structure of an assurance case
- find top-level claims
- walk an assurance case top-down
- evaluate a claim bottom-up
- inspect claim neighbourhood context
- route claims to specialist subagents
- update an existing assurance-case node
- add defeaters
- inspect evidence providers
- use or update shared system context
- reconstruct an assurance case
- apply targeted write-back mutations
- analyse CAE completeness
- identify unsupported claims
- identify weak or missing evidence
- prepare a human-facing assurance narrative from graph content

Do not use this skill for unrelated prose drafting unless the prose is derived from, or intended to update, an assurance-case node.

## Mandatory Discovery

Before assuming exact tool names or schemas, agents MUST discover available MCP tools.

The current server is expected to expose capabilities broadly aligned with:

- `parse_assurance_case`
- `get_assurance_neighborhood`
- `get_root_claims`
- `get_node_children`
- `reconstruct_assurance_case`
- `write_defeater`
- `modify_assurance_case`
- `set_system_context`
- `get_system_context`
- `discover_evidence_providers`
- `list_evidence_providers`

Exact tool names and arguments are implementation details. Discover first.

## Operating Model

### 1. Establish case context

For any `.axml` task:

1. Identify the target file.
2. Parse or inspect the case through MCP.
3. Confirm the active AXML path if the server supports active-file state.
4. Retrieve schema metadata if available.
5. Use MCP graph views rather than manually parsing XML.

If no target file is specified but the task clearly refers to the active case, use the current active AXML path exposed by the MCP server.

### 2. Traverse using graph operations

For top-down assurance work:

1. Use root-claim discovery.
2. Select the relevant root claim.
3. Use immediate-child traversal.
4. Fetch neighbourhood context before evaluating a node.
5. Preserve the distinction between claim, argument, evidence, side-claim, subcase, defeater, and comment nodes.

For bottom-up evaluation:

1. Start from the claim or evidence node.
2. Fetch its neighbourhood.
3. Inspect supporting children and incoming/outgoing links.
4. Identify whether the parent claim is actually supported by argument and evidence, not merely textually adjacent.

### 3. Use shared context deliberately

Use shared system context when multiple agents need a common description of:

- item definition
- operational context
- concept of operations
- assurance scope
- stakeholder framing
- system boundary
- threat environment
- lifecycle phase
- assumptions and caveats

Do not bury system context inside individual claim text where the MCP server supports shared context.

### 4. Route to specialist agents

The AXML MCP skill supports the wider agent architecture.

Use agent routing like this:

- Assurance Evaluator: bottom-up claim evaluation and routing
- Top-Down Architect: root-first traversal and structure analysis
- Narrative Synthesizer: human-facing briefing and shared system context generation
- Evidence Incorporation: evidence relevance, sufficiency, provenance, and traceability
- Calculation: quantitative or formula-based support
- Decomposition: claim breakdown and child-claim adequacy
- Substitution: standards, presumption-of-conformity, and equivalent-evidence reasoning
- Concretion: moving abstract claims toward item-specific claims
- Adversarial Evaluator: defeater discovery and challenge analysis

Agents should use MCP-derived node IDs and neighbourhood context when handing work to subagents.

## Mutation Rules

### General mutation

Before mutation:

1. Parse or inspect the case through MCP.
2. Identify the exact node IDs and link IDs affected.
3. State the intended semantic change.
4. Prefer targeted MCP write-back over whole-document rewrite.

After mutation:

1. Confirm what changed.
2. Re-read or reconstruct the affected section if the server supports it.
3. Report changed node IDs.
4. Report any unresolved limitations.

### Existing-node updates

Use MCP write-back for updates to existing nodes.

Typical updates include:

- title refinement
- annotation refinement
- status-field changes
- clarification of claim wording
- adding evaluation notes
- adding evidence interpretation

Do not rewrite the whole `.axml` file to change a single node.

### Defeater creation

Use the MCP defeater write-back capability when adding defeaters.

Each defeater should record:

- target node or inference
- defeater type
- concise title
- explanation
- severity or confidence if supported
- status if supported
- rationale
- source agent or pass

Use the following taxonomy:

- rebutting defeater: challenges the claim itself
- undermining defeater: challenges the evidence or source
- undercutting defeater: challenges the inference from evidence to claim

Do not remove defeaters simply because they weaken the assurance case. Defeaters are part of the assurance record.

### Evidence-provider workflow

When evidence is needed:

1. Inspect the claim and neighbourhood.
2. Discover available evidence providers through MCP.
3. Match evidence-provider capabilities to the evidence need.
4. Record whether the evidence is attached, unavailable, stale, weak, or merely proposed.
5. Do not mark a claim as evidenced unless evidence is explicitly connected or cited.

Evidence assessment should consider:

- relevance
- provenance
- version
- date
- scope
- independence
- repeatability
- coverage
- limitations
- whether it supports the specific claim or only a nearby/general claim

## Validation Discipline

The current MCP server may provide reconstruction and schema-aware checks rather than a single strict validation command. Use whatever validation or reconstruction capability is available.

Minimum post-change checks:

- affected node exists
- affected links resolve
- generated defeater links resolve
- updated node content appears in the reconstructed or re-read case
- no obvious dangling references were introduced
- node types remain schema-aware
- status fields are recognised by the loaded ASCAD schema
- backup behaviour has not been bypassed for write-back operations

If strict validation is unavailable, say so. Do not claim “validated” when only parsed or reconstructed.

Use these terms precisely:

- “parsed”: MCP successfully read the case
- “inspected”: MCP returned graph or neighbourhood data
- “reconstructed”: MCP produced a reconstructed case output
- “updated”: MCP applied a targeted mutation
- “validated”: MCP or another validator explicitly checked validity

## Safety Rules

Agents MUST NOT:

- silently overwrite `.axml` files
- invent node IDs when an MCP operation returns canonical IDs
- delete nodes without explicit user intent
- remove defeaters without recording rationale
- convert graph structure into flat prose and treat that as equivalent
- claim evidence exists when only an evidence gap exists
- assume all child nodes support the parent without checking link direction and type
- assume the first root claim is the only top-level claim
- assume exact MCP tool names without discovery
- edit raw `.axml` for structural changes when MCP supports the operation

Agents SHOULD:

- preserve existing node references
- work in small targeted changes
- report changed node IDs
- distinguish assurance gaps from parser/tool limitations
- use neighbourhood context before judging a claim
- keep context, assumptions, evidence, and defeaters explicit

## Output Format

For inspection-only tasks, respond with:

```text
Findings:
- ...

Relevant nodes:
- ...

Assurance implications:
- ...

Gaps or uncertainties:
- ...
````

For mutation tasks, respond with:

```text
Updated:
- ...

Changed nodes or links:
- ...

MCP checks:
- ...

Remaining gaps:
- ...
```

For failed MCP operations, respond with:

```text
Could not complete the MCP operation.

Reason:
- ...

What was safely completed:
- ...

Recommended next step:
- ...
```

## Example: Top-Down Traversal

User asks:

“Walk the assurance case from the top-level claim and identify weak branches.”

Agent should:

1. Discover MCP tools.
2. Parse the target `.axml`.
3. Get root claims.
4. For each relevant root, get immediate children.
5. Fetch neighbourhood context for suspicious or important nodes.
6. Classify weak branches as:

   * unsupported claim
   * argument without evidence
   * evidence without provenance
   * assumption dependency
   * unresolved defeater
   * vague or non-item-specific claim
7. Report node IDs and reasoning.

## Example: Adding a Defeater

User asks:

“Add a defeater against the evidence supporting this claim.”

Agent should:

1. Identify the claim node.
2. Fetch neighbourhood context.
3. Identify the evidence node or inference being challenged.
4. Classify the defeater as rebutting, undermining, or undercutting.
5. Use MCP defeater write-back.
6. Re-read affected neighbourhood.
7. Report the new defeater node ID and target.

## Example: Evidence Incorporation

User asks:

“Use this test report as evidence for the claim.”

Agent should:

1. Identify the target claim.
2. Inspect existing evidence children.
3. Determine what exact proposition the report supports.
4. Add or update evidence via MCP if supported.
5. Avoid overclaiming.
6. Record limitations.
7. Re-read or reconstruct affected section.

Evidence should support the claim as written. If it only supports a narrower claim, recommend claim refinement or decomposition.

## Example: Narrative Synthesis

User asks:

“Summarise this case for a reviewer.”

Agent should:

1. Parse the case.
2. Get root claims.
3. Use neighbourhood traversal to identify major argument lines.
4. Retrieve shared system context.
5. Produce a human-facing briefing.
6. Clearly distinguish:

   * supported claims
   * partially supported claims
   * assumptions
   * evidence gaps
   * unresolved defeaters
   * parser limitations

Do not invent assurance confidence beyond the graph evidence.

````

---

Recommended additional file:

`docs/agent-skill-contract.md`

```md
# Agent Skill Contract: AXML MCP

Agents working with `.axml` assurance cases must use the `asce_tools` MCP server for semantic operations.

The expected sequence is:

1. discover MCP tools
2. parse or inspect the target case
3. traverse through graph/neighbourhood tools
4. apply targeted MCP write-back where mutation is needed
5. re-read, reconstruct, or validate the affected region
6. report changed node IDs and remaining assurance gaps

Agents must not directly rewrite `.axml` for claims, arguments, evidence, links, status fields, or defeaters where MCP support exists.
````
