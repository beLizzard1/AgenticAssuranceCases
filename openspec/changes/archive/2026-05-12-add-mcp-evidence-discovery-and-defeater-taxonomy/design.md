## Context

The evidence-incorporation workflow currently benefits from explicit, schema-aware MCP tools, but it still needs a more flexible way to find evidence sources at runtime. Separately, the challenger loop would benefit from a structured list of defeater categories so it can generate attacks more systematically than with unconstrained prompting.

## Goals / Non-Goals

**Goals:**
- Add dynamic discovery of available MCP evidence sources.
- Make evidence-incorporation able to query multiple providers without changing core agent logic.
- Provide a structured defeater taxonomy that the challenger agent can use as context.
- Keep both additions lightweight and compatible with the existing OpenCode agent model.

**Non-Goals:**
- Building a general plugin framework for all agent types.
- Replacing the existing defeater subagents.
- Designing a persistent evidence index or external knowledge graph.

## Decisions

- Use a registry pattern for evidence discovery rather than hardcoded provider calls.
  - Rationale: the evidence-incorporation agent should be able to ask "what evidence sources exist?" and then query the ones that match the current claim.
  - Alternative considered: keep per-source retrieval scripts. That would be simpler for one source, but it would require code changes every time a new evidence provider is added.

- Keep discovery and retrieval separate.
  - Rationale: the agent should first discover available providers, then query the most relevant ones. That makes the workflow easier to reason about and debug.
  - Alternative considered: a single monolithic search call. That would be convenient, but it would hide which sources were consulted.

- Represent the defeater taxonomy as a structured context artifact rather than free-form guidance.
  - Rationale: challengers need consistent categories of weaknesses to inspect, and a stable taxonomy is easier to reuse than ad hoc prompt text.
  - Alternative considered: leave defeater generation fully zero-shot. That would be more flexible, but less rigorous and less repeatable.

- Keep the taxonomy aligned with the existing adversarial subagent roles.
  - Rationale: the challenger already thinks in terms of rebutting, undercutting, and undermining attacks, so the taxonomy should reinforce that structure.
  - Alternative considered: invent a completely new set of categories. That could be useful later, but it would increase conceptual drift from the existing workflow.

- Seed the taxonomy with established security and assurance patterns such as STRIDE-style threat modeling, resiliency, and recovery.
  - Rationale: these categories give the challenger a concrete starting vocabulary that goes beyond generic attack brainstorming.
  - Alternative considered: leave the taxonomy purely abstract. That would be more flexible, but less immediately useful in practice.

- Include the literature-backed defeater families as the primary taxonomy spine.
  - Rationale: Gohar et al.'s seven families cover evidence gaps, reasoning fallacies, contextual assumptions, human and organizational factors, environmental dynamics, system evolution, and external threats; this gives the challenger a broad but grounded set of attack lenses.
  - Alternative considered: only use STRIDE. That would be useful for security, but too narrow for assurance cases that fail for non-malicious reasons.

- Map Assurance 2.0 argument steps to targeted defeater modes.
  - Rationale: decomposition, substitution, concretion, evidence incorporation, and calculation each invite different challenge questions, so a step-aware taxonomy helps the challenger route attacks more precisely.
  - Alternative considered: use a flat list of defeaters only. That would be simpler, but it would miss the structure of how arguments are assembled.

- Add STPA-Sec loss scenarios as a security-oriented sub-taxonomy.
  - Rationale: transport and CNI use cases often need functional defeaters around unsafe control actions, timing, and recovery; STPA-Sec provides that vocabulary.
  - Alternative considered: represent all security challenges as generic external threats. That would be less precise for resiliency and recovery claims.

- Present the taxonomy as a structured packet with categories, definitions, look-for cues, typical questions, example phrasing, and route mappings.
  - Rationale: the challenger should not need to infer what STRIDE, STPA-Sec, or Assurance 2.0 step names mean; the prompt must teach the agent how to use the labels.
  - Alternative considered: provide only category names. That would be shorter, but it would force the model to guess the intended interpretation.

- Organize the packet into a three-layer shape: taxonomy, playbook, and examples.
  - Rationale: the taxonomy names the categories, the playbook tells the challenger how to choose among them, and the examples show the exact "Unless ..." style expected in outputs.
  - Alternative considered: merge everything into one flat list. That would be simpler to write, but harder for the model to use reliably.

- Use a "route first, overlay second" playbook.
  - Rationale: the challenger should first classify the argument step (e.g., substitution, decomposition, concretion) and then overlay security/control categories like STRIDE or STPA-Sec when relevant.
  - Alternative considered: treat all categories as flat peers. That would be simpler, but it would lose the structural priority needed for consistent defeater generation.

- Prefer the most specific category and permit one defeater per independent loss mode when necessary.
  - Rationale: a claim can fail for more than one reason, and forcing a single category can hide the strongest attack path.
  - Alternative considered: always pick exactly one category. That would be neat, but sometimes too restrictive for real challenger work.

- Keep both features local and easy to regenerate.
  - Rationale: the evidence registry should reflect currently available MCP servers, and the taxonomy should be easy to revise as the assurance practice evolves.
  - Alternative considered: persist them in an external store. That would be more durable, but unnecessary for this repo's current setup.

## Risks / Trade-offs

- Registry discovery may return too many evidence sources -> Filter by capability and claim relevance before querying.
- A taxonomy can become too broad or too abstract -> Keep the categories tied to concrete challenger questions and examples.
- More dynamic evidence search can increase prompt complexity -> Keep discovery output compact and machine-readable.
- Challenger agents may overfit the taxonomy and miss novel attacks -> Allow free-form reasoning after the taxonomy is consulted.

## Migration Plan

1. Add the registry-based evidence discovery path.
2. Add the defeater taxonomy context and wire it into the challenger prompt.
3. Validate that evidence-incorporation can discover and query multiple sources.
4. Validate that the challenger produces more systematic defeaters when given the taxonomy.

## Open Questions

- Should the registry live inside the MCP server or in a separate discovery helper?
- Should the taxonomy be a plain markdown context file or a more structured JSON-like artifact?
- Do we want the challenger to select taxonomy categories before or after it sees neighborhood context?
