## Why

Current write-back flows edit the existing `.axml` tree in place, which makes identity-sensitive structures brittle when links or references are reused. Reconstructing the output from the parsed graph plus schema gives us a single canonical source of truth for serialization and reduces drift between the graph model and the emitted file.

## What Changes

- Add a graph-backed reconstruction path that emits `.axml` from the parsed assurance-case graph.
- Use the schema as the source of truth for node, link, and status-field shape during reconstruction.
- Prefer regenerating the affected output region or file over mutating raw XML fragments in place.
- Write reconstructed output to a new `.axml` path and promote that path as the active case for later MCP interactions.
- Preserve stable node identity where possible while allowing links and derived structures to be rebuilt safely.
- **BREAKING**: direct raw-XML patching is no longer the primary output path for reconstruction workflows.

## Capabilities

### New Capabilities
- `graph-backed-output-reconstruction`: Rebuild assurance-case output from parsed graph data and schema metadata.

### Modified Capabilities
- 

## Impact

- `mcp-server/asce_parser.py` will need a reconstruction/serialization path in addition to graph parsing.
- Existing mutation-oriented workflows may need to switch to reconstruction when link identity or reused references matter.
- The MCP session or shared context will need to track the active `.axml` path after reconstruction.
- Schema validation becomes part of the output generation contract.
- Tests and fixtures for `.axml` round-tripping will need to cover link identity, node reuse, and structural equivalence.
