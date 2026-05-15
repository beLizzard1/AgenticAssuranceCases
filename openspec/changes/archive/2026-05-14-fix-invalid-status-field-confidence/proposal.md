## Why

Opening a malformed `.axml` file currently fails with a generic parser error that does not clearly identify the invalid field or the value that caused the failure. In the ASCAD 2.0 schema, the `confidence` status field is constrained to `Off`, `Low`, `Medium`, or `High`, so invalid values should be rejected with a precise diagnostic.

## What Changes

- Improve AXML file loading so invalid `confidence` status values are reported clearly at open time.
- Surface the exact offending field and value instead of a generic "could not open" failure.
- Keep valid files loading normally; only malformed input should trigger the new validation path.

## Capabilities

### New Capabilities
- `axml-file-validation`: validate AXML files on load against schema-defined status enums and report precise, actionable errors for malformed fields.

### Modified Capabilities
- 

## Impact

- AXML file parsing and validation logic.
- File-open error handling and user-facing diagnostics.
- Any UI or logging path that currently collapses parse failures into a generic message.
