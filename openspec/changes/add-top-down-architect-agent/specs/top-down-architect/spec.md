## ADDED Requirements

### Requirement: Immediate Child Inspection
The system MUST provide an MCP tool that returns the immediate children of a selected node in an assurance case, including each child's node metadata and the type of link connecting it to the parent.

#### Scenario: Agent inspects a node's direct descendants
- **WHEN** the top-down architect requests the children of a parent node
- **THEN** the MCP tool MUST return only the directly connected child nodes and their link types
- **AND THEN** it MUST NOT return unrelated nodes outside that immediate neighborhood

### Requirement: Root-Driven Traversal
The system MUST support a top-down assurance workflow that begins from root claims and traverses downward through the case structure.

#### Scenario: Agent begins a new traversal
- **WHEN** the top-down architect starts evaluating an assurance case
- **THEN** it MUST identify one or more root claims as traversal starting points
- **AND THEN** it MUST begin recursion from those roots rather than from a leaf claim

### Requirement: Recursive Subagent Delegation
The system MUST let the top-down architect delegate unsupported branches to specialist subagents so missing claims, arguments, or evidence can be generated or refined.

#### Scenario: A branch has a gap
- **WHEN** the architect finds a claim or argument branch that is incomplete
- **THEN** it MUST delegate the branch to an appropriate specialist subagent
- **AND THEN** it MUST resume traversal after the branch has been expanded
