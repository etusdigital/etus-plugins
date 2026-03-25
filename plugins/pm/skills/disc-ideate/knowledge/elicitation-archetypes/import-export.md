# Archetype: Import / Export

## Description

Use when the feature involves importing data from external files, exporting data for download or integration, or any bulk data ingestion/extraction pipeline. This archetype surfaces volume limits, partial failure handling, duplicate strategies, and validation gaps that are frequently discovered only during load testing.

## When to Activate

Activate this archetype when stories or problem framing mention:
- File uploads (CSV, Excel, JSON, XML)
- Bulk data import or migration
- Data export or report generation
- ETL pipelines or data sync
- Template-based data entry

## Mandatory Probes

### Probe 1: Accepted Formats
**Question:** "What file formats are accepted? CSV, Excel (.xlsx), JSON, XML, others? Are there template files the user should follow?"
- **Sufficient when:** Accepted formats listed with version specifics (e.g., "Excel .xlsx only, not .xls"), template file provided or described
- **Insufficient when:** "CSV" with no column specification or template

### Probe 2: Maximum Size
**Question:** "What is the maximum file size? Maximum number of rows or records? What happens if the user uploads a file that exceeds the limit?"
- **Sufficient when:** Concrete limits specified (e.g., "50MB or 100,000 rows"), clear error message for exceeded limits
- **Insufficient when:** "Reasonable size" or "it should handle most files" with no numbers

### Probe 3: Malformed Rows
**Question:** "If some rows are malformed (wrong type, missing required field, invalid format), does the import skip those rows, reject the entire file, or something else? How is the user informed?"
- **Sufficient when:** Strategy defined (skip + report, reject all, collect errors), error report format specified (line numbers, field names, error messages)
- **Insufficient when:** "It shows an error" with no specifics on granularity or error reporting

### Probe 4: Preview Before Commit
**Question:** "Can the user preview what will be imported before committing? Is there a dry-run mode? How many rows are shown in preview?"
- **Sufficient when:** Preview behavior defined (sample size, validation summary, confirmation step), or explicit decision that preview is not needed with rationale
- **Insufficient when:** "Maybe we should add preview" with no decision

### Probe 5: Validation Rules Per Field
**Question:** "What validation rules apply to each field? Are there uniqueness constraints, format masks, allowed value lists, or cross-field dependencies?"
- **Sufficient when:** Validation rules documented per field (type, required, unique, format, allowed values, cross-field rules)
- **Insufficient when:** "Standard validation" with no field-level specification

### Probe 6: Interrupted Import
**Question:** "If the import is interrupted (network failure, browser close, server crash), what happens to the partially imported data? Is it rolled back, kept, or left in limbo?"
- **Sufficient when:** Interruption behavior defined (atomic transaction vs partial commit), recovery mechanism specified, user notification on resume
- **Insufficient when:** "It should handle that" with no concrete behavior

### Probe 7: Rollback
**Question:** "After a completed import, can the user undo it? Is there a rollback mechanism? Within what time window?"
- **Sufficient when:** Rollback strategy defined (undo mechanism, time window, scope of undo, audit trail), or explicit decision that rollback is not supported with rationale
- **Insufficient when:** "We could add an undo" with no commitment or design

### Probe 8: Duplicate Handling
**Question:** "If the imported data contains duplicates (within the file or against existing records), what happens? Skip, overwrite, merge, or reject?"
- **Sufficient when:** Duplicate detection strategy defined (match keys, scope), resolution behavior specified per scenario (within-file, against-existing)
- **Insufficient when:** "No duplicates" as an assumption without validation, or "we'll skip duplicates" without defining what constitutes a duplicate

### Probe 9: Progress Indicator
**Question:** "For large imports, is there a progress indicator? Does it show percentage, rows processed, estimated time? Can the user cancel mid-import?"
- **Sufficient when:** Progress UX defined (indicator type, cancel behavior, background processing option), or explicit small-file-only scope where progress is unnecessary
- **Insufficient when:** "It should show progress" with no design for cancel or background processing

### Probe 10: Permissions & Audit
**Question:** "Who can import? Who can export? Is there an audit log of imports (who, when, what file, how many records)? Are there different permission levels (view vs import vs import+delete)?"
- **Sufficient when:** Permission model defined per operation (import/export/rollback), audit log requirements specified (fields, retention, access)
- **Insufficient when:** "Admin can import" with no export permissions or audit trail

## Anti-Patterns

1. **Assuming small files** — No consideration for files with 10k+ rows, leading to timeout or memory issues in production
2. **No partial failure plan** — Import is all-or-nothing, but the file has 50,000 rows and row 49,999 fails
3. **No duplicate strategy** — Duplicates are discovered only when users complain about double entries after import
4. **Schema drift blindness** — Export format changes break downstream consumers, or import template changes without versioning confuse users

## Archetype Dimensions

These dimensions are added to `coverage-matrix.yaml` under `semantic_dimensions.archetype_dimensions`:

| Dimension | Covered when |
|-----------|-------------|
| `format_constraints_defined` | Accepted formats, column specs, templates, and validation rules per field are documented |
| `failure_recovery_defined` | Malformed row handling, interrupted import behavior, and rollback mechanism are specified |
| `volume_limits_defined` | Maximum file size, maximum rows, progress indicator design, and background processing strategy are documented |
