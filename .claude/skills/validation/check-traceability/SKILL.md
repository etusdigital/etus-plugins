---
name: check-traceability
description: >
  Use when validating ID consistency, checking for orphan references, or during gate
  validation. Also triggers when asking 'are all IDs connected', 'check traceability',
  'find broken links', or 'verify the requirements chain'.
user-invocable: false
context: fork
agent: Explore
model: sonnet
version: 1.0.0
---

# Check Traceability Skill

## Purpose

This skill validates **traceability** — the ability to trace each requirement or feature from business objective (BO-#) through design (PRD-F-#, US-#, JOUR-#, FS-#) to implementation (impl-#). It detects:

- **Orphan IDs** — ID with no upstream reference (e.g., US-001 with no PRD-F-001)
- **Broken links** — ID references non-existent upstream (e.g., FS-foo-001 references US-999 which doesn't exist)
- **Missing cross-references** — ID should have downstream but doesn't (e.g., FS-foo-001 not referenced in any impl-# or sprint)
- **Dead ends** — ID that is defined but never implemented (no impl-# or sprint reference)

This is a **READ-ONLY validation skill**. It runs in a forked context (Explore agent) with no write access. It returns a report of violations for the orchestrator or user to remediate.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** None — this is a validation tool.
**ENRICHES:** None.

This skill validates the traceability chain. It supports two chains depending on the work mode:

- **Product mode:** `ACT/JTBD/JOUR/UC/EDGE → BO-# → O-# → SOL-# → PRD-F-# → US-# → FS-{name}-# → impl-#`
- **Feature mode:** `ACT/JTBD/JOUR/UC/EDGE → SOL-# → FB-# → US-# → impl-#`

It scans existing documents and reports orphan IDs, broken links, and missing cross-references.

## Traceability Chains

### Product Mode (default)

The expected ID chain is:

```
ACT-# / JTBD-# / JOUR-# / UC-# / EDGE-# (Ideation Coverage)
  ↓
BO-# (Business Objective)
  ↓
O-# (Opportunity)
  ↓
SOL-# (Selected Solution Direction)
  ↓
PRD-F-# (Product Requirement / Feature)
  ↓                    ↘
US-# (User Story)    JOUR-# (User Journey)
  ↓                    ↗
FS-[name]-# (Feature Spec)
  ↓
impl-# (Implementation Item / Task)
```

**Note:** JOUR-# links to PRD-F-# through the Features column in journey steps. This creates a parallel traceability path: PRD-F-# → US-# (behavioral spec) AND PRD-F-# → JOUR-# (experience spec). Both paths converge at FS-# for implementation.

### Feature Mode

When Feature mode artifacts are detected (`docs/ets/projects/{project-slug}/features/` contains `feature-brief-*.md`), validate this chain instead:

```
ACT-# / JTBD-# / JOUR-# / UC-# / EDGE-# (Ideation Coverage)
  ↓
SOL-# (Selected Solution Direction)
  ↓
FB-# (Feature Brief Item)
  ↓
US-# (User Story, scoped)
  ↓
impl-# (Implementation Item / Task)
```

**Feature mode rules:**
- US-# in `features/{feature-slug}/user-stories.md` must reference FB-# (not PRD-F-#)
- impl-# in `features/{feature-slug}/impl-plan.md` must reference US-# from the same slug
- FB-# without downstream US-# is an orphan (unless marked as deferred)
- Do NOT require BO-#, PRD-F-#, JOUR-#, or FS-# for Feature mode artifacts

Each ID should have:
- **Upstream link** — Reference to the parent ID that justified it
- **Downstream link** — At least one child ID that implements it (except impl-# which may have no children)

## Scan Procedure

### Step 1: Extract All IDs

Scan `docs/ets/projects/{project-slug}/` for all ID patterns:

| Pattern | Regex | Location (Product mode) | Location (Feature mode) |
|---------|-------|-------------------------|------------------------|
| ACT-# | `ACT-\d+` | opportunity-pack.md | opportunity-pack.md |
| JTBD-# | `JTBD-\d+` | opportunity-pack.md | opportunity-pack.md |
| BO-# | `BO-\d{3}` | project-context.md, prd.md | N/A |
| O-# | `O-\d+` | ost.md | optional |
| SOL-# | `SOL-\d+` | solution-discovery.md | solution-discovery.md |
| PRD-F-# | `PRD-F-\d{3}` | prd.md | N/A |
| FB-# | `FB-\d+` | N/A | features/{feature-slug}/feature-brief.md |
| US-# | `US-\d{3}` | user-stories.md | features/{feature-slug}/user-stories.md |
| JOUR-# | `JOUR-\d{2}` | user-journey.md | N/A |
| UC-# | `UC-\d+` | opportunity-pack.md | opportunity-pack.md |
| EDGE-# | `EDGE-\d+` | opportunity-pack.md | opportunity-pack.md |
| NG-# | `NG-\d+` | opportunity-pack.md, prd.md | opportunity-pack.md, feature-brief.md |
| FS-[name]-# | `FS-[a-z]+-\d{3}` | feature-spec-*.md | N/A |
| impl-# | `impl-\d{3}` | implementation-plan.md (authority), execution-status.yaml (optional projection) | features/{feature-slug}/impl-plan.md |

For each ID found, record:
- **ID and location** (file, line)
- **Title/description** (context)
- **Upstream reference** (linked ID, if any)
- **Downstream references** (child IDs that depend on this)

Also compare the IDs found in documents against `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` when it exists:
- if coverage-matrix declares an item that is never used downstream, flag it as uncovered
- if downstream docs invent coverage-critical behavior with no upstream ideation ID, flag it as a gap
- if coverage-matrix uses an invalid item status, flag it as malformed checkpoint state
- if `meta.last_completed_step` or `meta.next_recommended_step` contradict the actual coverage, flag the checkpoint as inconsistent
- if `workflow_version` requires solution discovery and no `SOL-#` exists, fail the chain

### Step 2: Build Traceability Graph

Create a directed graph:
- Nodes = IDs
- Edges = upstream→downstream links
- Orphans = nodes with no upstream (except BO-# which has no upstream by definition)
- Dead ends = nodes with no downstream (except impl-# which may have none)

### Step 3: Detect Violations

For each ID:

1. **Ideation coverage check** — Does ACT/JTBD/JOUR/UC/EDGE feed at least one downstream item when the mode requires it?
2. **Coverage-matrix alignment check** — Does document usage match the status tracked in coverage-matrix.yaml?
3. **Checkpoint-state check** — Are step states and next-step guidance consistent with what is already covered?
4. **Opportunity-to-solution check** — Does every selected `O-#` feed at least one `SOL-#`?
5. **Solution-to-delivery check** — Does every selected `SOL-#` feed `PRD-F-#` or `FB-#`?
6. **Orphan Check** — Does it have an upstream link (except BO-#)?
7. **Broken Link Check** — Does the upstream ID exist?
8. **Downstream Check** — Does it have at least one downstream ID (except impl-#)?
9. **Dead End Check** — Is it a FS-# or PRD-F-# with no impl-# or sprint reference?

## NG-# Violation Check

For each NG-# found in upstream docs (opportunity-pack.md, feature-brief.md, prd.md):
1. Extract the **statement** field (what must NOT happen)
2. Search downstream docs (user-stories.md, feature-spec-*.md, api-spec.md, tech-spec.md, wireframes.md, implementation-plan.md) for behavior that contradicts the non-goal
3. Contradiction signals to look for:
   - User story that implements the excluded behavior (e.g., NG says "must NOT accept .xlsx" but US-# says "user uploads Excel file")
   - API endpoint that exposes the excluded capability
   - Feature spec that describes the forbidden workflow
   - Implementation task that builds the excluded functionality
4. If found → flag as **NG VIOLATION**: `"NG-{N} says '{statement}' but {doc} contains '{contradicting text}'"`
5. Report all violations in the traceability report under a dedicated `=== NG VIOLATIONS ===` section

**Severity:** NG violations are HIGH severity — they indicate the team is building something explicitly excluded from scope.

**Special cases:**
- NG-# with `scope: deferred_to_v2` — still a violation if found in current-phase docs. Deferred means "not now," not "maybe."
- NG-# with `scope: conditional` — check if the condition is met. If not met, treat as violation. If met, skip.
- NG-# referenced in an ADR-# that overrides it — not a violation (the ADR documents the intentional override).

## Report Format

Return a structured violation report:

```
Traceability Validation Report
Generated: [timestamp]
Scan Scope: docs/ets/projects/{project-slug}/
IDs Extracted: [count per type]
  ACT-#: N
  JTBD-#: M
  BO-#: K
  NG-#: J
  PRD-F-#: L
  US-#: P
  FS-#: Q
  impl-#: R

=== VIOLATIONS SUMMARY ===
Total Violations: Z
By Type:
  Orphans: X
  Broken Links: Y
  Dead Ends: W
  NG Violations: V
  [etc.]

=== VIOLATIONS DETAIL ===

ORPHAN: US-001 (docs/ets/projects/{project-slug}/user-stories.md:42)
  Description: "User can upload profile photo"
  Issue: No upstream PRD-F-# reference
  Remediation: Add "PRD-F-005" as upstream requirement

BROKEN LINK: FS-auth-003 (docs/ets/projects/{project-slug}/design/feature-spec-auth.md:88)
  Description: "OAuth integration"
  Issue: References US-999 which does not exist
  Remediation: Update reference to existing US-# (e.g., US-012)

DEAD END: PRD-F-002 (docs/ets/projects/{project-slug}/prd.md:54)
  Description: "Dark mode support"
  Issue: No FS-#, US-#, or impl-# references
  Remediation: Either (a) implement, or (b) descope from current phase

MISSING JOURNEY: PRD-F-003 (docs/ets/projects/{project-slug}/prd.md:67)
  Description: "User onboarding flow"
  Issue: Must Have feature not referenced in any JOUR-# step
  Remediation: Add JOUR-# entry covering this feature's user experience

=== NG VIOLATIONS ===

NG VIOLATION: NG-1 (docs/ets/projects/{project-slug}/discovery/opportunity-pack.md:95)
  Statement: "The system must NOT accept .xlsx files"
  Contradicted by: docs/ets/projects/{project-slug}/features/{feature-slug}/user-stories.md:28
  Contradicting text: "User uploads an Excel (.xlsx) file and sees a preview"
  Severity: HIGH
  Remediation: Either (a) remove the contradicting behavior from user-stories, or (b) create an ADR overriding NG-1

=== SUMMARY ===
✓ Pass: All IDs traceable
✗ Fail: Z violations found (see remediation steps above)
Completeness: X% (Y of Z expected IDs have full downstream)
```

## Execution Steps

1. **Scan documents** — Extract all ID patterns from `docs/ets/projects/{project-slug}/`
2. **Build graph** — Link upstream/downstream IDs
3. **Detect violations** — For each ID, check upstream, link validity, downstream existence
4. **Build report** — Aggregate violations by type and document
5. **Output** — Print report to stdout; return violation count
6. **Exit code** — 0 if no violations, 1 if violations found

## Integration Points

- **Orchestrator** — Calls check-traceability before Planning Gate and Implementation Readiness Gate
- **CI/CD** — May run on every PR to enforce traceability
- **Sprint Planning** — Verifies that sprint items have upstream feature specs

## Common Violations & Remediation

| Violation | Root Cause | Remediation |
|-----------|-----------|-------------|
| Orphan US-# | Feature added without PRD-F-# | Write PRD-F-# or link to existing one |
| Broken Link | Typo in ID reference | Fix ID reference (e.g., `US-101` → `US-010`) |
| Dead End PRD-F-# | Feature defined but never designed | Either (a) design and implement, or (b) move to backlog |
| Dead End FS-# | Feature spec written but never implemented | Create sprint task / impl-# item |
| Orphan impl-# | Implementation task without spec | Link to upstream FS-# or remove task |

## EDGE-# Resolution Chain

For each EDGE-# found in discovery artifacts:
1. Search downstream docs (user-stories, feature-spec, api-spec, tech-spec) for references
2. If found with handling (Given/When/Then, FS-# rule, ADR, error response) → status: resolved, via: [doc + section]
3. If not found → check NG-# registry for explicit deferral
4. If found in NG-# → status: deferred, via: NG-{N}
5. If neither → flag as TRACEABILITY GAP: "EDGE-{N} has no downstream resolution"

Report edge_resolution findings in the traceability report output.
The CALLER (validate-gate or orchestrator) is responsible for persisting
edge_resolution updates to coverage-matrix.yaml based on this report.
check-traceability remains read-only.

## Notes

- **Partial traceability allowed** — A FS-# may be defined without all US-# (if it spans multiple user stories)
- **Many-to-many links possible** — One PRD-F-# may link to multiple US-#; one FS-# may implement multiple PRD-F-#
- **Backlog exclusion** — IDs in a "backlog" section may have no downstream (they're not in scope)
- **Draft status** — IDs marked as "draft" or "proposed" may skip downstream checks

## Knowledge Pointers

- **ID Scheme**: `docs/ets/projects/{project-slug}/.guides/id-scheme.md` — Complete ID naming and traceability rules
- **Reference**: `docs/ets/projects/{project-slug}/ids.yml` — Centralized ID registry (optional, for validation)

## INPUT VALIDATION

No input validation required — this skill scans whatever documents exist.
Minimum: at least `product-vision.md` (with BO-#) and one downstream document for meaningful traceability check.

## OUTPUT VALIDATION

The output is a traceability report. Validate:
- [ ] All ID types checked (BO-#, PRD-F-#, US-#, JOUR-#, FS-#, impl-#, NFR-#, ADR-#, NG-#)
- [ ] Orphan IDs listed (defined but never referenced downstream)
- [ ] Broken links listed (referenced but never defined upstream)
- [ ] Coverage percentage calculated (e.g., "85% of BO-# have PRD-F-# coverage")
- [ ] Recommendation for each broken link

## WORKFLOW

### Step 1: ID Extraction
- **Input:** All documents in `docs/ets/projects/{project-slug}/`
- **Action:** Extract all IDs matching patterns: BO-\d+, PRD-F-\d+, US-\d+, JOUR-\d+, FS-\w+-\d+, impl-\d+, NFR-\d+, ADR-\d+
- **Output:** ID registry (id, type, defined_in, referenced_in)

### Step 2: Chain Validation
- **Input:** ID registry
- **Action:** For each BO-#, trace forward: does it have PRD-F-#? Does that PRD-F-# have US-#? etc.
- **Output:** Chain completeness map

### Step 3: Report Generation
- **Input:** Chain map
- **Action:** Format orphans, broken links, coverage percentages
- **Output:** Traceability report (stdout or markdown)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| No documents found | Info | Report "No documents to validate" | Exit cleanly |
| Only Phase 1 docs exist | Info | Report partial chain (BO-# only) | Note: "Downstream phases not yet generated" |
| ID format ambiguous | Low | Flag for user review | Skip ambiguous match |
