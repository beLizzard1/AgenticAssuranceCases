## ADDED Requirements

### Requirement: MCP Evidence Registry Discovery
The system MUST provide a registry-based way for the evidence-incorporation agent to discover available MCP evidence providers at runtime.

#### Scenario: Agent starts evidence search
- **WHEN** the evidence-incorporation workflow begins
- **THEN** it MUST query the registry for available MCP evidence providers
- **AND THEN** it MUST receive discoverable provider names and capabilities before selecting a source to search

### Requirement: Multi-Provider Evidence Querying
The system MUST allow the evidence-incorporation agent to query multiple MCP evidence providers without changing the core agent logic when new providers are added.

#### Scenario: New evidence source appears
- **WHEN** a new MCP evidence provider is registered
- **THEN** the agent MUST be able to discover and query that provider through the registry pattern
- **AND THEN** no hardcoded retrieval script update is required for the new provider

### Requirement: Compact Discovery Output
The registry MUST return compact, machine-readable metadata so the agent can choose evidence providers efficiently.

#### Scenario: Agent inspects available providers
- **WHEN** the agent requests available MCP evidence sources
- **THEN** the registry MUST return a concise list of provider identities and capabilities
- **AND THEN** the output MUST be suitable for prompt consumption without excessive verbosity
