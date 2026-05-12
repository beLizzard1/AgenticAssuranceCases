## 1. Startup Path

- [x] 1.1 Update the OpenCode MCP configuration or entrypoint so the local AXML server launches reliably from the workspace root.
- [x] 1.2 Make the startup command/path deterministic enough to work without manual intervention.

## 2. Failure Visibility

- [x] 2.1 Add or adjust startup diagnostics so a failed AXML MCP launch is visible to the user or logs.
- [x] 2.2 Confirm OpenCode does not silently continue with missing AXML tooling after a failed launch.

## 3. Verification

- [x] 3.1 Launch OpenCode in the repository and confirm the AXML MCP server registers successfully.
- [x] 3.2 Reproduce a failure case, if possible, and confirm the failure is reported clearly.
