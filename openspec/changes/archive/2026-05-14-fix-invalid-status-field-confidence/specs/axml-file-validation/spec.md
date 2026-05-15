## ADDED Requirements

### Requirement: AXML file validation reports invalid schema-defined status values
The system MUST validate AXML content during file open against the ASCAD 2.0 schema and MUST reject malformed status fields with a clear error that identifies the field name and invalid value.

#### Scenario: Confidence status has an unsupported value
- **WHEN** a user opens an AXML file containing a `confidence` status value that is not one of `Off`, `Low`, `Medium`, or `High`
- **THEN** the system MUST fail the open operation
- **AND THEN** it MUST report which field is invalid and include the offending value in the error message

#### Scenario: Valid AXML file opens normally
- **WHEN** a user opens an AXML file whose status fields all contain supported values
- **THEN** the system MUST load the file successfully
- **AND THEN** it MUST not emit validation errors for those fields

### Requirement: File-open failures remain actionable
The system MUST surface validation failures in a way that helps the user correct the file instead of returning a generic load failure.

#### Scenario: Loader encounters malformed input
- **WHEN** the file loader detects a schema or enum violation while opening an AXML file
- **THEN** it MUST present an actionable error message to the user
- **AND THEN** it MUST preserve the underlying validation detail for troubleshooting
