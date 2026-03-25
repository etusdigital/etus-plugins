---
name: tech-spec
description: >
  Use when defining technical specifications, non-functional requirements, or
  architecture decisions. Also triggers on 'tech spec', 'what are the NFRs',
  'architecture decisions', 'performance requirements', 'scalability', 'security
  requirements', or 'ADR'.
model: opus
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Upstream: docs/ets/projects/{project-slug}/architecture/architecture-diagram.md"
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — Needed for system structure to inform NFRs and ADRs.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/planning/prd.md` — Business requirements improve NFR target alignment.
- `docs/ets/projects/{project-slug}/discovery/project-context.md` — Constraints inform NFR targets.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `tech-spec.requires: [architecture-diagram]`
2. Check: does `architecture-diagram.md` exist, non-empty, not DRAFT?
3. If missing → auto-invoke `architecture-diagram` skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in Output Document Structure
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — suggest alternatives, challenge assumptions, and explore what-ifs instead of only extracting information.

1. **One question per message** — Never batch multiple questions. Ask one, wait for the answer, then ask the next. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction, present 3-4 concrete options with a brief description of each. Highlight your recommendation.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs and a recommendation.

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section, ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before next phase** — Blocks the handoff.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing tech-spec.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed** — If the user's input is already detailed with clear requirements, specific acceptance criteria, and defined scope, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

## MEMORY PROTOCOL

This skill reads and writes persistent memory to maintain context across sessions.

**On start (before any interaction):**
1. Read `docs/ets/.memory/project-state.md` — know where the project is
2. Read `docs/ets/.memory/decisions.md` — don't re-question closed decisions
3. Read `docs/ets/.memory/preferences.md` — apply user/team preferences silently
4. Read `docs/ets/.memory/patterns.md` — apply discovered patterns
5. If any memory file doesn't exist, create it with the default template

**On finish (after saving artifact, before CLOSING SUMMARY):**
1. `project-state.md` is updated **automatically** by the PostToolUse hook — do NOT edit it manually.
2. If the user chose between approaches during this skill → run via Bash:
   `python3 .claude/hooks/memory-write.py decision "<decision>" "<rationale>" "<this-skill-name>" "<phase>" "<tag1,tag2>"`
3. If the user expressed a preference → run via Bash:
   `python3 .claude/hooks/memory-write.py preference "<preference>" "<this-skill-name>" "<category>"`
4. If a recurring pattern was identified → run via Bash:
   `python3 .claude/hooks/memory-write.py pattern "<pattern>" "<this-skill-name>" "<applies_to>"`

**The `.memory/*.md` files are read-only views** generated automatically from `memory.db`. Never edit them directly.

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- New system with undefined NFR targets and no prior ADRs
- System must meet compliance requirements (SOC2, GDPR, PCI-DSS)
- Multiple technology choices need formal justification

**Use short version when:**
- Adding NFRs for a single new feature or service
- Updating existing ADRs after a technology change
- Even in short version, still include: at least 3 NFR-# with quantified targets and at least 1 ADR-# for the primary decision

### Skill-Specific Interaction Patterns

- **NFR targets — tiered proposals:** For each NFR category (performance, scalability, availability, security, etc.), propose 3 tiers: minimum viable, recommended, and stretch. Ask the user to pick the tier for that category before moving on.
- **ADR decisions — alternatives first:** For each Architecture Decision Record, present 2-3 alternatives with tradeoffs and a recommendation. Let the user choose the decision before documenting consequences.
- **One NFR/ADR at a time:** Present each NFR or ADR individually for approval. Don't batch all NFRs or all ADRs into a single output.
- **Handoff options:** At completion, present:
  1. **Proceed to Design (parallel agents)** (Recommended) — Start data, UX, and API design in parallel
  2. **Refine tech spec** — Adjust NFR targets or ADR decisions
  3. **Add more NFRs/ADRs** — Expand coverage for additional categories or decisions
  4. **Pause** — Save progress and return later

# Tech Spec Skill

## Purpose

This skill generates `docs/ets/projects/{project-slug}/architecture/tech-spec.md`, the authoritative specification of all non-functional requirements (NFR-#) and architecture decisions (ADR-#). It is the **Single Source of Truth** for:

- **Non-Functional Requirements** — Quantified targets (not "fast" but "< 200ms p95", not "secure" but "TLS 1.3, AES-256")
- **Architecture Decision Records** — Context, decision, consequences for each major technical choice
- **Technical Design** — How the system achieves the NFRs (trade-offs, constraints, rationale)

This document bridges architecture (Context, Container diagrams from architecture-diagram.md) and implementation (code, tests, deployment).

## Context Loading (4-Level Fallback)

1. **From upstream path** (argument-hint): If user provides path, read that file first (typically architecture-diagram.md)
2. **From prd.md** (docs/ets/projects/{project-slug}/prd.md): Business requirements, success metrics, SLOs
3. **From project-context.md** (docs/ets/projects/{project-slug}/project-context.md): System scale (users, events/sec, data volume)
4. **Ask user** (if nothing found): "What are the top 5 constraints for this system? (e.g., cost, latency, uptime, compliance)"

## NFR Quantification

Each NFR-# must have a **measurable target**, not subjective language.

### NFR Categories

| Category | Examples | Format |
|----------|----------|--------|
| **Performance** | Latency, throughput, resource usage | `< 200ms p95`, `> 1M events/sec`, `< 2GB RAM/instance` |
| **Scalability** | Concurrent users, data growth, regional expansion | `10M users`, `100GB/day`, `5 regions by Q3 2026` |
| **Availability** | Uptime, failover time, MTTR | `99.95% uptime`, `< 5min failover` |
| **Security** | Encryption, authentication, compliance | `TLS 1.3`, `HMAC-SHA256`, `SOC2 Type II` |
| **Reliability** | Error rates, recovery, deduplication | `< 0.1% error rate`, `< 1min recovery`, `2-layer dedup` |
| **Data Quality** | Freshness, completeness, accuracy | `< 5min lag (p95)`, `100% page-level`, `< 0.5% missing IPs` |
| **Operational** | Deployability, observability, runbooks | `1-click deploy`, `< 2sec metric lag`, `runbooks for 10 scenarios` |

### NFR Template

```
NFR-00X: [Category] [Constraint]

**Measurement:** [Metric and unit]

**Target:** [Quantified value]

**Rationale:** [Why this target? Business or technical reason?]

**Verification:** [How do we measure/test?]

**Owned by:** [Team/service name]
```

Example:

```
NFR-001: Performance — Event Ingestion Latency

**Measurement:** Time from Event Tracker receives request to HTTP response sent

**Target:** < 100ms p95, < 500ms p99

**Rationale:** Browser SDK times out after 30s; p95 < 100ms ensures < 3% timeouts. Batch microblocker delays ~50ms.

**Verification:** Prometheus `event_tracker_request_duration_seconds` histogram, daily SLO report

**Owned by:** Infra Team (Event Tracker service)
```

## ADR Format (Architecture Decision Records)

Each ADR-# documents a significant technical decision and its consequences.

### ADR Template

```
ADR-00X: [Title]

**Status:** Accepted | Proposed | Deprecated

**Context:**
[What is the issue we're facing? What are the constraints?]

**Decision:**
[What did we decide to do and why?]

**Consequences:**
[What are the positive and negative outcomes?]

**Alternatives Considered:**
[What else did we consider? Why not chosen?]

**Related:**
- ADR-YYY (if applicable)
- Feature Spec: [FS-name-001]
```

Example:

```
ADR-001: Redpanda over Kafka for Event Streaming

**Status:** Accepted

**Context:**
Need event streaming for pipeline with:
- 1M events/sec throughput
- Multi-region deployment (future)
- Operational simplicity (small team, limited Kubernetes expertise)
- Latency-critical: < 5sec end-to-end

**Decision:**
Use Redpanda (fully Kafka API compatible) instead of self-managed Kafka cluster.

**Consequences:**
- Positive: 70% fewer operational tasks (no ZK, no broker rebalancing), 40% lower memory footprint, same ecosystem tools
- Negative: Vendor lock-in (Redpanda over Kafka), no multi-region replication (yet), 2x cost vs. self-hosted

**Alternatives Considered:**
- Self-managed Kafka: Complexity, 24/7 ops required
- AWS MSK: No multi-region, vendor lock-in, higher latency
- RabbitMQ: Worse throughput, less suitable for event streaming patterns

**Related:**
- NFR-001 (Latency), NFR-003 (Throughput)
```

## Observability Requirements

For each feature or service boundary, define:

### Logs
| Event | Level | Structured Fields | When |
|-------|-------|-------------------|------|

### Metrics
| Metric Name | Type | Labels | Description |
|-------------|------|--------|-------------|

### Alerts
| Condition | Severity | Channel | Runbook |
|-----------|----------|---------|---------|

### Dashboards
Key views needed for operational monitoring.

**SST Rule:** Observability requirements are ONLY defined in tech-spec.md. Downstream documents (quality-checklist, implementation-plan, release-plan) validate against these requirements but do NOT redefine them.

## Single Source of Truth Rules

These rules exist to prevent conflicting definitions across documents — why it matters: gate approval depends on SST compliance. Only tech-spec.md should define:

1. **NFR-# definitions** — All non-functional requirements must be in this document
2. **ADR-# decisions** — All architecture decisions must be recorded here
3. **Observability requirements** — Logs, metrics, alerts, and dashboards are defined here
4. **No duplicates** — An NFR-# or ADR-# may not appear in other documents (may be referenced, not redefined)
5. **Quantification** — Every NFR must have a measurable target (never "good", "fast", "secure")
6. **Rationale** — Every NFR and ADR must explain the "why" (business/technical reason)
7. **Verification method** — Every NFR must specify how it is measured/tested

If another document (prd.md, ux-design.md, etc.) needs to reference an NFR, it uses `NFR-#` ID and links to tech-spec.md.

## Output Document Structure

The generated `docs/ets/projects/{project-slug}/architecture/tech-spec.md` must include:

1. **Executive Summary** (1 paragraph) — Key NFRs, critical decisions
2. **Non-Functional Requirements** (10-30 NFRs organized by category)
   - Performance, Scalability, Availability, Security, Reliability, Data Quality, Operational
   - Each with measurement, target, rationale, verification, ownership
3. **Architecture Decision Records** (10-30 ADRs organized by topic)
   - Technology choices, scalability approaches, security measures, data strategy
   - Each with status, context, decision, consequences, alternatives
4. **Constraints & Trade-offs** (summary table: constraint, chosen value, trade-off)
5. **Roadmap** (which NFRs are for MVP, which for scaling phases)
6. **Verification Strategy** (how we measure compliance with NFRs; SLO dashboards, tests, audits)

## Knowledge Pointers

- **Template**: `docs/ets/projects/{project-slug}/.templates/tech-spec.md` — Skeleton with NFR/ADR sections and examples
- **Guide**: `docs/ets/projects/{project-slug}/.guides/nfr-quantification.md` — How to write measurable NFRs (anti-patterns, examples)
- **Guide**: `docs/ets/projects/{project-slug}/.guides/adr-decision-making.md` — ADR best practices, when to write one, template
- **Reference**: `docs/ets/projects/{project-slug}/prd.md` — Business requirements that drive NFRs
- **Reference**: `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md` — System structure that tech-spec justifies

## Execution Steps

1. Load context (4-level fallback)
2. Identify NFR categories (performance, security, scalability, etc.)
3. For each category, extract constraints from context and ask user for priorities
4. Quantify each NFR with measurement and target (iterate if needed)
5. Identify major technical decisions (why Redpanda? why ClickHouse? why CF Workers?)
6. Document each decision as an ADR with context, decision, consequences
7. Map NFRs to ADRs (which ADR helps achieve which NFR)
8. Write artifact to `docs/ets/projects/{project-slug}/architecture/tech-spec.md`
9. Validate: Check that every NFR-# is unique, every ADR-# is unique, no duplicates in other docs
10. Report: "Generated tech-spec.md with N NFRs, M ADRs, mapped to architecture"

## Common NFR Patterns

| NFR | Typical Target | Tech Decision |
|-----|---|---|
| Ingestion latency | < 100ms p95 | Batch microblocker, local buffering |
| Throughput | > 1M events/sec | Redpanda partitioning, consumer scaling |
| Query latency | < 1sec | ClickHouse, pre-aggregated tables |
| Deduplication | 2-layer (batch + DB) | In-batch bloom filter + ReplacingMergeTree |
| Freshness | < 5min lag | Dual-write (realtime + archive) |
| Security | TLS 1.3, AES-256 | mTLS, encryption in-transit, at-rest |
| Uptime | 99.95% | Multi-AZ, circuit breakers, SLO dashboards |

## Notes

- NFRs are **business/stakeholder owned** — they define success
- ADRs are **team owned** — they document how we'll achieve NFRs
- Tech-spec.md is NOT a code review document — no implementation details, no pseudo-code
- This document is the **bridge between architecture and implementation** — implementation-plan.md references NFRs/ADRs, and optional execution projections may mirror them
- NFR/ADR IDs are immutable — once published, the ID stays (you can deprecate, not rename)

## INPUT VALIDATION

**architecture-diagram.md** (BLOCKS):
- Must contain: `## Container View` or `## C4 Container`
- Must list at least 2 containers/services
- Minimum length: 80 lines

**prd.md** (ENRICHES):
- Should contain PRD-F-# features with success criteria

**project-context.md** (ENRICHES):
- Should contain deployment context (cloud, regions, scale)

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] At least 5 NFR-# defined with quantified targets (not "fast" but "< 200ms p95")
- [ ] Each NFR-# has measurement method and verification approach
- [ ] At least 3 NFR categories covered (performance, security, reliability, scalability, data quality, operational)
- [ ] At least 2 ADR-# with context, options considered, decision, consequences
- [ ] NFR-# IDs are unique and sequential
- [ ] ADR-# IDs are unique and sequential
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ tech-spec.md saved to `docs/ets/projects/{project-slug}/architecture/tech-spec.md`

Status: [COMPLETE | DRAFT]
IDs generated: [list NFR-# and ADR-# IDs, e.g., NFR-001 through NFR-010, ADR-001 through ADR-005]

→ Next step: data/ux/api agents (parallel) — Start parallel Design sub-phases
  Run: /design or let the orchestrator continue
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `architecture-diagram.md` (BLOCKS), `prd.md` (ENRICHES), `project-context.md` (ENRICHES)
- **Action:** Extract system components, technology choices, business constraints
- **Output:** Internal context object

### Step 2: NFR Category Identification
- **Input:** Step 1 context
- **Action:** Propose the NFR categories relevant to this project (performance, scalability, availability, security, reliability, data quality, operational). Highlight which categories are most critical based on the architecture.
- **Approval:** Ask the user to confirm the category list before diving into specifics.

### Step 3: NFR Definition (one at a time)
- **Input:** Approved category list + `user-stories.md` (if available)
- **Action:** For each NFR category, propose 3 tiers (minimum viable, recommended, stretch) with concrete targets. Present one NFR at a time.
- **Approval:** Ask the user to pick the tier for each NFR before moving to the next. "Does this target feel right? Anything to adjust?"
- **Output:** NFR table with target values and measurement methods
- **Integration:** NFR-# IDs referenced by `implementation-plan` and `quality-checklist`

### Step 4: ADR Drafting (one at a time)
- **Input:** Step 1 context + technology constraints
- **Action:** For each major technical decision, present 2-3 alternatives with tradeoffs and a recommendation. Let the user choose before documenting consequences.
- **Approval:** Present one ADR at a time. Wait for the user's choice before moving to the next.
- **Output:** ADR entries
- **Integration:** ADR-# IDs referenced by `architecture-diagram` (bidirectional)

### Step 5: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 6: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 7: Save Artifact

- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/architecture/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/architecture/tech-spec.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/architecture/tech-spec.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/architecture/architecture-diagram.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 9: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/architecture/tech-spec.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 10: Validation & Handoff
- **Input:** Steps 3-4 outputs
- **Action:** Run OUTPUT VALIDATION checklist. Display CLOSING SUMMARY.
- **Handoff:** Present the 4 next-step options from the Interaction Protocol. Let the user choose.
- **Output:** Document marked COMPLETE or DRAFT

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (architecture-diagram.md) | Critical | Auto-invoke architecture-diagram skill | Block execution |
| Architecture diagram is too sparse (<2 containers) | Medium | Warn user, proceed with limited NFRs | Mark tech-spec as DRAFT |
| Can't quantify an NFR target | Medium | Ask user for target, suggest industry defaults | Use TBD with TODO marker |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
| Conflicting NFR-# or ADR-# IDs | Medium | Renumber from max+1 | Append suffix |

## QUALITY LOOP

This skill supports iterative quality improvement when invoked by the orchestrator or user.

### Cycle

1. **Generate** — Produce initial document following WORKFLOW steps
2. **Self-Evaluate** — Score the output against OUTPUT VALIDATION checklist
   - Calculate: completeness % = (passing checks / total checks) × 100
   - If completeness ≥ 90% → mark COMPLETE, exit loop
   - If completeness < 90% → proceed to step 3
3. **Identify Issues** — List each failing check with specific gap description
4. **Improve** — Address each issue, regenerate affected sections only
5. **Re-Evaluate** — Score again against OUTPUT VALIDATION
   - If improved by < 5% from previous iteration → diminishing returns, mark DRAFT with notes
   - If completeness ≥ 90% → mark COMPLETE, exit loop
   - If max iterations (3) reached → mark DRAFT with iteration log
6. **Report** — Log to stdout: iteration count, score progression (e.g., 65% → 82% → 91%), remaining gaps if any

### Termination Conditions

| Condition | Action | Document Status |
|-----------|--------|-----------------|
| Completeness ≥ 90% | Exit loop | COMPLETE |
| Improvement < 5% between iterations | Exit loop (diminishing returns) | DRAFT + notes |
| Max 3 iterations reached | Exit loop | DRAFT + iteration log |

### Invocation

- **Automatic:** Orchestrator invokes Quality Loop for all high-dependency documents
- **Manual:** User can request `--quality-loop` on any skill invocation
- **Skip:** User can pass `--no-quality-loop` to disable (generates once, validates once)

### 3-Solution Critique

When the self-evaluation identifies a weakness (score < 7/10 on any criterion):

1. **Generate 3 distinct solutions** — each must use a fundamentally different approach (not variations of the same idea)
2. **Compare efficiency** — for each solution, rate:
   - Effort to implement (Low/Medium/High)
   - Impact on document quality (Low/Medium/High)
   - Risk of introducing new issues (Low/Medium/High)
3. **Select and apply** — choose the solution with the best effort-to-impact ratio and lowest risk
4. **Document the decision** — add a brief note in the output explaining which solution was chosen and why

Example: If "NFR targets not quantified (using subjective language)" is identified:
- **Solution A:** Replace subjective terms with SLI metrics in existing NFRs → Effort: Low, Impact: Medium, Risk: Low
- **Solution B:** Add verification methods section with measurement tooling per NFR → Effort: Medium, Impact: High, Risk: Low
- **Solution C:** Restructure as capability roadmap (MVP NFRs vs. scaling phase NFRs) with acceptance thresholds → Effort: High, Impact: High, Risk: Medium
- **Selected:** Solution B — high impact with moderate effort, directly addresses measurement gaps and provides clear verification paths

