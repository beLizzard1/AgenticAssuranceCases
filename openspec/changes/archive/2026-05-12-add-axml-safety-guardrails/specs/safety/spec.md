## ADDED Requirements

### Requirement: Hard-Blocked Native File Access
Agents MUST be physically prevented from using default LLM file-reading or file-writing tools on `.axml` files to prevent schema corruption.

#### Scenario: Agent hallucinates standard file access
- **GIVEN** an agent attempts to use the native `read` or `edit` tool on `drone-case.axml`
- **WHEN** the OpenCode permission engine intercepts the call
- **THEN** it MUST deny the request and force the agent to fall back to the allowed `my_mcp_server_*` tools.

### Requirement: Mandatory Pre-Write Backups
The system MUST NEVER destructively overwrite an assurance case without saving the previous state.

#### Scenario: Agent attempts an MCP write operation
- **GIVEN** an agent triggers `write_subclaims` or `write_defeater` via the MCP server
- **WHEN** the Python script receives the request
- **THEN** it MUST synchronously copy the target `.axml` file to a hidden `.backups/` directory with a timestamped `.bak` extension BEFORE executing the XML modifications.
