## ADDED Requirements

### Requirement: Change Branch Creation
The system SHALL create or checkout a dedicated git branch for a change before `/opsx-apply` begins implementation work.

#### Scenario: Apply starts on an isolated branch
- **WHEN** a user applies a specific OpenSpec change
- **THEN** the system creates or switches to a change-scoped branch for that change before making edits

### Requirement: Branch-Scoped Work State
The system SHALL keep change work isolated to the active change branch until the change is archived.

#### Scenario: Change edits stay on the change branch
- **WHEN** the user edits artifacts during apply
- **THEN** the edits occur on the change branch rather than the default base branch

### Requirement: Branch-Aware Archive Completion
The system SHALL archive a completed change from its change branch and return the repository to a stable base-branch state.

#### Scenario: Archive finalizes the change branch
- **WHEN** a user archives a completed OpenSpec change
- **THEN** the system finalizes the change on the active change branch and returns to the base branch after archive completes

### Requirement: Active Branch Visibility
The system SHALL expose the active branch or branch transition state when reporting change status.

#### Scenario: Status shows branch context
- **WHEN** a user checks the status of an applied or archived change
- **THEN** the system reports which branch is active or which branch transition is in progress

### Requirement: Deterministic Branch Naming
The system SHALL derive change branch names from the OpenSpec change name using a deterministic, human-readable convention.

#### Scenario: Branch name can be predicted from change name
- **WHEN** a user knows the change name
- **THEN** the user can infer the corresponding branch name from the naming convention

### Requirement: Shared Change Branch Across Entry Points
The system SHALL use the same change branch when the workflow is initiated from OpenCode or the Pi agent path.

#### Scenario: Different clients operate on the same branch
- **WHEN** the same change is applied or archived from OpenCode and from the Pi agent workflow
- **THEN** both clients operate on the same branch and observe the same branch creation, branch selection, and archive transition rules

### Requirement: Branch Retention After Archive
The system SHALL retain the completed change branch after archive unless a human explicitly removes it.

#### Scenario: Archive leaves the branch available
- **WHEN** a user archives a completed change
- **THEN** the branch remains available locally for manual inspection or cleanup
