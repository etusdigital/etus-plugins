---
name: check-sst
description: >
  Use when checking document consistency, verifying SST compliance, or during gate
  validation. Also triggers when the orchestrator runs quality checks, or when asking
  'are there duplicate definitions', 'check SST rules', or 'validate document ownership'.
user-invocable: false
context: fork
agent: Explore
model: sonnet
version: 1.0.0
---

# Check SST Skill

## Purpose

This skill validates **Single Source of Truth** (SST) rules across the documentation corpus in `docs/ets/projects/{project-slug}/`. It scans documents for rule violations — duplicate definitions that should exist in only one authoritative location.

This is a **READ-ONLY validation skill**. It runs in a forked context (Explore agent) with no write access. It returns a report of violations for the orchestrator or user to remediate.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS:** None — this is a validation tool that scans existing documents.
**ENRICHES:** None.

This skill can run at any time. It scans all documents in `docs/ets/projects/{project-slug}/` and checks SST rules:
- ACT / JTBD / use-case matrices / edge-case registers / assumption registers → ONLY in opportunity-pack.md
- Solution options, four-risk matrices, and experiment definitions → ONLY in solution-discovery.md
- Given/When/Then → ONLY in user-stories.md (Product mode) or features/{feature-slug}/user-stories.md (Feature mode)
- NFR-# targets → ONLY in tech-spec.md
- ADR-# decisions → ONLY in tech-spec.md
- DDL (CREATE TABLE) → ONLY in database-spec.md
- dict.*/ev.* definitions → ONLY in data-dictionary.md
- tok.* design tokens → ONLY in style-guide.md
- API schemas → ONLY in api-spec.md
- Baseline metrics (current state / AS-IS) → ONLY in baseline.md
- Structured opportunities + candidate solutions (O-#, S-#.#) → ONLY in ost.md
- Rollout strategy + rollback plan + monitoring metrics → ONLY in release-plan.md
- Discovery evidence, method/sample, and insights by theme → ONLY in discovery-report.md
- ICE/RICE scores, P0/P1/P2 ranking, and trade-off decisions → ONLY in prioritization.md

## SST Rules (17 Enforced Patterns)

| Rule | Authority | Pattern | Example |
|------|-----------|---------|---------|
| 0 | **opportunity-pack.md** | `ACT-#` / `JTBD-#` / `UC-#` / `EDGE-#` / `ASM-#` (ideation coverage definitions) | `JTBD-1: Upload data in bulk without manual cleanup` |
| 1 | **solution-discovery.md** | `SOL-#` / `EXP-#` / four-risk matrix | `SOL-1: Guided onboarding; EXP-1: Prototype test` |
| 2 | **user-stories.md** or **features/{feature-slug}/user-stories.md** | `Given/When/Then` (BDD scenarios) | `Given I open the app, When I click "Buy", Then order created` |
| 2 | **tech-spec.md** | `NFR-#` (non-functional requirements) | `NFR-001: < 100ms p95 latency` |
| 3 | **tech-spec.md** | `ADR-#` (architecture decisions) | `ADR-005: Use Redpanda for streaming` |
| 4 | **database-spec.md** | `CREATE TABLE/INDEX/VIEW` (DDL) | `CREATE TABLE ets.events (...)` |
| 5 | **data-dictionary.md** | `dict.*` (field definitions) | `dict.user_id: UUID, identifies user` |
| 6 | **data-dictionary.md** | `ev.*` (event type definitions) | `ev.page_view: Page viewed by user` |
| 7 | **style-guide.md** | `tok.*` (design tokens) | `tok.color.primary: #007AFF` |
| 8 | **api-spec.md** | `/api/v1/*` (API endpoint specs) | `POST /api/v1/batch — ingest events` |
| 9 | **baseline.md** | Baseline metrics / current state (AS-IS) | `Current conversion rate: 12.3% (source: GA, confidence: high)` |
| 10 | **ost.md** | `O-#` / `S-#.#` (opportunities + candidate solutions) | `O-1: Low funnel completion; S-1.1: Simplify checkout` |
| 11 | **release-plan.md** | Rollout strategy + rollback plan + monitoring | `Rollout: canary 10% → 50% → 100%; Rollback trigger: error > 5%` |
| 12 | **discovery-report.md** | Discovery evidence, method/sample, insights by theme | `Tema 1 — Insight: 68% drop-off at step 3 (source: GA4, N=12 interviews)` |
| 13 | **prioritization.md** | ICE/RICE scores, P0/P1/P2 ranking, trade-offs | `O-1: ICE=8.3, P0; O-3: ICE=3.2, P2 — deferred due to dependency on O-1` |

## Scan Procedure

For each document in `docs/ets/projects/{project-slug}/`:

1. **Search for patterns** (regex/string matching):
   - `ACT-\d+:\|JTBD-\d+:\|UC-\d+:\|EDGE-\d+:\|ASM-\d+:` — Must only appear in opportunity-pack.md
   - `SOL-\d+:\|EXP-\d+:` — Must only appear in solution-discovery.md
   - `Given.*When.*Then` — Must only appear in user-stories.md (Product mode) or features/{feature-slug}/user-stories.md (Feature mode)
   - `NFR-\d{3}:` — Must only appear in tech-spec.md (may be referenced elsewhere)
   - `ADR-\d{3}:` — Must only appear in tech-spec.md (may be referenced elsewhere)
   - `CREATE TABLE\|CREATE INDEX\|CREATE VIEW` — Must only appear in database-spec.md
   - `dict\.[a-z_]+:` — Must only appear in data-dictionary.md
   - `ev\.[a-z_]+:` — Must only appear in data-dictionary.md
   - `tok\.[a-z_\.]+:` — Must only appear in style-guide.md
   - `POST\|GET\|PUT\|DELETE /api/v\d+/` — Must only appear in api-spec.md (endpoint definitions, not references)
   - `baseline.*:.*valor.*fonte\|AS-IS.*flow\|current.*metric` — Baseline metrics definitions must only appear in baseline.md (references allowed elsewhere)
   - `O-\d+:.*\|S-\d+\.\d+:` — Opportunity and solution candidate definitions must only appear in ost.md (references allowed elsewhere)
   - `rollout.*strategy\|rollback.*trigger\|rollback.*procedure\|ramp-up.*plan` — Rollout strategy and rollback definitions must only appear in release-plan.md (high-level rollout in prd.md is allowed as summary reference)
   - `metodo.*amostra\|fontes qualitativas\|fontes quantitativas\|insights.*tema\|H-\d+:.*Se.*entao` — Discovery evidence definitions, method/sample, and insights by theme must only appear in discovery-report.md (references to H-# allowed elsewhere)
   - `ICE.*=\|RICE.*=\|P0.*P1.*P2\|ranking.*final\|trade-off.*decisao\|score.*impacto.*confianca` — ICE/RICE score definitions, P0/P1/P2 ranking, and trade-off decisions must only appear in prioritization.md (references to priority level allowed elsewhere)

2. **For each violation found:**
   - Record filename and line number
   - Extract context (40 chars before/after match)
   - Note rule violated and authority document

3. **Exclusions** (do not flag as violations):
   - References to NFR-#, ADR-# (e.g., "As described in NFR-001")
   - Examples in comments (e.g., `// Example: Given a user logs in`)
   - Quoted text in guide documents (e.g., `.guides/nfr-quantification.md`)
   - **Feature mode scoped documents**: Given/When/Then in `features/{feature-slug}/user-stories.md` is valid (these are Feature mode user stories, not duplicates of `planning/user-stories.md`)

## Report Format

Return a structured violation report:

```
Single Source of Truth Validation Report
Generated: [timestamp]
Scan Scope: docs/ets/projects/{project-slug}/
Rules Checked: 13
Documents Scanned: [count]

=== VIOLATIONS SUMMARY ===
Total Violations: N
By Rule:
  Rule 0 (Ideation coverage): X violations
  Rule 1 (Given/When/Then): Y violations
  Rule 2 (NFR-#): Z violations
  [etc.]

=== VIOLATIONS DETAIL ===

Rule 1: Given/When/Then (Authority: user-stories.md)
  File: docs/ets/projects/{project-slug}/prd.md, Line 42
    Context: "...Given user clicks button, When event fires, Then..."
    Remediation: Move to user-stories.md as US-001

Rule 2: NFR-# (Authority: tech-spec.md)
  File: docs/ets/projects/{project-slug}/data-design/database-spec.md, Line 88
    Context: "...NFR-001 requires < 100ms latency..."
    Remediation: Reference as "NFR-001 (see tech-spec.md)" instead of redefining

=== SUMMARY ===
✓ Pass: All SST rules enforced
✗ Fail: N violations found (see remediation steps above)
```

## Execution Steps

1. **Discover documents** — List all .md files in `docs/ets/projects/{project-slug}/` (recursive)
2. **Scan each document** — For each SST pattern, search and extract matches
3. **Filter violations** — Exclude references and comments
4. **Build report** — Aggregate violations by rule and document
5. **Output** — Print report to stdout; return violation count
6. **Exit code** — 0 if no violations, 1 if violations found (useful for CI gates)

## Integration Points

- **Orchestrator** — Calls check-sst before Discovery Gate, Planning Gate, Implementation Readiness Gate
- **CI/CD** — May run on every commit or PR to enforce SST compliance
- **Document editors** — Receives warning if they introduce SST violations

## Common Violations & Remediation

| Violation | Root Cause | Remediation |
|-----------|-----------|-------------|
| NFR-# in prd.md | Business writer defined requirement | Remove from prd.md, add to tech-spec.md with measurement |
| Given/When/Then in feature-spec | Feature writer documented BDD | Move scenarios to user-stories.md as US-# |
| DDL in data-design overview | Designer sketched schema | Move DDL to database-spec.md, keep narrative in data-design |
| tok.* in component docs | Designer defined token inline | Add to style-guide.md, reference by ID in component |
| ADR-# duplicate | Team split on decision | Consolidate into single ADR-# (if same), or use different rule (e.g., narrative if not binding) |

## Notes

- **Referencing is allowed** — Other documents may reference `NFR-001`, `ADR-005`, etc. (not redefine)
- **Comments and examples are excluded** — Don't flag violations in markdown comments or guide documents
- **Case-insensitive** — Patterns match regardless of case (e.g., `nfr-001` and `NFR-001` both match)
- **No false positives** — If unsure, don't flag; let the orchestrator or user decide on remediation
- **Feature mode scoping** — Feature mode documents in `docs/ets/projects/{project-slug}/features/` are valid authority locations for their scoped content. Specifically, `features/{feature-slug}/user-stories.md` is a valid authority for Given/When/Then (same as `planning/user-stories.md` for Product mode). These are not duplicates — they serve different scopes.

## Knowledge Pointers

- **SST Documentation**: `docs/ets/projects/{project-slug}/.guides/single-source-of-truth.md` — Full SST specification, audit process
- **Reference**: `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Example tech-spec with NFR-# and ADR-# definitions

## INPUT VALIDATION

No input validation required — this skill scans all existing documents in `docs/ets/projects/{project-slug}/`.
If no documents exist, report: "No documents found to validate."

## OUTPUT VALIDATION

The output of this skill is a violation report, not a document. Validate:
- [ ] Report lists all files scanned
- [ ] Each violation includes: rule violated, file, line number, content excerpt
- [ ] Summary count of violations per rule
- [ ] Recommendation for each violation (which file should own the content)

## WORKFLOW

### Step 1: Document Discovery
- **Input:** `docs/ets/projects/{project-slug}/` directory
- **Action:** Recursively list all .md files
- **Output:** File list to scan

### Step 2: Pattern Scanning
- **Input:** File list
- **Action:** For each SST rule, scan all files for violations (e.g., Given/When/Then outside user-stories.md)
- **Output:** Violation list with file, line, content

### Step 3: Report Generation
- **Input:** Violations
- **Action:** Format into structured report with summary and recommendations
- **Output:** Violation report (stdout or markdown)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| No documents found in docs/ets/projects/{project-slug}/ | Info | Report "No documents to validate" | Exit cleanly |
| File read error | Low | Skip file, note in report | Continue with remaining files |
| Ambiguous SST match (e.g., code example in a doc) | Low | Flag as potential violation, note context | Let user review |
