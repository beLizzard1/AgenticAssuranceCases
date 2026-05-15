## Context

Opening a malformed AXML file currently surfaces a generic load failure instead of a targeted validation error. The immediate problem is not the file format itself, but the lack of actionable feedback when the ASCAD 2.0 `confidence` field contains an unsupported value such as `medium` instead of one of `Off`, `Low`, `Medium`, or `High`.

## Goals / Non-Goals

**Goals:**
- Detect invalid AXML status values during file open using the schema enum definitions.
- Preserve the underlying validation detail so the user can identify the bad field and value.
- Keep successful file loading unchanged for valid documents.

**Non-Goals:**
- Redesigning the AXML schema.
- Auto-correcting invalid files.
- Broad parser refactors unrelated to validation diagnostics.

## Decisions

- Validate status fields at the loader boundary rather than allowing the parser to fail generically.
  - Rationale: this keeps the failure localized to file-open handling and makes error reporting consistent.
  - Alternative considered: change the parser to accept more values. Rejected because the issue is malformed input, not supported syntax.

- Map low-level enum/schema errors into a user-facing diagnostic that names the offending field and value.
  - Rationale: the user needs a fixable message, not an internal exception string.
  - Alternative considered: display the raw parser error. Rejected because it is too opaque for end users.

- Treat validation as fail-fast for malformed files.
  - Rationale: continuing after a bad status value can produce partial or misleading graphs.
  - Alternative considered: load with warnings. Rejected because it would hide data integrity problems.

## Risks / Trade-offs

- [Risk] Validation may reject files that were previously accepted by permissive parsing -> Mitigation: keep the rule narrow and limited to unsupported status values.
- [Risk] Error messages could become too technical -> Mitigation: include field/value context but avoid stack traces in the user-facing path.
- [Risk] Additional validation could affect load timing -> Mitigation: confine checks to the open path and keep them linear over the parsed document.

## Migration Plan

- Update the file-open path to classify enum/status validation failures explicitly.
- Add or adjust user-facing error text for invalid `confidence` values.
- Verify valid AXML files still open and malformed files now fail with actionable diagnostics.
- Rollback strategy: revert the loader-level validation mapping if the new messaging causes regressions; the parser behavior remains unchanged.

## Open Questions

- Should the user-facing error surface highlight only `Confidence`, or all invalid status fields consistently?
- Do we want a separate diagnostic code for this failure class so future validation errors can share the same handling path?
