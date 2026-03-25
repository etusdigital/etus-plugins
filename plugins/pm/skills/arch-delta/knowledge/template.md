---
doc_meta:
  id: dd
  display_name: Design Delta
  pillar: Architecture
  owner_role: Tech Lead
  summary: Documents only what changes in architecture for a specific feature.
  order: 0
  requires: [fb]
  feeds: [impl-plan]
---

# Template: Design Delta

**File:** `docs/ets/projects/{project-slug}/features/{feature-slug}/design-delta.md`

**Purpose:** Document ONLY the architectural changes required for a specific feature. Not a full architecture review — a focused delta showing what is new, modified, or removed.

## Responsaveis

- **Owner:** Tech Lead
- **Contribuem:** PM, Dev team
- **Aprovacao:** PM + Tech Lead

## Table of Contents
1. [Complete Structure](#complete-structure)
2. [Filling Notes](#filling-notes)
3. [Concrete Example](#concrete-example-minimal)
4. [Validation](#validation)

---

## Complete Structure

```markdown
# Design Delta: [Feature Name]

**Date:** [DATE]
**Feature Brief:** [link to features/{feature-slug}/feature-brief.md]
**Status:** [DRAFT | APPROVED]
**Mode:** Feature

---

## Summary of Changes

[1-2 sentence overview of what changes and why]

## API Changes

### New Endpoints
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| [POST] | [/api/v1/resource] | [What it does] | [JWT/API key] |

### Modified Endpoints
| Endpoint | Change | Reason |
|----------|--------|--------|
| [existing endpoint] | [what changes] | [why] |

### Removed Endpoints
[If any — typically rare]

## Database Changes

### New Tables

[DDL or structured description]

### Modified Tables
| Table | Change | Migration Notes |
|-------|--------|-----------------|
| [table] | [add column X] | [reversible: yes/no] |

### New Indexes
| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| [table] | [idx_name] | [columns] | [why needed] |

### Data Migration
[If existing data needs transformation]

## UI Changes

### New Screens
- [Screen name]: [purpose, key components]

### Modified Screens
- [Screen name]: [what changes, why]

### New Components
- [Component name]: [reusable? where used?]

## Infrastructure Changes

[Only if applicable — new services, config changes, environment variables, third-party integrations]

### New Environment Variables
| Variable | Purpose | Example Value |
|----------|---------|---------------|
| [VAR_NAME] | [what it configures] | [example] |

### New Services/Dependencies
- [Service]: [why needed, how it connects]

## Migration Plan

- [ ] Database migration reversible?
- [ ] API backward compatible?
- [ ] Feature flag needed?
- [ ] Data backfill required?
- [ ] Rollback procedure documented?

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [risk description] | [Low/Med/High] | [Low/Med/High] | [how to mitigate] |


## O que fazer / O que nao fazer

**O que fazer:**
- Listar todos os componentes afetados explicitamente
- Documentar migrations de schema com rollback
- Avaliar impacto em NFR-# existentes
- Incluir risco e mitigacao para cada mudanca

**O que nao fazer:**
- Nao redesenhar arquitetura inteira (delta = diferenca, nao sistema completo)
- Nao propor mudancas sem referenciar o feature-brief
- Nao ignorar impacto em API contracts existentes
- Nao esquecer backward compatibility

## Related Documents

- Feature Brief: [link]
- Architecture Diagram: [link if exists]
- Tech Spec: [link if exists]
- Database Spec: [link if exists]
- API Spec: [link if exists]
```

---

## Filling Notes

### Section: Summary of Changes

- Maximum 2 sentences
- Answer: "What is changing and why?"
- Example: "Adding a new bulk import endpoint and a background job table to support CSV upload. This requires 1 new API endpoint, 1 new DB table, and modifications to the existing customer creation flow."

### Section: API Changes

- **New Endpoints:** Full method + path + description + auth requirement
- **Modified Endpoints:** Reference existing endpoint, describe the change, explain why
- For each endpoint, consider: request body changes, response shape changes, new query parameters, rate limiting changes
- If no API changes: write "No API changes required for this feature."

### Section: Database Changes

- **New Tables:** Provide column names, types, and constraints (DDL preferred but structured description acceptable)
- **Modified Tables:** Specify exactly which columns/constraints change
- **Indexes:** New indexes needed for query performance
- **Migrations:** Note whether migrations are reversible (can you roll back without data loss?)
- If no DB changes: write "No database changes required for this feature."

### Section: UI Changes

- **New Screens:** Name, purpose, key interaction patterns
- **Modified Screens:** What specifically changes in the existing screen
- **Components:** New reusable components created for this feature
- Keep descriptions focused on WHAT changes, not pixel-perfect designs
- If no UI changes: write "No UI changes required for this feature."

### Section: Infrastructure Changes

- Only include if the feature requires new services, environment variables, third-party integrations, or configuration changes
- If no infra changes: write "No infrastructure changes required for this feature."

### Section: Migration Plan

- Every design delta should have a migration plan, even if simple
- Answer: "Can we safely deploy this? Can we safely roll it back?"
- Feature flags are recommended for any user-facing change that could be reverted independently

---

## Concrete Example (Minimal)

```markdown
# Design Delta: CSV Bulk Import

**Date:** 2026-03-17
**Feature Brief:** docs/ets/projects/{project-slug}/features/feature-brief-csv-bulk-import.md
**Status:** APPROVED
**Mode:** Feature

---

## Summary of Changes

Adding a bulk import endpoint and background processing to support CSV customer uploads. Requires 1 new API endpoint, 1 new DB table, and a background job processor.

## API Changes

### New Endpoints
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/v1/customers/import | Upload CSV file for bulk customer creation | JWT (admin role) |
| GET | /api/v1/customers/import/{job_id} | Check import job status and results | JWT (admin role) |

### Modified Endpoints
| Endpoint | Change | Reason |
|----------|--------|--------|
| POST /api/v1/customers | Add `source` field to request body | Track whether customer was created via UI or bulk import |

## Database Changes

### New Tables

```sql
CREATE TABLE import_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  file_name VARCHAR(255) NOT NULL,
  total_rows INTEGER NOT NULL,
  processed_rows INTEGER DEFAULT 0,
  failed_rows INTEGER DEFAULT 0,
  status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
  error_log JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);
```

### Modified Tables
| Table | Change | Migration Notes |
|-------|--------|-----------------|
| customers | Add column `source VARCHAR(20) DEFAULT 'ui'` | Reversible: yes (drop column) |

### New Indexes
| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| import_jobs | idx_import_jobs_user_status | (user_id, status) | Query user's active imports |

## UI Changes

### New Screens
- **Bulk Import Page** (/admin/import): Drag-and-drop CSV upload, column mapping preview, import progress tracker

### Modified Screens
- **Customer List** (/admin/customers): Add "Import" button in toolbar, add "Source" column to table

## Infrastructure Changes

### New Environment Variables
| Variable | Purpose | Example Value |
|----------|---------|---------------|
| IMPORT_MAX_FILE_SIZE_MB | Maximum CSV file size | 10 |
| IMPORT_MAX_ROWS | Maximum rows per import | 10000 |
| IMPORT_RATE_LIMIT_PER_HOUR | Max imports per user per hour | 5 |

## Migration Plan

- [x] Database migration reversible? Yes — new table can be dropped, new column has default value
- [x] API backward compatible? Yes — new endpoints only, existing endpoint change is additive (new optional field)
- [x] Feature flag needed? Yes — `FEATURE_BULK_IMPORT` to enable/disable the import button and endpoints
- [ ] Data backfill required? No
- [x] Rollback procedure documented? Drop table, remove column, disable feature flag

## Related Documents

- Feature Brief: docs/ets/projects/{project-slug}/features/feature-brief-csv-bulk-import.md
```

---

## Validation

**Before finalizing Design Delta:**

- [ ] At least 1 change section has content (API, DB, UI, or Infra)
- [ ] Sections with no changes explicitly state "No changes required"
- [ ] Each change clearly states what is new vs. modified vs. removed
- [ ] Migration plan checklist is filled out
- [ ] Feature brief is linked at the top of the document
- [ ] Summary of Changes is concise (1-2 sentences)
