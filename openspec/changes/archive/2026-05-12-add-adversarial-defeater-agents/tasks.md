## 1. Project Infrastructure
- [x] 1.1 Add the adversarial agent files under `.opencode/agents/`.
- [x] 1.2 Update OpenCode configuration or permissions if the new agents need explicit tool access.

## 2. Adversarial Agents
- [x] 2.1 Create `.opencode/agents/adversarial-evaluator.md` as the red-team router.
- [x] 2.2 Create `.opencode/agents/rebutting-defeater.md` for claim-level attacks.
- [x] 2.3 Create `.opencode/agents/undercutting-defeater.md` for inference attacks.
- [x] 2.4 Create `.opencode/agents/undermining-defeater.md` for evidence attacks.

## 3. MCP Integration
- [x] 3.1 Verify the adversarial router can read graph context from the existing MCP parser.
- [x] 3.2 Verify the red-team flow can draft schema-compatible Defeater nodes for write-back.

## 4. Validation
- [x] 4.1 Review the adversarial agent prompts for clear routing boundaries.
- [x] 4.2 Confirm the new workflow does not interfere with the existing builder-pass agents.
