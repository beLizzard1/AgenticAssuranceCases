## 1. Validation and diagnostics

- [x] 1.1 Update the AXML file-open path to detect unsupported `confidence` status values from the ASCAD 2.0 schema and fail with a targeted validation error.
- [x] 1.2 Map parser/enum failures into a user-facing message that includes the invalid field name and offending value.

## 2. Verification

- [x] 2.1 Add a test for opening a malformed AXML file with an invalid `confidence` value outside `Off`, `Low`, `Medium`, or `High` and assert the error is actionable.
- [x] 2.2 Add a test for opening a valid AXML file to confirm normal load behavior is unchanged.
- [x] 2.3 Run the relevant validation/open-file test suite and confirm the new diagnostics appear as expected.
