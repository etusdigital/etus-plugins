---
name: val-elicit
description: >
  Use when stress-testing documentation for ambiguities, contradictions, and
  developer confusion. Triggers on 'elicit', 'stress-test', 'challenge the spec',
  'find gaps', 'interrogate docs', 'what did we miss', or 'semantic review'.
model: opus
version: 1.0.0
argument-hint: "[feature-slug] [--focus=permissions|failures|consistency]"
---

# Elicit — Semantic Stress-Test Skill

## Purpose

Interrogate existing documentation to surface ambiguities, contradictions, missing boundaries, and hidden assumptions BEFORE they reach implementation. This skill does NOT create new product artifacts — it produces a findings report only.

## When to Use

- Before any gate validation (especially Implementation Readiness Gate)
- When the team feels "the spec looks complete but something feels off"
- After major scope changes to verify consistency survived
- When onboarding a new developer to verify docs are self-sufficient
- When the implementation-packet skill flags missing sections

## Scope Resolution

1. If `[feature-slug]` provided → scope to `docs/ets/projects/{project-slug}/features/{feature-slug}/`
2. If no argument → scope to full project `docs/ets/projects/{project-slug}/`
3. If `--focus` provided → run only the matching technique subset

## 8 Interrogation Techniques

### Technique 1: Developer Simulation
For each feature or user story, adopt the perspective of a developer who has never seen the codebase:
- Read the feature-spec, user-stories, and tech-spec for that feature
- List every question a developer would need to ask before writing the first line of code
- Flag each unanswered question as **EL-D-#**
- Common gaps: "which service handles this?", "what happens on timeout?", "who owns this data?"

### Technique 2: Cross-Doc Consistency
Compare overlapping definitions across documents:
- Database constraints (database-spec) vs validation rules (data-dictionary) vs API schema (api-spec) vs feature-spec business rules
- If a field is `NOT NULL` in DDL but optional in API request schema → **EL-C-#**
- If a field has `max_length: 255` in data-dictionary but no validation in API → **EL-C-#**
- If feature-spec says "admin only" but api-spec has no auth check on the endpoint → **EL-C-#**

### Technique 3: Vague Quantifier Scan
Search all documents for subjective language that should be quantified:
- Scan for: "fast", "quick", "secure", "scalable", "reliable", "easy", "simple", "many", "few", "most", "some", "real-time", "robust", "seamless", "efficient"
- For each occurrence outside of template/example blocks → **EL-A-#**
- Cross-reference with the Vague Terms Flag Table in validate-gate

### Technique 4: NG-# Violation Scan
Read all NG-# (non-goal) declarations from product-vision, feature-brief, or PRD:
- For each NG-#, search downstream documents for content that contradicts or implements the non-goal
- Example: NG-3 says "No mobile app" but wireframes include mobile layouts → **EL-C-#**
- Example: NG-1 says "No real-time sync" but API spec includes WebSocket endpoints → **EL-C-#**

### Technique 5: EDGE-# Resolution Audit
Collect all EDGE-# IDs from opportunity-pack, feature-spec, and user-stories:
- For each EDGE-#, trace forward to find a resolution (error handling, fallback, or explicit deferral)
- If an EDGE-# has no downstream resolution → **EL-E-#**
- If an EDGE-# is marked "deferred" but no deferral target (phase, ticket) exists → **EL-E-#**

### Technique 6: Missing Error Siblings
For each happy-path scenario (UC-#, US-# with happy-path Given/When/Then):
- Check if a corresponding error-path or edge-case scenario exists
- Missing error paths for: invalid input, timeout, permission denied, concurrent modification, empty state, rate limit exceeded
- Each missing error sibling → **EL-B-#**

### Technique 7: Permission Matrix Gap
Scan all documents for permission-related claims:
- "only admin can...", "managers have access to...", "authenticated users may..."
- For each claim, verify it traces to a formal role definition (in feature-spec permission matrix, api-spec auth section, or tech-spec security NFRs)
- Informal claims without formal backing → **EL-H-#**

### Technique 8: State Machine Completeness
For each entity that has lifecycle states (e.g., order: draft > pending > confirmed > shipped > delivered):
- Verify all valid transitions are documented
- Verify forbidden transitions are explicitly listed (e.g., "cannot go from delivered back to draft")
- Verify side effects per transition are documented (e.g., "on confirm: send email, create invoice")
- Missing transitions or side effects → **EL-B-#**

## Focus Dimension Mapping

| Flag | Techniques |
|------|-----------|
| `--focus=permissions` | #7 (deep), #1 (permission questions only) |
| `--focus=failures` | #5, #6, #8, #1 (failure questions only) |
| `--focus=consistency` | #2, #4, #3 |
| (no flag) | All 8 techniques |

## Output Format

The report is saved to `docs/ets/projects/{project-slug}/state/reports/elicit-report.md`.

```markdown
# Elicit Report — {project-slug} [{feature-slug | "full project"}]

Generated: {timestamp}
Scope: {path}
Focus: {all | permissions | failures | consistency}

## Summary

| Category | Count | Critical |
|----------|-------|----------|
| EL-A (Ambiguities) | N | N |
| EL-C (Contradictions) | N | N |
| EL-B (Missing Boundaries) | N | N |
| EL-H (Hidden Assumptions) | N | N |
| EL-E (Unresolved Edges) | N | N |
| EL-D (Developer Questions) | N | N |
| **Total** | **N** | **N** |

## Findings

### EL-A-001: {title}
- **Location:** {document} > {section}
- **Issue:** {description}
- **Severity:** HIGH | MEDIUM | LOW
- **Suggested Resolution:** {actionable fix}
- **Evidence:** "{quote from document}"

### EL-C-001: {title}
...

## Recommendations

1. {Highest priority fix}
2. {Second priority fix}
...

## Technique Coverage

| Technique | Ran | Findings | Notes |
|-----------|-----|----------|-------|
| 1. Developer Simulation | Yes/No | N | |
| 2. Cross-Doc Consistency | Yes/No | N | |
| 3. Vague Quantifier Scan | Yes/No | N | |
| 4. NG-# Violation Scan | Yes/No | N | |
| 5. EDGE-# Resolution Audit | Yes/No | N | |
| 6. Missing Error Siblings | Yes/No | N | |
| 7. Permission Matrix Gap | Yes/No | N | |
| 8. State Machine Completeness | Yes/No | N | |
```

## Severity Classification

| Severity | Meaning | Action |
|----------|---------|--------|
| **HIGH** | Would block or confuse implementation | Must fix before Implementation Readiness Gate |
| **MEDIUM** | Risk of rework or misinterpretation | Should fix, track as action item |
| **LOW** | Improvement opportunity | Nice to fix, no urgency |

## Integration Points

- **validate-gate:** Elicit findings feed into gate validation. HIGH findings from elicit should be treated as Layer 2 failures.
- **implementation-packet:** When the packet skill encounters a missing section, it recommends running `/elicit` to diagnose the gap.
- **correct-course:** After a mid-sprint scope change, run `/elicit` to verify consistency survived the change.

## Execution Steps

1. Resolve scope (feature-slug or full project)
2. Resolve focus dimension (all or filtered)
3. Load all documents in scope
4. Run each applicable technique sequentially
5. Collect and deduplicate findings
6. Classify severity (HIGH / MEDIUM / LOW)
7. Generate report
8. Save to `docs/ets/projects/{project-slug}/state/reports/elicit-report.md`
9. Display summary to user
10. Suggest next actions based on findings

## Notes

- This skill is READ-ONLY with respect to product artifacts. It never modifies existing documents.
- Zero findings is suspicious — for any project with > 5 documents, at least 3 findings are expected. If zero found, re-run with broader scope or acknowledge the exception.
- Findings IDs (EL-*-#) are local to the report and reset on each run. They are not persistent cross-session IDs.
