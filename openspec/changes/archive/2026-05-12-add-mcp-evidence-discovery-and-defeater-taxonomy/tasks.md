## 1. MCP Evidence Discovery

- [x] 1.1 Add registry-based evidence discovery so the evidence-incorporation workflow can enumerate available MCP evidence providers.
- [x] 1.2 Update the evidence-incorporation prompt or wiring so it queries discovered providers instead of relying on hardcoded retrieval scripts.
- [x] 1.3 Validate that new evidence providers can be discovered and queried without changing the core agent logic.

## 2. Defeater Taxonomy

- [x] 2.1 Add a prompt-ready defeater taxonomy packet for the challenger agent with a taxonomy layer, a playbook layer, and concrete prompt examples.
- [x] 2.2 Update the challenger-facing prompt or wiring so the taxonomy is used as context before defeater generation.
- [x] 2.3 Confirm the taxonomy remains easy to revise without changing the challenger agent's core logic.

## 3. Validation

- [x] 3.1 Validate the evidence-incorporation flow against at least one representative evidence source discovered through the registry.
- [x] 3.2 Validate the challenger flow against a representative claim and confirm the taxonomy makes the defeaters more systematic.
