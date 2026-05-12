## Why

OpenCode is expected to bring up the local AXML MCP server automatically, but that startup path does not appear to be reliable. If the server is not launched at session start, the repo loses its structured `.axml` tooling and downstream agent workflows cannot operate as intended.

## What Changes

- Make the local AXML MCP server start consistently when OpenCode launches the workspace.
- Ensure the configured MCP entry is valid and discoverable at startup.
- Improve failure visibility so a missing or broken server launch is obvious early.

## Capabilities

### New Capabilities
- `axml-mcp-startup`: Reliable startup and registration of the local AXML MCP server in OpenCode.

### Modified Capabilities
- 

## Impact

- `opencode.json` MCP configuration.
- Local AXML MCP server startup path.
- OpenCode workspace initialization and user-facing availability of `.axml` tools.
