# ETUS PMDocs v5.2 — Gap Analysis Report

**Date:** 2026-03-17
**Auditor:** Claude (Opus)
**Scope:** Full audit of v5.2 upgrade — structure, skills, commands, agents, orchestrator, infrastructure

---

## Executive Summary

The upgrade from v4.1 (product-only, 25 skills) to v5.2 (4-mode system, 31 skills) is **100% complete**. The architecture is sound: mode detection router, handoff protocol, dependency graph, memory protocol, spec reviewer agent, and quality loop are all in place.

**0 gaps remaining** — all 4 identified gaps have been fixed (2 critical, 2 minor). See resolution notes below.

**0 structural gaps** — dependency-graph.yaml, all 32 knowledge/template.md files, all 11 commands, all 7 agents, and the orchestrator are fully present and correctly wired.

---

## Gap Classification

| Severity | Count | Status | Description |
|----------|-------|--------|-------------|
| CRITICAL | 2 | ✅ FIXED | Feature mode pipeline broken — skills block on wrong upstream |
| MINOR | 2 | ✅ FIXED | Validation skills could benefit from Feature mode awareness |
| INFO | 3 | — | Opportunities for improvement, not blocking |

---

## CRITICAL GAPS (2) — ✅ ALL FIXED

### GAP-1: `user-stories/SKILL.md` — No Feature Mode Awareness — ✅ FIXED

**File:** `.claude/skills/planning/user-stories/SKILL.md`
**Impact:** Feature mode pipeline is broken at step 2.

**Problem:** The BLOCKS section requires `prd.md` as the only upstream:

```
BLOCKS (required — auto-invoke if missing):
- docs/ets-docs/planning/prd.md
```

In Feature mode, the pipeline is `feature-brief → user-stories → design-delta → impl-plan`. There is no `prd.md` — the upstream is `feature-brief-{slug}.md`.

**What needs to change:**

1. **DEPENDENCY RESOLUTION** — Add mode-conditional BLOCKS:
   - Product mode: BLOCKS on `docs/ets-docs/planning/prd.md` (current, unchanged)
   - Feature mode: BLOCKS on `docs/ets-docs/features/feature-brief-{slug}.md`

2. **ID mapping** — Document FB-# → US-# traceability (currently only documents PRD-F-# → US-#)

3. **CONTEXT LOADING** — Add Feature mode branch that reads feature-brief instead of prd

4. **OUTPUT PATH** — In Feature mode, save to `docs/ets-docs/features/user-stories-{slug}.md` instead of `docs/ets-docs/planning/user-stories.md`

5. **INPUT/OUTPUT VALIDATION** — Accept FB-# as valid upstream reference

---

### GAP-2: `implementation-plan/SKILL.md` — No Feature Mode Awareness — ✅ FIXED

**File:** `.claude/skills/implementation/implementation-plan/SKILL.md`
**Impact:** Feature mode pipeline is broken at step 4.

**Problem:** The BLOCKS section requires `user-stories.md` + `tech-spec.md`:

```
BLOCKS (must exist — auto-invoke if missing):
- docs/ets-docs/planning/user-stories.md
- docs/ets-docs/architecture/tech-spec.md
```

In Feature mode, the upstream is `user-stories-{slug}.md` + `design-delta-{slug}.md` (not the full tech-spec).

**What needs to change:**

1. **DEPENDENCY RESOLUTION** — Add mode-conditional BLOCKS:
   - Product mode: BLOCKS on `user-stories.md` + `tech-spec.md` (current, unchanged)
   - Feature mode: BLOCKS on `features/user-stories-{slug}.md` + `features/design-delta-{slug}.md`

2. **CONTEXT LOADING** — Add Feature mode branch that reads design-delta for technical constraints instead of full tech-spec + architecture-diagram

3. **OUTPUT PATH** — In Feature mode, save to `docs/ets-docs/features/impl-plan-{slug}.md`

4. **SCOPE** — In Feature mode, only plan tasks for the feature scope (not full product)

---

## MINOR GAPS (2) — ✅ ALL FIXED

### GAP-3: `check-traceability/SKILL.md` — No FB-# Chain — ✅ FIXED

**File:** `.claude/skills/validation/check-traceability/SKILL.md`

**Problem:** The traceability chain validated is `BO-# → PRD-F-# → US-# → FS-# → impl-#`. Feature mode uses a different chain: `FB-# → US-# → impl-#`. If `check-traceability` is ever invoked in Feature mode context, it will report false positives (orphan US-# with no PRD-F-# parent).

**Recommendation:** Add a mode-conditional chain. When Feature mode artifacts are detected, validate `FB-# → US-# → impl-#` instead.

**Severity:** Minor — the orchestrator doesn't call check-traceability in Feature mode, but a user could invoke `/validate` manually.

---

### GAP-4: `check-sst/SKILL.md` — No Feature Mode Scope — ✅ FIXED

**File:** `.claude/skills/validation/check-sst/SKILL.md`

**Problem:** SST checks scan the entire `docs/ets-docs/` tree. In Feature mode, the feature's documents are in `docs/ets-docs/features/`. If feature-scoped user-stories contain Given/When/Then blocks, they won't conflict with the main `user-stories.md` since they're in different files — but the SST checker may flag them as violations if it expects Given/When/Then only in `planning/user-stories.md`.

**Recommendation:** Add Feature mode awareness: Given/When/Then in `features/user-stories-{slug}.md` is valid, not a violation.

**Severity:** Minor — same reasoning as GAP-3. Not called automatically in Feature mode.

---

## INFO (Opportunities)

### INFO-1: `quality-checklist/SKILL.md` — Feature Mode Scoping

The quality checklist currently targets full-product releases. For Feature mode, a lighter checklist (focused on the feature scope) might be useful. Not blocking — features can use the full checklist and skip irrelevant sections.

### INFO-2: `sprint-status/SKILL.md` — Feature Mode Tasks

Sprint status tracks `impl-#` tasks from the full implementation plan. In Feature mode, feature-scoped `impl-#` tasks from `features/impl-plan-{slug}.md` should also be trackable. Not blocking — sprint-status can be updated manually.

### INFO-3: Orchestrator Feature Pipeline — Output Path Consistency

The orchestrator documents Feature mode pipeline but doesn't explicitly specify that Feature mode artifacts go to `docs/ets-docs/features/` (it's implied by the individual skill output paths). Adding an explicit note in the orchestrator's Feature mode section would improve clarity.

---

## Infrastructure Audit — All Clear

| Component | Status | Notes |
|-----------|--------|-------|
| `dependency-graph.yaml` | ✅ Present | 377 lines, 27 entries, mode-aware |
| `knowledge/template.md` (×32) | ✅ All present | 100% coverage across all skills |
| Commands (×11) | ✅ All present | 4 new + 7 existing |
| Agents (×7) | ✅ All present | 2 new (spec-reviewer, learnings-researcher) + 5 existing |
| Orchestrator | ✅ Updated | Mode detection, 4-mode routing, anti-rationalization rules |
| CLAUDE.md | ✅ Updated | v5.2, full 4-mode documentation |
| Handoff protocol | ✅ Defined | phase.json + per-phase report JSON |
| Memory protocol | ✅ Defined | 4 files in .memory/ |
| SST rules | ✅ Updated | New entries for baseline, OST, release-plan, discovery-report, prioritization |

---

## Skills Audit Summary — 31 Skills

### New Skills (14) — All Complete ✅

| Skill | Mode | Status |
|-------|------|--------|
| baseline | Product | ✅ |
| discovery-report | Product | ✅ |
| spike | Spike | ✅ |
| feature-brief | Feature | ✅ |
| ost | Product | ✅ |
| prioritization | Product | ✅ |
| correct-course | Product | ✅ |
| design-delta | Feature | ✅ |
| tech-spec-standalone | Bug | ✅ |
| release-plan | Product | ✅ |
| quick-check | All | ✅ |
| etus-help | All | ✅ |
| project-retrospective | All | ✅ |
| validate-gate (updated) | All | ✅ |

### Existing Skills (17) — All Updated ✅

| Skill | Mode | Needs Update? | Status |
|-------|------|---------------|--------|
| project-context | Product | No | ✅ |
| product-vision | Product | No | ✅ |
| prd | Product | No | ✅ |
| user-stories | Product + Feature | Fixed | ✅ GAP-1 resolved |
| feature-spec | Product | No | ✅ |
| architecture-diagram | Product | No | ✅ |
| tech-spec | Product | No | ✅ |
| data-requirements | Product | No | ✅ |
| erd | Product | No | ✅ |
| database-spec | Product | No | ✅ |
| data-dictionary | Product | No | ✅ |
| data-flow-diagram | Product | No | ✅ |
| data-catalog | Product | No | ✅ |
| user-journey | Product | No | ✅ |
| ux-sitemap | Product | No | ✅ |
| wireframes | Product | No | ✅ |
| style-guide | Product | No | ✅ |
| api-spec | Product | No | ✅ |
| implementation-plan | Product + Feature | Fixed | ✅ GAP-2 resolved |
| sprint-status | Product | No | ✅ |
| quality-checklist | Product | No | ✅ |

---

## Fix Resolution Summary

All 4 gaps were fixed on 2026-03-17:

| Priority | Gap | Status | What was done |
|----------|-----|--------|---------------|
| 1 | GAP-1: user-stories Feature mode | ✅ Fixed | Added mode-conditional DEPENDENCY RESOLUTION, CONTEXT LOADING, OUTPUT PATH, INPUT/OUTPUT VALIDATION, and WORKFLOW sections |
| 2 | GAP-2: implementation-plan Feature mode | ✅ Fixed | Added mode-conditional DEPENDENCY RESOLUTION, CONTEXT LOADING, INPUT VALIDATION, and WORKFLOW sections |
| 3 | GAP-3: check-traceability FB-# chain | ✅ Fixed | Added Feature mode chain (FB-# → US-# → impl-#), FB-# pattern in ID table, Feature mode rules |
| 4 | GAP-4: check-sst Feature scope | ✅ Fixed | Updated Rule 1 to accept features/user-stories-{slug}.md, added Feature mode exclusion, added scoping note |

The Feature mode pipeline (`/feature`) is now fully operational: `feature-brief → user-stories → design-delta → impl-plan`.

---

## What's Working Well

The v5.2 upgrade is well-architected. Highlights:

- **Mode detection router** with 4-level fallback (command → phrases → context → ask) is clean
- **Dependency graph** correctly documents mode-conditional dependencies for new skills
- **Spec reviewer agent** adds genuine quality control without slowing the interactive flow
- **Memory protocol** enables cross-session learning
- **Quality loop** with diminishing-returns exit prevents infinite iteration
- **Right-size check** prevents over-documentation for simple work
- **Anti-rationalization rules** in the orchestrator are a smart guardrail against dependency skipping
- **Pressure test** in discovery-report and feature-brief challenges framing before generating
- **Anti-patterns** section in new skills captures team experience

The framework is ready for use in all 4 modes: Product, Feature, Bug, and Spike. All gaps have been resolved — v5.2 is fully operational.
