---
name: val-gate
description: >
  Use when checking if a phase is ready to proceed, reviewing phase quality, or
  approving a gate. Also triggers on 'validate', 'are we ready', 'gate check',
  'review phase', 'GO/NO-GO', or 'can we move to the next phase'.
model: opus
version: 1.0.0
argument-hint: "[phase]"
---

# Validate Gate Skill

## Purpose

This skill executes an **interactive quality gate** for any phase of the documentation workflow. It:

1. **Checks document completeness** — Verifies that all required documents for the phase are present and populated
2. **Runs validation checks** — Calls check-sst and check-traceability to detect rule violations
3. **Presents results** — Shows the user a clear GO/NO-GO/ITERATE recommendation with details
4. **Asks for decision** — Collects user input (GO / NO-GO / ITERATE / DESCOPE / REDESIGN) before proceeding

Gates are the control points in the workflow where stakeholders decide whether to proceed to the next phase. The opening ideation layer uses an Ideation Readiness Gate before Discovery/Planning artifacts are allowed to run downstream.

## 3-LAYER VALIDATION

Gate validation runs in 3 sequential layers. Each layer must pass before proceeding to the next. If a layer fails, stop and report — do not continue to subsequent layers.

### Layer 1: Structure (Fast Fail)
Checks that required documents exist and have the correct format:
- [ ] All required documents for this phase exist at expected paths
- [ ] Each document has the required sections (headings match template)
- [ ] ID sequences are present and correctly formatted (BO-#, PRD-F-#, US-#, FS-#, impl-#, etc.)
- [ ] No empty required sections (section exists but has no content)
- [ ] No unresolved [TODO] or [TBD] placeholders in required sections

### Anti-Placeholder Patterns (Layer 1 extension)
Reject automatically if found in required sections:
- Text inside brackets: [SOMETHING], [USER], [ACTION], [RESULT], [VALUE]
- NFR-# without a number: "fast", "quick", "scalable", "secure", "reliable" without metric
- Given/When/Then with < 5 words per clause
- Empty table cells in required tables
- "TBD", "TODO", "to be defined", "a definir" in any form
Exception: skip template files, example blocks, and quoted guidance text.

**If any check fails:** Report "STRUCTURE FAILURE" with list of missing/malformed items. Do NOT proceed to Layer 2.

### Layer 2: Content (Deep Check)
Checks that document content meets quality standards:
- [ ] Business objectives have measurable success metrics (not vague)
- [ ] Features have clear scope boundaries (what's in vs. out) and acceptance criteria
- [ ] User stories follow Given/When/Then with specific values (not placeholders)
- [ ] Technical specs have quantified NFRs (numbers, not "fast" or "scalable")
- [ ] Architecture decisions have trade-off analysis documented
- [ ] API schemas are complete and machine-readable
- [ ] Design tokens (tok.*) are properly categorized and documented
- [ ] Data dictionary entries are comprehensive with types and descriptions

#### Semantic Dimension Check

Mandatory dimensions are defined in `state_defaults.py → MODE_DIMENSION_RULES`.
This is the SINGLE SOURCE OF TRUTH for which dimensions are required per mode.

For the current mode, read the `required` list from MODE_DIMENSION_RULES:
- If a required dimension status == "missing" AND no "not_applicable" justification → FAIL
- If a required dimension status == "partial" → WARN

The `conditional` dimensions generate warnings but do not block the gate.
The `recommended` dimensions are informational only.

Do NOT duplicate the per-mode rules here. If the rules need to change,
change them in state_defaults.py and they propagate automatically.

#### EDGE Resolution Check
For each EDGE-# in edge_resolution:
- If status == "unresolved" → FAIL with gap description
- failure_modes dimension is only "covered" when ALL EDGE-# are resolved or deferred

### Vagueness Checks (Layer 2 extension)
- Every NFR-# must contain at least one number (ms, %, req/s, etc.)
- Every US-# happy-path must have at least 1 US-# or EDGE-# error-path sibling
- Every permission claim ("only admin can...") must trace to a formal role definition
- Absence of at least 1 error scenario per feature is a CONTENT GAP

### Vague Terms Flag Table
| Term | Required Replacement |
|------|---------------------|
| "fast" | "response time < X ms at p95" |
| "easy to use" | "new user completes [task] without help in < X min" |
| "secure" | specific threat model + encryption + auth requirements |
| "scalable" | "supports X concurrent users / Y req/s" |
| "real-time" | "latency < X ms" |
| "robust" | "handles [specific failures] with [specific behavior]" |
| "seamless" | specific integration/transition requirements |

**If any check fails:** Report "CONTENT GAPS" with specific items needing improvement. Do NOT proceed to Layer 3.

### Layer 3: Dependencies (Cross-Document)
Checks consistency and traceability across documents:
- [ ] Every BO-# traces forward to at least 1 PRD-F-#
- [ ] Every Must Have PRD-F-# traces to at least 1 US-# AND at least 1 design artifact (FS-#, JOUR-#, etc.)
- [ ] Every US-# references a valid PRD-F-#
- [ ] Every FS-# references a valid PRD-F-#
- [ ] No orphan IDs (IDs referenced but never defined)
- [ ] SST rules respected (no Given/When/Then outside user-stories.md, no DDL outside database-spec.md, no tok.* outside style-guide.md, no dict.*/ev.* outside data-dictionary.md, no NFR-# or ADR-# redefinitions)
- [ ] Phase handoff JSON is complete and references all generated documents
- [ ] Document completeness ≥ 90% (minimal TODOs in non-required sections)

**If any check fails:** Report "DEPENDENCY VIOLATIONS" with specific broken links and violations.

### Gate Decision
Only after all 3 layers pass can the gate recommend GO. Decision options:
- **GO** — All 3 layers pass. Proceed to next phase.
- **ITERATE** — Layer 2 or 3 has minor issues (fixable in current phase). Fix and re-validate.
- **DESCOPE** — Scope too large. Remove features from "Must" to "Should"/"Won't" and re-validate (Planning/Implementation gates only).
- **REDESIGN** — Layer 1 passes but design conflicts detected in Layer 3. Return to Design phase (Implementation Readiness Gate only).
- **NO-GO** — Layer 1 fails or Layer 2/3 has critical gaps. Major rework needed or project viability at risk.

## Gate Decision Persistence

When gate result is ITERATE or NO-GO:
1. Ask user for feedback: "What needs to change before this can proceed?"
2. Save to workflow-state.yaml gate section:
   - feedback: user's feedback text
   - rejected_approaches: list of what was tried and failed
   - timestamp: current ISO timestamp
   - increment iteration_count
3. When gate result is GO:
   - Save timestamp
   - Clear unresolved_objections
4. Downstream phases MUST read gate decisions before starting work to avoid re-proposing rejected approaches.

## MODE-AWARE VALIDATION THRESHOLDS

Validation thresholds vary by work mode. The mode is read from `state/project-status.yaml` if it exists, or passed as an argument (e.g., `--mode feature`). If neither is available, default to **Product** mode (strictest thresholds).

### Product mode (default — strict thresholds)

These are the standard thresholds used throughout this document. No relaxation.

- US-# >= 5 (minimum 5 user stories)
- Acceptance criteria >= 3 per user story (Given/When/Then)
- Coverage matrix required (PRD-F-# to US-# mapping with full traceability)
- Competitive landscape required in product-vision.md
- SST check runs across all project documents (full scope)
- All 3 validation layers enforced (Structure, Content, Dependencies)

### Feature mode (relaxed thresholds)

Feature mode generates fewer, more focused documents. Validation is scoped accordingly.

- US-# >= 1 (minimum 1 user story — not >= 5)
- Acceptance criteria >= 1 per user story (not >= 3)
- `feature-status.md` required for each active feature workflow
- Coverage matrix is recommended because Feature mode now starts from ideation, but thresholds are scoped
- No competitive landscape required
- SST check scoped to the active feature folder only (files in `docs/ets/projects/{project-slug}/features/{feature-slug}/`), not the full project
- Layer 3 (Dependencies) checks traceability within feature scope only: SOL-# -> FB-# -> US-# -> impl-#
- Gate decisions available: GO / ITERATE only (no DESCOPE or REDESIGN)

### Bug mode (minimal thresholds)

Bug mode produces a single document. Validation checks only essential content.

- Problem described clearly (non-empty problem statement section)
- Fix approach documented (non-empty fix approach section)
- Test plan present (>= 1 test case defined)
- Rollback plan present (non-empty rollback section)
- No traceability checks (bugs may or may not link to existing IDs)
- No SST checks (single standalone document)
- Gate decisions available: GO / ITERATE only

### Spike mode (minimal thresholds)

Spike mode produces a single research document. Validation checks only essential content.

- Research question stated (non-empty research question section)
- Findings documented (>= 1 finding with evidence)
- Recommendation present (non-empty recommendation section)
- No traceability checks
- No SST checks
- Gate decisions available: GO / ITERATE only

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** None — this skill runs at phase boundaries, after documents are generated.
**ENRICHES:** None.

This skill executes quality gate validation for any phase (Ideate, Discovery, Planning, Design). It reads the dependency graph to know which documents should exist for the given phase, then validates completeness.

### Gate 0: Ideation Readiness Gate (Opening Layer)

**Required Documents:**
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Filled with actors, JTBDs, journeys, use cases, edge cases, guardrails, and assumptions
- `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml` — Filled with threshold counts and readiness status

**Checks:**
- Problem is defined independently from the proposed solution
- Actors identified
- JTBD coverage threshold met for the mode
- Journey coverage threshold met for the mode
- Use-case coverage threshold met for the mode
- Edge-case coverage threshold met for the mode
- Guardrails defined
- Blocking questions explicit
- `coverage-matrix.yaml` identifies the incomplete semantic block when coverage is missing
- `meta.last_completed_step` and `meta.next_recommended_step` are coherent

**Decision Points:**
- **GO** — Coverage is strong enough to derive downstream documentation
- **ITERATE** — Coverage gaps remain and ideation must continue

**If ITERATE:** The report should explicitly say which subcommand to run next
(for example `/ideate jobs`, `/ideate edges`, or `/ideate synth`).

## Gate Types & Checklists

### Gate 1: Discovery Gate (End of Phase 1)

**Required Documents:**
- `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md` — Filled and approved or explicitly marked draft with known gaps
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Filled (background, problem statement, constraints)
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — Filled (vision, success metrics, assumptions)

**Checks:**
- Document completeness (sections present, no [TODO])
- No SST violations (lightweight check — not all rules apply to discovery)
- Opportunity Pack to Discovery derivation is visible (actors, JTBDs, and open questions are reflected downstream)
- User alignment (did discovery interviews surface key insights?)

**Decision Points:**
- **GO** — Vision is clear, constraints documented, team aligned → proceed to Planning
- **ITERATE** — Missing insights, unclear constraints → run another discovery cycle
- **NO-GO** — Problem statement is unclear → stop and reassess project viability

### Gate 2: Planning Gate (End of Phase 2)

**Opportunity Focus sub-gate**
- `docs/ets/projects/{project-slug}/planning/ost.md`
- `docs/ets/projects/{project-slug}/planning/prioritization.md`
- Opportunities are explicit, evidence-backed, and not disguised solutions
- Selected `O-#` items are clear enough to enter solution discovery

**Solution Readiness sub-gate**
- `docs/ets/projects/{project-slug}/planning/solution-discovery.md` for Product mode
- `docs/ets/projects/{project-slug}/features/{feature-slug}/solution-discovery.md` for Feature mode
- At least 2 `SOL-#` options were considered unless scope is trivially narrow
- Value, usability, viability, and feasibility risks were evaluated
- Unresolved risks are explicit
- A recommended solution exists
- Experiments are defined when confidence is not high

**Required Documents:**
- `docs/ets/projects/{project-slug}/planning/prd.md` — Filled (features, success criteria, acceptance, trade-offs)
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — Filled (US-# with Given/When/Then)
- `docs/ets/projects/{project-slug}/planning/feature-specs/feature-spec-*.md` (1+) — Filled when needed (FS-# with detailed specs)

**Checks:**
- Document completeness (all required sections present)
- SST validation (Given/When/Then only in user-stories.md, no NFR-# redefinitions, no ADR-# duplicates)
- Traceability validation (ACT/JTBD/JOUR/UC/EDGE → O-#/SOL-#/BO-#/FB-# → PRD-F-#/US-#/FS-# chain complete, no orphans)
- Prioritization (Must/Should/Could/Won't tagged, scope is realistic)

**Decision Points:**
- **GO** — Features are clear, priorities set, acceptance criteria defined → proceed to Design
- **DESCOPE** — Scope too large, move some features to "Won't" or future phases
- **ITERATE** — Acceptance criteria are vague, traceability incomplete → refine PRD/specs
- **NO-GO** — Fundamental requirements conflict → reassess product strategy

**Compatibility rule:** If the project is legacy and does not declare the new workflow version, solution discovery may be absent without failing the gate. For the new workflow version, it is mandatory. In Feature mode, the scoped file is `features/{feature-slug}/solution-discovery.md`.

### Gate 3: Implementation Readiness Gate (End of Phase 3, after Design)

**Required Documents:**
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — Filled (C4 levels, deployment view)
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Filled (NFR-#, ADR-#, all quantified)
- `docs/ets/projects/{project-slug}/data/database-spec.md` — Filled (DDL, schema, indexes)
- `docs/ets/projects/{project-slug}/data/data-dictionary.md` — Filled (dict.*, ev.* definitions)
- `docs/ets/projects/{project-slug}/ux/style-guide.md` — Filled (tok.*, design system)
- `docs/ets/projects/{project-slug}/ux/*.md` (4+) — Filled (UX flows, wireframes, interaction specs)
- `docs/ets/projects/{project-slug}/implementation/api-spec.md` — Filled (endpoints, schemas, errors)

**Checks:**
- Document completeness (all required sections present, diagrams rendered, links valid)
- SST validation (all NFR-# in tech-spec.md, all DDL in database-spec.md, all tok.* in style-guide.md, all dict.*/ev.* in data-dictionary.md)
- Traceability validation (ideation and planning coverage survives into design, and FS-# → impl-# chain starts; all FS-# have implementation roadmap)
- Technical readiness (NFRs are quantified, ADRs are detailed, infrastructure is defined)
- Resource planning (Do we have the team/tools/time to implement?)

**Decision Points:**
- **GO** — Design is complete, NFRs are quantified, team is ready → proceed to Implementation
- **REDESIGN** — Architecture conflicts with constraints, NFRs unrealistic → iterate design
- **ITERATE** — Some design areas incomplete (e.g., missing ux-design specs) → complete before gate
- **NO-GO** — Design reveals infeasibility (cost, complexity, timeline) → reassess project

## ADVERSARIAL REVIEW MODE

When invoked with the `--adversarial` flag, or when the orchestrator runs validation before the **Implementation Readiness Gate** (Gate 3), the reviewer switches to adversarial mode. This mode exists because confirmation bias is real — reviewers who helped create the documents naturally see them as complete. Adversarial review forces a critical lens.

### Adversarial Stance

In adversarial mode, the reviewer adopts a **cynical stance**: assume problems exist and actively look for them. The goal is not to block progress, but to surface issues that would otherwise be discovered during implementation — when they are far more expensive to fix.

The reviewer acts as a skeptical stakeholder who has seen projects fail and knows where the weak points typically hide: vague NFRs, untested edge cases, missing error handling, implicit assumptions, and scope creep disguised as "nice-to-haves".

### Minimum Findings Requirement

- **Minimum 5 findings required** before the gate can recommend GO. This forces thorough analysis and prevents rubber-stamping.
- **Zero findings triggers mandatory re-analysis.** Zero findings means the review was not thorough enough — go back and look harder. No real design is perfect.
- If fewer than 5 findings are found after thorough analysis, document why fewer were found (e.g., "This is a very small scope with only 2 endpoints and 1 entity") and explicitly justify the exception.

### Finding Severity Levels

Each finding is categorized by severity:

| Severity | Meaning | Effect on Gate |
|----------|---------|----------------|
| **HIGH** | Blocks GO — must be fixed before proceeding | Automatically changes recommendation to ITERATE |
| **MEDIUM** | Should fix — significant risk if left unaddressed | Does not block GO, but tracked as post-gate action items |
| **LOW** | Informational — improvement opportunity | Noted for future reference, no effect on gate decision |

**Any HIGH finding automatically changes the gate recommendation to ITERATE**, regardless of how many items pass validation.

### Finding Format

Each finding must include these fields:

```
### Finding F-{N}: {brief title}

- **Location:** {document name} → {section or ID}
- **Issue:** {clear description of what's wrong or missing}
- **Severity:** HIGH | MEDIUM | LOW
- **Suggested Fix:** {concrete, actionable recommendation}
- **Evidence:** {quote or reference from the document that demonstrates the issue}
```

Example:
```
### Finding F-1: NFR-3 latency target is not measurable

- **Location:** tech-spec.md → NFR-3 (API Response Time)
- **Issue:** NFR-3 says "API should be fast" but does not specify a measurable target (e.g., P99 < 200ms)
- **Severity:** HIGH
- **Suggested Fix:** Replace "fast" with a specific latency target: "P99 < 200ms for read endpoints, P99 < 500ms for write endpoints"
- **Evidence:** "NFR-3: API Response Time — The API should respond quickly to all requests."
```

### Adversarial Review Checklist

In addition to the standard 3-layer validation, adversarial mode runs these additional checks:

**Architecture & Design:**
- [ ] Are there single points of failure not addressed in the architecture?
- [ ] Do NFRs have specific, measurable targets (not vague adjectives)?
- [ ] Are ADR alternatives genuinely considered, or just straw men?
- [ ] Is the scalability strategy tested against 10x growth, not just current load?
- [ ] Are security assumptions documented and validated?

**Data & API:**
- [ ] Are all edge cases in the data model covered (nulls, empty strings, max lengths)?
- [ ] Do API error responses cover all realistic failure modes?
- [ ] Is there a data migration strategy for schema changes?
- [ ] Are rate limits justified by actual capacity analysis?

**UX & Implementation:**
- [ ] Do wireframes account for error states, empty states, and loading states?
- [ ] Is the implementation plan's critical path realistic given team capacity?
- [ ] Are estimate ranges provided (not single-point estimates)?
- [ ] Is there a rollback plan for each deployment step?

**Cross-Cutting:**
- [ ] Are there implicit assumptions that should be explicit?
- [ ] Is scope creep hiding in "Could Have" features that are actually needed?
- [ ] Are dependencies on external services documented with fallback plans?
- [ ] Is the testing strategy adequate for the risk level?

### Adversarial Output Format

```
╔════════════════════════════════════════════════════════════════╗
║           ADVERSARIAL REVIEW — {PHASE} GATE                    ║
╚════════════════════════════════════════════════════════════════╝

Review Mode: ADVERSARIAL
Timestamp: {date}
Reviewer Stance: Cynical — assuming problems exist

━━━ STANDARD VALIDATION (3-Layer) ━━━
Layer 1 (Structure): {PASS/FAIL}
Layer 2 (Content):   {PASS/FAIL}
Layer 3 (Dependencies): {PASS/FAIL}

━━━ ADVERSARIAL FINDINGS ({N} total) ━━━

HIGH ({N}):
  F-1: {title} — {location}
  F-2: {title} — {location}

MEDIUM ({N}):
  F-3: {title} — {location}

LOW ({N}):
  F-4: {title} — {location}
  F-5: {title} — {location}

━━━ RECOMMENDATION ━━━
Status: {GO | ITERATE}
Reason: {rationale — if ITERATE, list HIGH findings that must be resolved}

━━━ ACTION ITEMS ━━━
Before proceeding:
  1. {fix for HIGH finding F-1}
  2. {fix for HIGH finding F-2}

Post-gate (tracked):
  3. {fix for MEDIUM finding F-3}

━━━ DECISION REQUIRED ━━━
{standard decision prompt}
```

## Checklist Structure

For each gate, present a checklist with checkmarks:

```
=== DISCOVERY GATE CHECKLIST ===

Document Completeness:
  ✓ project-context.md present and filled (X% complete)
  ✓ product-vision.md present and filled (X% complete)

Validation Checks:
  ✓ No SST violations
  ✓ No unresolved TODOs

Stakeholder Alignment:
  ? Have key stakeholders reviewed vision? (user input)
  ? Are constraints documented and accepted? (user input)

Status: [GO / ITERATE / NO-GO]
```

## Decision Options

At the end of each gate, present these options:

| Decision | Effect | Next Phase |
|----------|--------|-----------|
| **GO** | Approve phase completion, proceed | Next phase (e.g., Planning → Design) |
| **ITERATE** | Return to current phase, address feedback | Repeat current phase |
| **NO-GO** | Phase failed, major issues found | Reassess project or kill project |
| **DESCOPE** | Remove features/scope (Planning/Implementation gates only) | Reduce scope, re-validate |
| **REDESIGN** | Major redesign needed (Implementation Readiness only) | Return to Design phase |

## Output Format

Present the gate results to the user in an interactive session:

```
╔════════════════════════════════════════════════════════════════╗
║              DISCOVERY GATE VALIDATION REPORT                  ║
╚════════════════════════════════════════════════════════════════╝

Timestamp: 2026-03-14 10:30:00 UTC
Phase: Discovery
Scope: docs/ets/projects/{project-slug}/

━━━ DOCUMENT COMPLETENESS ━━━
✓ project-context.md: 100% (all sections filled)
✓ product-vision.md: 95% (1 section has [TODO])

━━━ VALIDATION CHECKS ━━━
✓ SST compliance: No violations
✓ No unresolved TODOs

━━━ RECOMMENDATION ━━━
Status: GO ✓
Reason: Vision and constraints are clear. Team alignment confirmed in standup.

━━━ DECISION REQUIRED ━━━
Ready to proceed to Planning Phase?

Options:
  1. GO — Approve phase, proceed to Planning
  2. ITERATE — Return to Discovery, address feedback
  3. NO-GO — Major issues, kill project

Enter decision (1/2/3) or explanation:
```

## Execution Steps

1. **Detect phase** (from argument or user input)
2. **Load gate checklist** (from checklists.md)
3. **Check document completeness** (list required files, check existence and % complete)
4. **Run validation checks** — Call check-sst and check-traceability
5. **Present results** (formatted table with checkmarks and counts)
6. **Make recommendation** (GO/ITERATE/NO-GO based on violations and completeness)
7. **Ask for decision** (interactive prompt for user choice)
8. **Record decision** (write to `state/reports/gate-log.md` for audit trail)
9. **Proceed or iterate** (based on user decision)

## Integration Points

- **Orchestrator** — Calls validate-gate after each phase completion
- **CI/CD** — May be run before deploying documentation changes
- **Slack notifications** — Optional: post gate results to #docs or #releases Slack channel

## Notes

- Gates are **go/no-go decisions** — either you pass or you iterate; no partial progress
- **Gates are cumulative** — Passing Discovery Gate doesn't invalidate later discoveries
- **Flexibility allowed** — Teams may descope features at Planning or Redesign at Implementation Readiness
- **Audit trail** — Every gate decision is logged in `state/reports/gate-log.md` for traceability

## Knowledge Pointers

- **Checklists**: `docs/ets/projects/{project-slug}/.guides/gate-checklists.md` — Detailed checklists for all 3 gates
- **SST Validation**: Call to check-sst skill (read-only validation)
- **Traceability Validation**: Call to check-traceability skill (read-only validation)
- **Handoff Protocol**: `docs/ets/projects/{project-slug}/state/reports/gate-log.md` — Append gate decision record

## INPUT VALIDATION

This skill requires a phase argument to validate:
- Valid phases: `discovery`, `planning`, `design`, `implementation`
- If no phase specified: read from `docs/ets/.memory/project-state.md` → `Current phase` (primary)
- If project-state.md not available: detect from `state/workflow-state.yaml` (secondary)
- If neither exists: ask user which phase to validate

## OUTPUT VALIDATION

The output is a gate recommendation. Validate:
- [ ] Document completeness table present (doc name, status, missing items)
- [ ] SST validation results included (from check-sst)
- [ ] Traceability results included (from check-traceability)
- [ ] Gate recommendation stated: GO / ITERATE / NO-GO / DESCOPE / REDESIGN
- [ ] Clear action items for ITERATE or NO-GO decisions

## WORKFLOW

### Step 1: Phase Detection
- **Input:** `$ARGUMENTS` → `docs/ets/.memory/project-state.md` → `state/workflow-state.yaml` (in this order)
- **Action:** Determine which phase and mode to validate. Read `project-state.md` for `Current phase` and `Current mode` — this is the most reliable source since it is auto-updated by hook on every document save.
- **Output:** Phase identifier + mode + expected documents list (from dependency-graph.yaml)

### Step 2: Document Inventory
- **Input:** Expected documents for this phase
- **Action:** Check each document exists, is COMPLETE (not DRAFT), passes OUTPUT VALIDATION
- **Output:** Document status table

### Step 3: Run Validation Skills
- **Input:** All documents for this phase
- **Action:** Invoke `check-sst` and `check-traceability` skills
- **Output:** SST violations + traceability gaps

### Step 4: Gate Recommendation
- **Input:** Document status + validation results
- **Action:** Apply gate criteria:
  - GO: All docs COMPLETE, zero SST violations, traceability ≥ 90%
  - ITERATE: Some docs DRAFT or minor violations
  - NO-GO: Critical docs missing or major SST violations
- **Output:** Recommendation with rationale

### Step 5: User Decision
- **Input:** Recommendation
- **Action:** Present results, ask user for GO/ITERATE/NO-GO decision
- **Output:** Gate decision → written to `state/reports/`

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| Phase not specified and no phase.json | Medium | Ask user which phase | Default to earliest incomplete phase |
| Expected documents all missing | High | Recommend: "Phase not started yet" | Suggest running the phase first |
| check-sst or check-traceability fails | Medium | Report partial results | Note which validation couldn't run |
| Output validation fails | High | Mark gate as ITERATE | Don't allow GO with incomplete validation |
