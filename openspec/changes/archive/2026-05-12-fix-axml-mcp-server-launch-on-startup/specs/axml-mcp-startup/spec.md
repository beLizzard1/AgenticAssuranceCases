## ADDED Requirements

### Requirement: Automatic AXML MCP startup
The system MUST start and register the local AXML MCP server when OpenCode launches a workspace that includes the configured AXML MCP integration.

#### Scenario: Workspace opens with AXML tools available
- **WHEN** OpenCode launches the repository workspace
- **THEN** the local AXML MCP server is started and exposed to the session's MCP clients

#### Scenario: AXML tools remain usable after launch
- **WHEN** the workspace startup completes successfully
- **THEN** the AXML MCP-backed tools are available for use in the session

### Requirement: Startup failures are visible
The system MUST surface a clear startup failure when the local AXML MCP server cannot be launched or registered.

#### Scenario: MCP server launch fails
- **WHEN** OpenCode attempts to start the local AXML MCP server and the launch does not succeed
- **THEN** the failure is reported to the user or logs rather than being silently ignored

#### Scenario: MCP server is unavailable after startup
- **WHEN** the workspace starts without a usable AXML MCP server
- **THEN** the session indicates that AXML tooling is unavailable
