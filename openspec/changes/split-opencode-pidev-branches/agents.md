## Agents

This document describes agent workflows and packaging for the repository.

- opencode: clone-and-run workflow supported. Follow the README at the repository root or in the opencode branch.
- pidev: packaged distribution via pi.dev. Packaging metadata and build scripts live under agents/pidev/ or in the pidev branch.

Packaging notes:
- pi package metadata should include name, version, entrypoint, and any dependencies (example `pi.yaml` in agents/pidev/).

Validation:
- CI will run a script to validate that agent-specific files are only modified in their agent branches, and that pi package metadata is present when needed.
