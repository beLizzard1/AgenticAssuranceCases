## ADDED Requirements

### Requirement: Executive Narrative Synthesis
The system MUST provide a narrative-synthesizer agent that can translate a parsed assurance-case graph into a plain-English executive briefing.

#### Scenario: User asks for a summary
- **WHEN** a user asks what an assurance case means or "so what is this?"
- **THEN** the agent MUST summarize the bottom line, the core argument, the evidence reality, and the current risks in human-readable language
- **AND THEN** it MUST avoid raw AXML layout jargon unless explicitly requested

### Requirement: System Context Generation
The system MUST provide a second narrative-synthesizer mode that generates a compact system context brief for downstream agents.

#### Scenario: Builder agents need context
- **WHEN** the narrative synthesizer is asked to prepare shared context for other agents
- **THEN** it MUST produce a concise system brief describing the system's goals and operating environment
- **AND THEN** it MUST keep the brief short enough to be reused as agent context

### Requirement: Shared Context Persistence
The system MUST provide MCP tools to save and retrieve the current system context brief in memory.

#### Scenario: Context is updated and reused
- **WHEN** the narrative synthesizer stores a new system brief
- **THEN** the MCP server MUST make that brief available to later calls that request the shared context
- **AND THEN** it MUST return the latest saved brief when queried
