## ADDED Requirements

### Requirement: Opencode SHALL continue to support clone-and-run workflow
The opencode agent SHALL maintain the current developer experience where users clone the repository and follow README instructions to run the agent locally.

#### Scenario: Developer clones repo
- **WHEN** a developer follows the README in the opencode branch
- **THEN** they can build and run the opencode agent without needing additional packaging steps

### Requirement: Optional packaging support for opencode
If maintainers choose to publish opencode as a package, packaging artifacts SHALL be isolated to the opencode branch or `agents/opencode/` directory and MUST not be required for the clone-and-run workflow.

#### Scenario: Packaged consumption
- **WHEN** a consumer installs opencode via a package
- **THEN** the package should include the runtime and metadata but docs must continue to cover clone-and-run
