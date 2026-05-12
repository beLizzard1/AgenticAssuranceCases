## 1. Apply YAML Permissions

- [x] 1.1 Update `.opencode/agents/top-down-architect.md` with strict `.axml` read/edit denial.
- [x] 1.2 Update `.opencode/agents/adversarial-evaluator.md` with strict `.axml` read/edit denial.
- [x] 1.3 Update `.opencode/agents/narrative-synthesizer.md` with strict `.axml` read/edit denial.
- [x] 1.4 Apply the same permission block to all remaining subagents.

## 2. Implement MCP Backup System

- [x] 2.1 Add a `create_backup(file_path)` helper to `mcp-server/asce_parser.py`.
- [x] 2.2 Call `create_backup(file_path)` at the start of `write_defeater`.
- [x] 2.3 Call `create_backup(file_path)` at the start of the remaining mutating assurance-case write paths.
- [x] 2.4 Add `.backups/` to `.gitignore` if backups should stay untracked.

## 3. Verify Safety Behavior

- [x] 3.1 Confirm `.axml` reads and edits are denied for agents.
- [x] 3.2 Confirm mutating MCP calls create timestamped backups before writes.
