## ADDED Requirements

### Requirement: Reconstruct output from graph and schema
The system MUST provide a reconstruction path that emits `.axml` output from parsed assurance-case graph data and schema metadata instead of editing raw XML fragments in place.

#### Scenario: Rebuild output for a parsed case
- **WHEN** the system is asked to produce assurance-case output from a parsed graph
- **THEN** it MUST serialize the output from graph structure plus schema metadata
- **AND THEN** it MUST not depend on previously stored XML fragments as the source of truth

### Requirement: Rebuild relationship links from graph edges
The system MUST regenerate relationship and link elements from the graph's edges so that stale or reused link structures are not carried forward accidentally.

#### Scenario: A link endpoint changes
- **WHEN** a node or relationship in the graph changes
- **THEN** the reconstructed output MUST rebuild the affected link elements from the current graph state
- **AND THEN** it MUST avoid reusing obsolete link references from the prior XML tree

### Requirement: Reconstructed output is schema-valid
The system MUST validate reconstructed `.axml` output against the loaded schema metadata before persisting it.

#### Scenario: Reconstruction produces invalid structure
- **WHEN** serialization yields an output that violates the schema definition
- **THEN** the system MUST report a clear failure and MUST NOT persist the invalid output

### Requirement: Promote reconstructed file as active case
The system MUST switch future MCP interactions to the newly reconstructed `.axml` file so that subsequent parsing and edits continue from the regenerated path.

#### Scenario: Reconstruction completes successfully
- **WHEN** the system writes a reconstructed case to a new file path
- **THEN** that new path MUST become the active file for later MCP operations
- **AND THEN** future interactions MUST resolve against the regenerated file rather than the original source file
