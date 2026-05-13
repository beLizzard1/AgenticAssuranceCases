## ADDED Requirements

### Requirement: Pidev agent SHALL be packageable as a pi package
The pidev agent codebase SHALL include metadata and packaging instructions necessary to publish a pi package on pi.dev. Packaging metadata (e.g., `pi.yaml`) and build scripts SHALL be placed under `agents/pidev/` or in the `pidev` branch only.

#### Scenario: Build pi package
- **WHEN** the packaging script is invoked in the pidev branch
- **THEN** it produces a pi package artifact suitable for publishing to pi.dev and includes required metadata

### Requirement: Repo SHALL support both clone-and-run and pi package consumption
The repository SHALL continue to support the current developer workflow where users clone the repo and follow README instructions (opencode). Simultaneously, the repo SHALL contain packaging support for the pidev agent so consumers can install via pi.dev packages.

#### Scenario: Developer consumes agent via pi.dev
- **WHEN** a consumer fetches the agent from pi.dev
- **THEN** the agent installs and runs without requiring manual cloning of this repository
