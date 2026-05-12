## ADDED Requirements

### Requirement: AXML MCP guidance skill
The system MUST provide an OpenCode skill that directs agents to use the AXML MCP server for assurance-case operations involving formal graph structure, validation, and export.

#### Scenario: Agent receives a structural assurance-case task
- **WHEN** an agent is asked to create, inspect, modify, validate, compare, or export an assurance case
- **THEN** the skill MUST direct the agent to use the AXML MCP server as the primary semantic interface

### Requirement: Discovery-first tool usage
The skill MUST instruct agents to discover available AXML MCP tools before assuming exact tool names or capabilities.

#### Scenario: Tool names are unknown
- **WHEN** the agent does not know which AXML MCP tools are available
- **THEN** the skill MUST tell the agent to inspect the tool surface first

### Requirement: Structural edits use MCP
The skill MUST require structural assurance-case edits to flow through MCP-capable workflows rather than ad hoc raw XML editing.

#### Scenario: A node or relationship changes
- **WHEN** the agent needs to add, remove, rename, or restructure a formal assurance-case node or relationship
- **THEN** the skill MUST direct the agent to use MCP tools instead of direct `.axml` text edits

### Requirement: Editorial-only exceptions
The skill MUST allow direct edits only for non-semantic documentation or purely editorial content that is not attached to a formal assurance-case node.

#### Scenario: A comment or README changes
- **WHEN** the change is purely editorial and does not affect the assurance-case graph
- **THEN** the skill MAY allow direct file editing instead of MCP usage
