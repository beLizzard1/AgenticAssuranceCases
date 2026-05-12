## ADDED Requirements

### Requirement: Repository-specific AXML MCP skill
The system MUST provide an OpenCode skill for AXML assurance-case work that is tailored to the repository's local `asce_tools` MCP server.

#### Scenario: Agent loads AXML guidance
- **WHEN** an agent needs guidance for working with an AXML assurance case
- **THEN** the skill MUST present the repository-specific MCP operating model for `asce_tools`

### Requirement: MCP-first structural editing
The skill MUST direct agents to prefer MCP operations over raw `.axml` edits for structural assurance-case changes.

#### Scenario: Structural case content changes
- **WHEN** an agent needs to add, delete, rename, or restructure claims, arguments, evidence, links, defeaters, or status fields
- **THEN** the skill MUST tell the agent to use MCP tools rather than direct XML editing

### Requirement: Discovery before exact tool assumptions
The skill MUST instruct agents to discover available MCP tools before assuming exact tool names or broader capabilities.

#### Scenario: Tool surface is uncertain
- **WHEN** the agent does not know which AXML MCP tools exist in the current environment
- **THEN** the skill MUST require discovery before use

### Requirement: Explicit edit exceptions
The skill MUST allow raw `.axml` edits only for unsupported metadata, comments, documentation examples, or emergency recovery when MCP is unavailable and the user accepts the fallback.

#### Scenario: Non-semantic documentation changes
- **WHEN** the change is purely editorial or documentation-only
- **THEN** the skill MAY allow direct file editing

### Requirement: Current server capability awareness
The skill MUST describe the current repository capability set accurately and distinguish it from broader MCP deployments.

#### Scenario: Agent reads the capability list
- **WHEN** the agent reviews the skill's expected AXML MCP capabilities
- **THEN** the skill MUST describe the current `asce_tools` surface and note that broader capabilities are deployment-dependent
