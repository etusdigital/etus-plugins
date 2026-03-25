# Implementation Packet — {feature-slug}

> **Generated:** {timestamp}
> **Scope:** {feature-slug}
> **Status:** NON-AUTHORITATIVE — this document consolidates content from authoritative sources. Do not edit directly; update the source document instead.

---

## 1. Context & Non-Goals [Authority: feature-brief.md + NG-# registry]

### Feature Context
{Brief description of the feature, its purpose, and how it fits into the product.}

### Non-Goals (NG-#)
{List of NG-# items relevant to this feature. These define what this feature explicitly does NOT do.}

| ID | Non-Goal | Source |
|----|----------|--------|

---

## 2. Actors & Permissions [Authority: opportunity-pack.md + feature-spec]

### Actors
{List of actors who interact with this feature.}

### Permission Matrix
| Action | {Role A} | {Role B} | {Role C} |
|--------|----------|----------|----------|

---

## 3. Business Rules [Authority: feature-brief FB-# + feature-spec]

| Rule ID | Description | Condition | Outcome |
|---------|-------------|-----------|---------|

---

## 4. Acceptance Criteria [Authority: user-stories.md]

{Filtered US-# for this feature with Given/When/Then.}

### US-{NNN}: {title}
**Given** {precondition}
**When** {action}
**Then** {expected result}

---

## 5. Error Handling [Authority: feature-spec error handling matrix]

| Scenario | EDGE-# | Trigger | System Response | User Message | Retry? | Rollback? |
|----------|--------|---------|-----------------|--------------|--------|-----------|

---

## 6. State Machine [Authority: feature-spec]

### States
{Mermaid diagram or table of states and transitions.}

### Transition Table
| From | To | Trigger | Side Effects | Forbidden? |
|------|----|---------|--------------|------------|

---

## 7. API Contracts [Authority: api-spec.md]

{Filtered endpoints for this feature.}

### Endpoint: {METHOD} {path}
- **Description:** {description}
- **Auth:** {auth requirement}
- **Request:** {schema summary}
- **Response:** {schema summary}
- **Error codes:** {list}
- **Idempotency:** {key/strategy if mutation}

---

## 8. Data Mutations & Validation [Authority: database-spec.md + data-dictionary.md]

### Tables Affected
| Table | Operation | Key Fields | Constraints |
|-------|-----------|------------|-------------|

### Validation Rules
| Field (dict.*) | Required | Format | Min/Max | Default | On Invalid |
|-----------------|----------|--------|---------|---------|------------|

---

## 9. Performance NFR-# [Authority: tech-spec.md]

| NFR-# | Category | Target | Measurement | Verification |
|-------|----------|--------|-------------|-------------|

---

## 10. Observability [Authority: tech-spec.md observability section]

### Logs
| Event | Level | Structured Fields | When |
|-------|-------|-------------------|------|

### Metrics
| Metric Name | Type | Labels | Description |
|-------------|------|--------|-------------|

### Alerts
| Condition | Severity | Channel | Runbook |
|-----------|----------|---------|---------|

---

## 11. Tasks impl-# [Authority: implementation-plan.md]

| impl-# | Task | Estimate | Dependencies | Sprint |
|---------|------|----------|--------------|--------|

---

## 12. Open Questions [Authority: all sources]

{Always present. Consolidates unresolved items from all authority documents.}

| ID | Question | Source | Blocks? | Owner |
|----|----------|--------|---------|-------|

### Open Assumptions (ASM-#)
| ASM-# | Assumption | Validation Path | Status |
|-------|-----------|-----------------|--------|
