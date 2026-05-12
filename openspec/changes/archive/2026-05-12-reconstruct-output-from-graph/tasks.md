## 1. Reconstruction pipeline

- [x] 1.1 Define the graph-to-XML reconstruction entrypoint in `mcp-server/asce_parser.py`.
- [x] 1.2 Map graph nodes to schema-compliant XML elements using schema metadata as the serialization contract.
- [x] 1.3 Rebuild links and relationships from graph edges instead of reusing serialized link nodes.

## 2. Safety and validation

- [x] 2.1 Add deterministic allocation or mapping for regenerated identifiers where the graph does not already provide a stable value.
- [x] 2.2 Validate reconstructed output against the schema before writing the file.
- [x] 2.3 Fail with a clear error when reconstruction would violate schema rules or drop required structure.
- [x] 2.4 Record the newly reconstructed file as the active path for future MCP calls.

## 3. Verification

- [x] 3.1 Add round-trip tests that parse a case, reconstruct output, and reparse the result for structural equivalence.
- [x] 3.2 Add regression coverage for link reuse and endpoint-change scenarios.
- [x] 3.3 Confirm unrelated graph content survives reconstruction unchanged.
- [x] 3.4 Verify follow-up MCP operations use the regenerated file path after reconstruction.
