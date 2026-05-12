## Why

The evidence-incorporation workflow needs a more extensible way to discover evidence sources than hardcoded retrieval scripts, and the challenger loop needs a better starting structure than unconstrained zero-shot prompting. Adding both together gives the assurance system a flexible evidence-discovery layer and a more systematic way to generate strong defeaters.

## What Changes

- Add an MCP registry pattern so the evidence-incorporation subagent can discover and query available MCP servers dynamically.
- Allow the evidence workflow to search multiple evidence providers without changing the core agent logic each time a new source is added.
- Add a structured defeater taxonomy or library for the challenger agent to use when generating counter-claims.
- Seed that taxonomy with practical security and assurance categories such as STRIDE-style threat modeling, resiliency, and recovery concerns.
- Expand the taxonomy with assurance-specific categories from the literature, including Gohar et al.'s seven defeater families, Assurance 2.0 step-based attacks, and STPA-Sec loss scenarios.
- Package the taxonomy as a prompt-ready packet with definitions, cues, route mappings, examples, and playbook rules so the challenger does not need to infer the meaning of the labels.
- Keep the defeater taxonomy focused on categories of weakness and attack patterns rather than free-form brainstorming.
- **BREAKING**: evidence discovery and challenger prompting are expected to use the new registry/taxonomy path rather than static retrieval scripts or purely zero-shot counter-claim generation.

## Capabilities

### New Capabilities
- `dynamic-evidence-mcp-discovery`: MCP registry-based evidence source discovery and querying for evidence incorporation.
- `defeater-taxonomy`: Structured defeater categories and prompts for more systematic challenger generation.

### Modified Capabilities

- None.

## Impact

- Updates to evidence-incorporation and challenger-facing agent prompts.
- Potential updates to MCP wiring or shared context utilities if the registry needs to expose discoverable servers.
- No schema changes are expected.
