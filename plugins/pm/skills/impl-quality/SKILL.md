---
name: impl-quality
description: >
  Use when preparing for release, checking quality readiness, or defining QA
  criteria. Also triggers on 'quality checklist', 'are we ready to ship',
  'release criteria', 'QA requirements', or 'pre-launch validation'.
model: sonnet
version: 1.0.0
argument-hint: "[upstream-path]"
compatibility: "Optional: external execution adapter integration (for example, a Linear adapter). If an execution adapter is active, read `state/project-status.yaml`, `state/execution-sync.yaml`, and `state/execution-status.yaml` for the current operational picture."
---

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/planning/user-stories.md` — Needed for acceptance criteria to verify.
- `docs/ets/projects/{project-slug}/architecture/tech-spec.md` — Needed for NFR-# targets to measure against.

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` — Task coverage improves checklist completeness.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `quality-checklist.requires: [user-stories, tech-spec]`
2. Check both required docs exist, non-empty, not DRAFT
3. If missing → auto-invoke upstream skill → wait → continue
4. Check ENRICHES → warn if missing, proceed

## WHEN TO USE / DEPTH GUIDE

**Use full version when:**
- Pre-launch validation for a new product or major release
- Compliance-critical release requiring audit trail
- Release with NFR-# targets that need formal verification

**Use short version when:**
- Minor release or hotfix with limited scope
- Feature flag rollout with easy rollback
- Even in short version, still include: acceptance criteria verification, NFR-# check, and rollback plan

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
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

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing quality-checklist.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

### Skill-Specific Interaction

- **Coverage targets:** Propose 3 tiers for test coverage and ask which tier to target:
  - *Minimum (70%)* — covers critical paths, acceptable for MVP
  - *Recommended (80%)* — good balance of confidence and effort (Recommended)
  - *Stretch (90%)* — high confidence, significant test investment, appropriate for regulated products
- **Security requirements:** Propose security checks based on the tech-spec NFRs and architecture. Present each category (auth, input validation, encryption, API security, dependency scanning) and ask "Which of these apply to this product?" before generating the checklist.
- **Accessibility level:** Propose WCAG compliance level with tradeoffs and effort:
  - *Level A* — minimum baseline, catches critical barriers, low effort
  - *Level AA* — industry standard, good coverage, moderate effort (Recommended)
  - *Level AAA* — gold standard, maximum inclusivity, high effort
  Ask which level to target.
- **Performance benchmarks:** Propose benchmarks based on NFR-# targets from tech-spec. For each metric (response time, throughput, error rate), ask the user to calibrate — "Is this target realistic for your infrastructure?"
- **Handoff options:**
  1. Workflow complete! (Recommended) — ideation + planning artifacts generated, review and iterate as needed
  2. Refine checklist — adjust criteria or add custom checks
  3. Adjust targets — recalibrate coverage, performance, or accessibility levels
  4. Pause — save current progress and return later

# Quality Assurance Checklist Generation

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

## PURPOSE

Generate a comprehensive **quality-checklist.md** that defines all pre-release quality criteria and acceptance gates. This document maps Non-Functional Requirements (NFRs) from the architecture phase to specific test cases, performance benchmarks, security reviews, and acceptance criteria. It provides the definitive checklist for release readiness.

The quality checklist is the final validation step before launch, ensuring that product quality standards are met and risks are identified before users are impacted.

## CRITICAL SST RULE

**Quality criteria, test requirements, and acceptance gates are ONLY documented here.** User story acceptance criteria are defined in user-stories.md; NFR targets are defined in tech-spec.md. This document maps those requirements to specific test and validation procedures.

## CONTEXT LOADING (4-level fallback)

1. **$ARGUMENTS**: If `[upstream-path]` provided, load that document
2. **Handoff**: Check for `docs/ets/projects/{project-slug}/planning/user-stories.md` (acceptance criteria per US-#)
3. **Scan**: If not found, check `docs/ets/projects/{project-slug}/architecture/tech-spec.md` (NFRs) and `docs/ets/projects/{project-slug}/implementation/implementation-plan.md` (DoD)
4. **Ask**: If no context available, ask user for release type (MVP, beta, GA) and critical paths

Load the following sections from upstream:
- Acceptance criteria from user stories (per US-#)
- Non-functional requirements from tech-spec (NFR-#: performance, security, reliability, scalability)
- Definition of Done from implementation plan
- Any identified risks or compliance requirements

## PROCESS

1. **Release Type & Scope Definition**:
   - MVP: Core feature validation, basic security
   - Beta: Feature-complete, performance benchmarks met
   - GA: Full QA coverage, production hardened
   - Custom: User-defined release criteria

2. **Functional Testing**:
   - For each user story (US-#), list acceptance criteria
   - Define test case for each criterion
   - Specify test type (manual, automated, UAT)
   - Reference related impl-# tasks

3. **Performance Testing**:
   - Extract performance targets from tech-spec.md (NFR-#)
   - Define performance test scenarios:
     - Load testing (concurrent users)
     - Stress testing (peak load)
     - Endurance testing (sustained load over time)
   - Document baseline metrics and acceptable ranges
   - Identify test tools and infrastructure

4. **Security Review**:
   - Extract security requirements from tech-spec.md
   - Define security test categories:
     - Authentication/authorization
     - Input validation (OWASP top 10)
     - Data encryption (at rest, in transit)
     - API security (rate limiting, CORS)
     - Third-party dependency scanning
   - Document security sign-off owner

5. **Accessibility Validation**:
   - WCAG 2.1 Level AA compliance
   - Keyboard navigation testing
   - Screen reader testing (ARIA)
   - Color contrast ratios
   - Automated accessibility scanning tools

6. **Database & Data Integrity**:
   - Schema validation (DDL correct)
   - Migration testing (data preservation)
   - Backup/restore procedures
   - Query performance (index validation)
   - Referential integrity checks

7. **Deployment Readiness**:
   - Configuration management (all environments)
   - Secrets management (API keys, database credentials)
   - Observability: validate that implementation covers all observability requirements defined in tech-spec. If tech-spec has no observability section, flag as gap, do NOT define requirements here.
   - Rollback procedures documented and tested
   - Deployment runbook created and reviewed

8. **Documentation & Support**:
   - User documentation (help, guides) complete
   - API documentation up-to-date
   - Deployment guide for ops team
   - Troubleshooting guide for support
   - Known issues documented

9. **User Acceptance Testing (UAT)**:
   - UAT plan documented (participants, scenarios)
   - UAT sign-off criteria
   - Feedback integration plan

## OUTPUT FORMAT

Document structure:
- **Executive Summary**: Release type, date, critical risks, sign-off status
- **Functional Testing**: By user story
  - Table: US-#, acceptance criterion, test case, status
  - Links to test results or automation framework
- **Performance Benchmarks**: NFR-linked testing
  - Target vs. measured for each metric
  - Load/stress test scenarios and results
  - Performance regression analysis
- **Security Review**:
  - Security requirements (NFR-#)
  - Test procedures per requirement
  - Vulnerability assessment results
  - OWASP compliance checklist
- **Accessibility Compliance**: WCAG 2.1 AA checklist
- **Data Integrity**: Database validation procedures and results
- **Deployment Readiness**: Infrastructure, monitoring, runbook
- **Documentation Review**: All artifacts present and current
- **UAT Plan & Sign-off**: Participants, scenarios, approval gate
- **Risk Assessment**: Outstanding risks and mitigation plans
- **Sign-off Matrix**: Roles and approval gates (QA, Ops, Product, Security)

## PIPELINE CONTEXT

- **Input**: user-stories.md (acceptance criteria), tech-spec.md (NFRs), implementation-plan.md (DoD)
- **Output**: quality-checklist.md
- **Feeds**: Release planning, go/no-go decision
- **Gate function**: Validates product is ready for launch

## KNOWLEDGE POINTER

Refer to `docs/ets/projects/{project-slug}/implementation/template-quality-checklist.md` for:
- Checklist template by release type (MVP, beta, GA)
- Performance benchmark examples
- OWASP security checklist
- WCAG 2.1 AA compliance checklist
- UAT plan template
- Sign-off email template

---

**Execution instruction**: Load context, extract acceptance criteria from stories, map NFRs to performance tests, define security and accessibility validation, establish deployment readiness checks, plan UAT, identify risks, create sign-off matrix, and output quality-checklist.md to docs/ets/projects/{project-slug}/implementation/.

## INPUT VALIDATION

**user-stories.md** (BLOCKS):
- Must contain US-# with Given/When/Then acceptance criteria

**tech-spec.md** (BLOCKS):
- Must contain NFR-# with quantified targets

**implementation-plan.md** (ENRICHES):
- Should contain impl-# task list

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Test coverage criteria defined for each Must Have US-#
- [ ] Performance benchmarks from NFR-# targets included
- [ ] Security review checklist present
- [ ] Accessibility criteria present (if UX-facing)
- [ ] Deployment readiness checklist present
- [ ] Acceptance criteria verification plan (Given/When/Then → test case mapping)
- [ ] Source Documents section present at top

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
✅ quality-checklist.md saved to `docs/ets/projects/{project-slug}/implementation/quality-checklist.md`

Status: [COMPLETE | DRAFT]
IDs generated: N/A (this document maps US-# and NFR-# to test criteria)

→ Next step: Workflow complete — ideation and planning artifacts generated
  The product documentation pipeline is finished. Review and iterate as needed.
```

Do NOT proceed to the next skill without displaying this summary first.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `user-stories.md`, `tech-spec.md` (BLOCKS), `implementation-plan.md` (ENRICHES)
- **Action:** Extract US-# acceptance criteria, NFR-# targets, impl-# tasks
- **Output:** Quality requirements bundle
- **Why this matters:** Quality criteria come from user expectations (stories) and technical constraints (NFRs). Loading both ensures the checklist covers functional and non-functional requirements.

### Step 2: Coverage Targets (Interactive)
- **Input:** Project context and release type
- **Action:** Propose 3 tiers for test coverage:
  - *Minimum (70%)* — covers critical paths, acceptable for MVP
  - *Recommended (80%)* — good balance of confidence and effort
  - *Stretch (90%)* — high confidence, appropriate for regulated products
  Ask which tier to target.
- **Output:** Selected coverage target
- **Why this matters:** The coverage target determines how much testing infrastructure to build. Setting expectations early avoids scope surprises.

### Step 3: Test Coverage Planning (Section-by-Section)
- **Input:** US-# acceptance criteria + coverage target
- **Action:** Map each Given/When/Then to test case categories. Present the test coverage matrix and ask "Does this test mapping look complete? Any gaps?"
- **Output:** Approved test coverage matrix

### Step 4: Security & Accessibility (Interactive)
- **Input:** NFR-# targets from tech-spec
- **Action:**
  1. Propose security checks based on tech-spec. Present each category (auth, input validation, encryption, API security, dependency scanning) and ask "Which of these apply?"
  2. Propose WCAG level (A, AA, AAA) with tradeoffs and effort. Ask which level to target.
- **Output:** Security and accessibility requirements

### Step 5: Performance Benchmarks (Interactive)
- **Input:** NFR-# performance targets
- **Action:** Propose benchmarks based on NFR-# targets. For each metric (response time, throughput, error rate), ask "Is this target realistic for your infrastructure?"
- **Output:** Calibrated performance benchmarks
- **Why this matters:** Unrealistic benchmarks lead to wasted effort or false confidence. User calibration ensures targets are both ambitious and achievable.

### Step 6: Deployment Readiness
- **Input:** All previous outputs
- **Action:** Create pre-release checklist covering configuration, secrets, monitoring, rollback, and documentation. Present and ask "Is this deployment checklist complete?"
- **Output:** Deployment readiness criteria

### Step 7: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If this is lightweight work and the document has unnecessary sections → trim empty or boilerplate sections
  - If this is complex work and sections are thin → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 8: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the NEXT skill in the pipeline still have to invent if this document is all they get?
  2. Do any sections depend on content claimed to be out of scope?
  3. Are there implicit decisions that should be explicit?
  4. Is there a low-effort addition that would make this significantly more useful for the next phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 9: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/implementation/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/implementation/quality-checklist.md` using the Write tool
  3. The document DOES NOT EXIST until it is written to the filesystem. Presenting content in chat is NOT saving.
- **Output:** File written to disk at the specified path

### Step 10: Spec Review

- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/implementation/quality-checklist.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/planning/user-stories.md`, `docs/ets/projects/{project-slug}/architecture/tech-spec.md`)
  2. The reviewer checks: completeness, consistency, clarity, traceability, SST compliance, scope, and YAGNI
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Why this matters:** A fresh reviewer catches problems the author misses — contradictions, implicit assumptions, and scope creep that are invisible when you wrote the document yourself.
- **Output:** Reviewed and approved document

### Step 11: User Review Gate

- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/implementation/quality-checklist.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Why this matters:** The user is the final authority on whether the document captures their intent correctly.
- **Output:** User-approved document

### Step 12: Validation & Handoff
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT
- **Handoff:** Present next step options:
  1. Workflow complete! (Recommended) — ideation + planning artifacts generated
  2. Refine checklist
  3. Adjust targets
  4. Pause

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing | Critical | Auto-invoke upstream skill | Block execution |
| No testable acceptance criteria in US-# | Medium | Flag untestable stories | Mark corresponding checks as TODO |
| NFR targets are TBD | Medium | Ask user for targets | Use industry defaults with note |
| Output validation fails | High | Mark as DRAFT | Proceed with DRAFT status |
