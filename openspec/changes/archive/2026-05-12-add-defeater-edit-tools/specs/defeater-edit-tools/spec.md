## ADDED Requirements

### Requirement: Atomic Defeater Write
The system MUST provide an MCP tool that creates a Type 8 defeater node and a Type 5 defeats link in a single mutation operation.

#### Scenario: Red-team agent appends a defeater
- **WHEN** a subagent requests a defeater edit against a target node
- **THEN** the MCP tool MUST create a defeater node and connect it to the target with a defeats link
- **AND THEN** it MUST preserve the existing graph structure outside that mutation

### Requirement: In-Place Node Rewrite
The system MUST provide an MCP tool that rewrites the text content of an existing `.axml` node without replacing unrelated structure.

#### Scenario: Concretion refines a claim
- **WHEN** the concretion workflow requests a rewrite of an existing node
- **THEN** the MCP tool MUST update the selected node text in place
- **AND THEN** it MUST keep the node identifier, links, and unrelated metadata intact

### Requirement: Mutation Feedback
The system MUST return stable identifiers and validation feedback after a mutation so calling agents can chain further edits safely.

#### Scenario: Caller verifies a write
- **WHEN** the MCP tool completes a defeater write or node rewrite
- **THEN** it MUST return the affected node identifier(s), the applied mutation type, and a status indicating success or failure
