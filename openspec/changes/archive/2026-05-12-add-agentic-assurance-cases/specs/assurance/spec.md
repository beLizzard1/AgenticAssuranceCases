## ADDED Requirements

### Requirement: AXML Network Parsing
The system MUST parse raw `.axml` assurance case files into a token-efficient semantic structure using the repository schema definitions as the source of truth for node and link metadata.

#### Scenario: User provides an AXML file
- **GIVEN** a user uploads an `.axml` file to OpenCode chat
- **WHEN** the assurance-case workflow reads the file
- **THEN** it MUST use the `parse_assurance_case` MCP tool to extract titles, stripped HTML annotations, relationship links, and schema-aware node metadata instead of reading raw XML

### Requirement: Neighborhood Context Exposure
The system MUST provide local graph context around a claim so subagents can see adjacent supporting structure.

#### Scenario: Evaluator requests nearby nodes
- **GIVEN** a parsed claim node identifier
- **WHEN** the evaluator requests neighborhood context from the MCP server
- **THEN** the server MUST return the connected subgraph within the requested radius from the NetworkX model

### Requirement: AXML File Modification
The system MUST be able to persist targeted updates back to the source `.axml` file while respecting schema-defined fields.

#### Scenario: Claim annotation is revised
- **GIVEN** a user-approved edit to a claim node or annotation
- **WHEN** the workflow sends the update to the MCP server
- **THEN** the server MUST write the updated content back to the `.axml` file without replacing unrelated structure or dropping schema-defined status fields

### Requirement: Helping Hand Claim Routing
The system MUST evaluate claims systematically and delegate to the correct strategy.

#### Scenario: Claim evaluation workflow
- **GIVEN** a parsed claim
- **WHEN** the primary assurance agent evaluates it
- **THEN** it MUST route the claim to one of five specialized subagents based on the Helping Hand decision tree
