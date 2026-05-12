## MODIFIED Requirements

### Requirement: Executive Narrative Synthesis
The system MUST provide a narrative-synthesizer agent that can translate a parsed assurance-case graph into a plain-English executive briefing.

#### Scenario: User asks for a summary
- **WHEN** a user asks what an assurance case means or "so what is this?"
- **THEN** the agent MUST call `parse_assurance_case` to ingest the `.axml` file
- **AND THEN** it MUST summarize the bottom line, the core argument, the evidence reality, and the current risks from the parsed graph data
- **AND THEN** it MUST avoid raw AXML layout jargon unless explicitly requested

### Requirement: System Context Generation
The system MUST provide a second narrative-synthesizer mode that generates a compact system context brief for downstream agents.

#### Scenario: Builder agents need context
- **WHEN** the narrative synthesizer is asked to prepare shared context for other agents
- **THEN** it MUST call `parse_assurance_case` to ingest the `.axml` file
- **AND THEN** it MUST produce a concise system brief describing the system's goals and operating environment from the parsed graph data
- **AND THEN** it MUST save that brief via `set_system_context` so downstream agents can reuse it
