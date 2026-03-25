# Dependency Enforcement Research: BMAD vs Superpowers vs Compound Engineering vs Neo v0 vs ETUS PMDocs

> Research date: 2026-03-14 (updated: 2026-03-14)
> Objective: Understand how leading frameworks enforce skill dependencies and auto-generate missing prerequisites
> Added: Deep analysis of Neo v0 (our own predecessor framework) — 280 files, 13 agents, 7 chains

---

## 1. BMAD Method (bmad-code-org/BMAD-METHOD)

### Architecture
- 8 agent-type skills (PM, Architect, Dev, QA, SM, Analyst, UX Designer, Quick Flow)
- 4 numbered phases: Analysis → Planning → Solutioning → Implementation
- Agents expose menus with workflow triggers (e.g., PM has "Create PRD", "Validate PRD", "Edit PRD")

### Dependency Enforcement: **Hard Gate at Workflow Init**

BMAD uses **blocking validation at the start of each workflow**. When the Architecture workflow initializes, it checks for the existence of the PRD document. If not found, it returns:

> "Architecture requires a PRD to work from. Please run the PRD workflow first or provide the PRD file path."

This is an **active blocker** — the workflow refuses to proceed, not just a warning.

### How It Chains
- Each agent exposes a **menu of workflows** (YAML-defined, e.g., `workflow-create-prd.md`)
- Workflows have multi-step `steps-c/` directories with ordered files (step-01, step-02, etc.)
- The **completion step** of each workflow suggests the next logical workflow
- Issue #1080 revealed a bug where the completion step incorrectly showed Architecture as equal to PRD — proving the system actively relies on this chaining

### Document-as-Contract Pattern
- Documents (Product Brief → PRD → Architecture → Stories) are persistent context
- Each downstream workflow reads the upstream document as its primary input
- The `bmad-skill-manifest.yaml` registers skills but doesn't declare dependencies — dependencies live inside each workflow's init step

### What They Don't Do
- No automatic generation of missing prerequisites — it blocks and tells you which command to run
- No dependency graph metadata — enforcement is procedural (inside workflow code), not declarative (in manifest)
- No concept of "optional" dependencies — all prerequisites are hard blockers

---

## 2. Superpowers (obra/superpowers)

### Architecture
- 14 composable skills (brainstorming, writing-plans, TDD, debugging, subagent-driven-development, etc.)
- Meta-skill: `using-superpowers` orchestrates all others
- Skills are **behavioral disciplines**, not document generators

### Dependency Enforcement: **Implicit Sequential Chain**

Superpowers uses a **narrative workflow chain** embedded in prose, not metadata:

1. `brainstorming` → produces a design spec → explicitly says "The ONLY skill you invoke after brainstorming is writing-plans"
2. `writing-plans` → produces a plan document → explicitly says "Use subagent-driven-development if available (required)"
3. `subagent-driven-development` → reads the plan → decision tree asks "Have implementation plan?" with "no" path → "Manual execution or brainstorm first"

### The Meta-Skill Pattern
The `using-superpowers` skill doesn't manage dependencies — it enforces **behavioral discipline**:
- Skill check comes BEFORE any action (even clarifying questions)
- Lists 12 "rationalization patterns" agents use to skip skills
- Process skills (brainstorming, debugging) run before implementation skills
- Rigid skills (TDD) follow exactly; flexible skills adapt

### What They Don't Do
- No file-existence checks — the plan document is assumed to exist
- No auto-generation — if prerequisite missing, skill text says "brainstorm first" but doesn't invoke it
- No dependency metadata — everything is prose in SKILL.md
- No warning/blocking mechanism — relies entirely on the AI reading and following instructions

---

## 3. Compound Engineering (EveryInc/compound-engineering-plugin)

### Architecture
- 26 specialized agents, 23 commands, 13 skills
- 4-step loop: Plan → Work → Assess → Compound
- Fully-qualified namespacing: `compound-engineering:<category>:<agent-name>`

### Dependency Enforcement: **Loop Compounding + Coverage Gates**

Compound Engineering takes a fundamentally different approach — it doesn't have a linear document pipeline. Instead:

1. `/ce:brainstorm` → explores requirements (produces specs)
2. `/ce:plan` → sub-agents research codebase in parallel → creates plan
3. `/ce:work` → implements from plan in worktrees
4. `/ce:review` → 14 specialized review agents run in parallel
5. `/ce:compound` → captures learnings into docs

### The "Compound" Pattern
- Each cycle feeds forward: brainstorms sharpen plans, plans inform future plans, reviews catch more issues, patterns get documented
- `.coverage-thresholds.json` acts as a **blocking gate** before PR creation
- Learnings are captured in version-controlled docs that become context for next cycle

### What They Don't Do
- No linear document dependency chain — it's a loop, not a pipeline
- No prerequisite file checks — assumes the workflow is followed in order
- No auto-generation of missing docs — humans drive the loop
- Dependencies are namespace-based (for agent resolution), not artifact-based

---

## 4. Neo v0 (Our Predecessor — `aa-etuslab/neo_v0`)

### Architecture
- 280 files across `prompts/` directory
- 13 agent personas (Neo, Morpheus, Product Owner, System Architect, Frontend Developer, Backend Developer, Database Developer, Test Engineer, UI Designer, UX Designer, UX Researcher, System Admin)
- 7 chains (Requirements, Architecture & Design, UI/UX, Backend Development, Code Quality, Testing, UI Conventions)
- 17 component categories under `chains/components/`
- 20 YAML config files under `neo_prompt/`
- Designed for Cline/Cursor as a monolithic mega-prompt (132KB YAML loaded into context)

### Dependency Enforcement: **4-Layer System**

Neo v0 had the most sophisticated dependency system of any framework analyzed — and it's ours.

#### Layer 1: Declarative `requires`/`generates` in `index.yaml`

The central index declares explicit dependency chains with typed relationships:

```yaml
# Documents declare what they need and what they produce
UXDD:
  requires: ["PRD"]
  generates: ["ux_design"]

SRS:
  requires: ["UXDD"]
  generates: ["software_requirements"]

TRD:
  requires: ["SRS"]
  generates: ["technical_requirements"]

DRD:
  requires: ["TRD"]
  generates: ["design_requirements"]
```

This creates a full dependency graph: `BRD → PRD → UXDD → SRS → TRD → DRD`. The same pattern applies to development (`project_setup → atomic_design_system → component_library`) and testing (`test_framework_setup → test_strategy`).

#### Layer 2: `chain-position` with `previous` in XML Prompts

Each prompt component declares its position in the chain and what came before:

```xml
<chain-position>
  <step>2</step>
  <name>implementation_analysis</name>
  <type>analysis</type>
  <previous>prompt_chain_orchestrator</previous>
</chain-position>
<input>
  <sources>
    <source>
      <type>requirements</type>
      <from>prompt_chain_orchestrator.output</from>
    </source>
  </sources>
</input>
```

This is a **data-flow contract** — the implementation_analysis step explicitly reads its input from `prompt_chain_orchestrator.output`.

#### Layer 3: Document Chain Orchestrator with Dependencies

The `prompt-chain-orchestrator.xml` defines document chains with explicit step-level dependencies:

```xml
<document-chains>
  <chain id="requirements">
    <step id="1">
      <template>BRD.md</template>
      <dependencies>
        <requires>feature_requirements.md</requires>
        <requires>market_analysis.md</requires>
      </dependencies>
    </step>
    <step id="2">
      <template>PRD.md</template>
      <dependencies>
        <requires>BRD.md</requires>
        <requires>technical_spec.md</requires>
      </dependencies>
    </step>
  </chain>
  <chain id="design">
    <step id="1">
      <template>DRD.md</template>
      <dependencies>
        <requires>PRD.md</requires>
        <requires>design_spec.md</requires>
      </dependencies>
    </step>
  </chain>
</document-chains>
```

The output schema includes `blockingIssues` and `nextAction`, implying active dependency enforcement.

#### Layer 4: Input Validation Schemas in Prompt Chains

Each prompt_chain XML (BRD, PRD) has `input_validation` with `required_fields` and `output_validation` with `metrics` and `pass_fail` conditions:

```xml
<input_validation>
  <required_fields>
    <field name="product_vision" type="object">
      <validation>
        <min_length>50</min_length>
        <required_sections>
          <section>overview</section>
          <section>target_users</section>
        </required_sections>
      </validation>
    </field>
  </required_fields>
</input_validation>

<output_validation>
  <metrics>
    <metric name="feature_coverage" type="percentage">
      <threshold>100</threshold>
    </metric>
    <metric name="pass_fail" type="boolean">
      <conditions>
        <condition>All features specified</condition>
        <condition>Technical validation complete</condition>
      </conditions>
    </metric>
  </metrics>
</output_validation>
```

#### Layer 5: Chain Validation + Integration Points

Every chain has a validation section and explicit integration points:

```
Chain Dependencies (from index.md):
- Requirements Chain → used by ALL other chains
- Architecture Chain → input: Project requirements → used by: UI/UX, Backend, Code Quality
- UI/UX Chain → input: Requirements + Architecture
- Code Quality Chain → input: ALL previous chain outputs
- Testing Chain → input: Code + Requirements
- Backend Chain → input: Architecture + API specs
```

### What Neo v0 Did Better Than Anyone
1. **Declarative dependency graph** (`requires`/`generates` in index.yaml) — no other framework has this
2. **Input validation schemas** with `min_length`, `required_sections`, `min_items` — structural enforcement, not just "does file exist?"
3. **Output quality metrics** with percentage thresholds and pass/fail conditions
4. **Chain position metadata** linking each step to its predecessor
5. **Knowledge graph generation** (`optimze_depd_graph.js`) for runtime codebase analysis
6. **Traceability mapping** in story decomposition (Story → Tasks → Tests → Requirements)

### What Neo v0 Didn't Do / Limitations
1. **No auto-invocation** — dependencies were declarations, not active triggers
2. **Monolithic context** — the entire 132KB YAML was loaded at once, consuming massive token budget
3. **No phase gates** — no GO/NO-GO decisions between phases
4. **No handoff protocol** — no JSON files passing context between phases
5. **Designed for Cline** — relied on Cline's tool system, not Claude's native skills/agents
6. **Over-engineered for AI execution** — many of the XML schemas were aspirational (vector DB, ChromaDB) rather than what the AI could actually execute

---

## 5. ETUS PMDocs (Current Implementation)

### Architecture
- 25 skills, 7 agents, 7 commands
- 4 phases: Discovery → Planning → Design → Implementation
- Handoff protocol (JSON files for phase chaining)
- IDs traceability: BO-# → PRD-F-# → US-# → FS-# → impl-#

### Current Dependency Enforcement: **WARN → SUGGEST → ASK → MARK**

Our 19 skills have a `## DEPENDENCIES` section with:
```markdown
**Required upstream:**
- `docs/ets-docs/architecture/architecture-diagram.md` — needed for X

**Dependency check:** Before generating, verify upstream exists. If missing:
1. WARN: "⚠ Required document X not found..."
2. SUGGEST: "Run /design first to generate it..."
3. ASK: "Continue anyway (generic output) or generate upstream first?"
4. If continue, add <!-- WARNING --> comment at top
```

### Gap Analysis vs Other Frameworks

| Aspect | BMAD | Superpowers | Compound Eng. | Neo v0 | ETUS PMDocs |
|--------|------|-------------|---------------|--------|-------------|
| **Dependency location** | Inside workflow init step | Prose in SKILL.md | N/A (loop model) | `index.yaml` + XML `<requires>` + chain orchestrator | `## DEPENDENCIES` section |
| **Enforcement type** | Hard block | Implicit (prose) | Coverage gate | Declarative graph + input validation schemas | Soft (WARN + ASK) |
| **Missing prerequisite** | Block + tell which command | Prose says "do X first" | N/A | `blockingIssues` in output schema (passive) | Warn + offer to continue |
| **Auto-generate upstream** | No | No | No | No (declarations only, no auto-trigger) | No |
| **Dependency metadata** | No (procedural) | No (prose) | No (namespace) | Yes — `requires`, `generates`, `chain-position`, `input_validation` | Partial (in SKILL.md) |
| **Skill invocation chain** | Completion step suggests next | Explicit "invoke X next" | Loop phases | Chain orchestrator `nextAction` + `pendingDocuments` | Suggest command |
| **Input validation** | File existence only | None | Coverage thresholds | Structural (`min_length`, `required_sections`, `min_items`) | None |
| **Output quality gates** | None | None | `.coverage-thresholds.json` | Percentage metrics + `pass_fail` boolean conditions | Phase gates (GO/NO-GO) |

---

## 6. Key Findings

### Finding 1: Nobody Auto-Generates Missing Prerequisites
None of the four frameworks automatically invoke upstream skills when prerequisites are missing. All rely on some form of "go run X first" messaging. Neo v0 had the infrastructure (declarative `requires`/`generates`) but never wired it to auto-invocation.

### Finding 2: BMAD's Hard Block is the Strongest Enforcement Pattern
BMAD's approach of **refusing to proceed** at workflow init is the most robust runtime enforcement. The AI can't rationalize skipping the prerequisite because the workflow simply won't start.

### Finding 3: Neo v0 Had the Best Dependency Model — But Never Activated It
Our own predecessor framework already had a centralized `requires`/`generates` graph, input validation schemas with structural enforcement (`min_length`, `required_sections`), and output quality metrics with thresholds. This is more sophisticated than anything BMAD, Superpowers, or Compound Engineering offer. The gap: these declarations were **passive metadata** — the system never blocked execution when dependencies were unmet.

### Finding 4: Input Validation > File Existence
Neo v0's approach of checking **content structure** (does `product_vision` have an `overview` section with at least 50 chars?) is far superior to BMAD's binary "does file exist?" check. A file can exist and be empty or incomplete — structural validation catches this.

### Finding 5: Our WARN+ASK Pattern is Too Permissive
Offering "continue anyway" means the AI (or user) will often say yes, producing documents without proper context. BMAD's hard block proves that this degrades output quality.

### Finding 6: Superpowers' Anti-Rationalization is a Useful Complement
The "12 rationalization patterns" in the meta-skill is clever — it preempts the AI from talking itself out of following the process. This is orthogonal to structural enforcement and can be layered on top.

### Finding 7: The Best System Combines Declarative Graph + Active Enforcement + Structural Validation
No single framework has all three. Neo v0 had the graph and validation but not active enforcement. BMAD has enforcement but no graph. The ideal is: **Neo v0's declarative model + BMAD's hard blocking + Neo v0's structural validation + Superpowers' anti-rationalization.**

---

## 7. Recommended Improvements for ETUS PMDocs

Based on all five frameworks analyzed, here's the revised improvement plan. Each improvement cites which framework(s) inspired it.

### Improvement 1: Centralized `dependency-graph.yaml` (from Neo v0)

Neo v0's `index.yaml` with `requires`/`generates` was its strongest pattern. Adopt this as the single source of truth for all document dependencies. Every skill reads from this graph instead of maintaining its own `## DEPENDENCIES` section.

```yaml
# .claude/skills/orchestrator/dependency-graph.yaml
documents:
  project-context:
    produces: docs/ets-docs/discovery/project-context.md
    requires: []
    enriched-by: []
    skill: project-context
    phase: discovery

  product-vision:
    produces: docs/ets-docs/discovery/product-vision.md
    requires: [project-context]
    enriched-by: []
    skill: product-vision
    phase: discovery

  prd:
    produces: docs/ets-docs/planning/prd.md
    requires: [product-vision]
    enriched-by: [project-context]
    skill: prd
    phase: planning

  user-stories:
    produces: docs/ets-docs/planning/user-stories.md
    requires: [prd]
    enriched-by: [product-vision]
    skill: user-stories
    phase: planning

  architecture-diagram:
    produces: docs/ets-docs/architecture/architecture-diagram.md
    requires: [prd, user-stories]
    enriched-by: [project-context]
    skill: architecture-diagram
    phase: design

  tech-spec:
    produces: docs/ets-docs/architecture/tech-spec.md
    requires: [architecture-diagram]
    enriched-by: [prd, project-context]
    skill: tech-spec
    phase: design

  data-requirements:
    produces: docs/ets-docs/data/data-requirements.md
    requires: [user-stories]
    enriched-by: [prd]
    skill: data-requirements
    phase: design

  erd:
    produces: docs/ets-docs/data/erd.md
    requires: [data-requirements]
    enriched-by: []
    skill: erd
    phase: design

  database-spec:
    produces: docs/ets-docs/data/database-spec.md
    requires: [erd]
    enriched-by: [tech-spec]
    skill: database-spec
    phase: design

  data-dictionary:
    produces: docs/ets-docs/data/data-dictionary.md
    requires: [database-spec]
    enriched-by: []
    skill: data-dictionary
    phase: design

  data-flow-diagram:
    produces: docs/ets-docs/data/data-flow-diagram.md
    requires: [erd, data-dictionary]
    enriched-by: [architecture-diagram]
    skill: data-flow-diagram
    phase: design

  data-catalog:
    produces: docs/ets-docs/data/data-catalog.md
    requires: [database-spec, data-dictionary, data-flow-diagram]
    enriched-by: []
    skill: data-catalog
    phase: design

  user-journey:
    produces: docs/ets-docs/ux/user-journey.md
    requires: [product-vision]
    enriched-by: [user-stories]
    skill: user-journey
    phase: design

  ux-sitemap:
    produces: docs/ets-docs/ux/ux-sitemap.md
    requires: [user-journey]
    enriched-by: [wireframes]
    skill: ux-sitemap
    phase: design

  wireframes:
    produces: docs/ets-docs/ux/wireframes.md
    requires: [ux-sitemap]
    enriched-by: [style-guide]
    skill: wireframes
    phase: design

  style-guide:
    produces: docs/ets-docs/ux/style-guide.md
    requires: [wireframes]
    enriched-by: []
    skill: style-guide
    phase: design

  api-spec:
    produces: docs/ets-docs/implementation/api-spec.md
    requires: [tech-spec, database-spec, user-stories]
    enriched-by: [architecture-diagram]
    skill: api-spec
    phase: design

  implementation-plan:
    produces: docs/ets-docs/implementation/implementation-plan.md
    requires: [user-stories, tech-spec]
    enriched-by: [api-spec, architecture-diagram]
    skill: implementation-plan
    phase: implementation

  sprint-status:
    produces: docs/ets-docs/implementation/sprint-status.yaml
    requires: [implementation-plan]
    enriched-by: []
    skill: sprint-status
    phase: implementation

  quality-checklist:
    produces: docs/ets-docs/implementation/quality-checklist.md
    requires: [user-stories, tech-spec]
    enriched-by: [implementation-plan]
    skill: quality-checklist
    phase: implementation
```

**Why this matters:** Unlike the current approach where each SKILL.md maintains its own `## DEPENDENCIES` section (which can diverge), this graph is a single file the orchestrator and every skill reference. Changes propagate automatically.

### Improvement 2: Two-Tier Dependency Classification — BLOCKS vs ENRICHES (from BMAD + Neo v0)

Combine BMAD's hard blocking with Neo v0's declarative model. The `requires` field = BLOCKS, the `enriched-by` field = ENRICHES.

```
BLOCKS   = Required. Skill refuses to run. Auto-invokes upstream skill.
           (from: BMAD hard gate + Neo v0 `requires`)

ENRICHES = Optional. Skill runs but output is better with context.
           Warns user but proceeds.
           (new — neither BMAD nor Neo v0 had this distinction)
```

**In each SKILL.md**, replace the current WARN → SUGGEST → ASK → MARK with:

```markdown
## DEPENDENCY RESOLUTION

**BLOCKS** (must exist — auto-invoke if missing):
- `architecture-diagram.md` → Cannot generate tech-spec without system structure.

**ENRICHES** (improves output — warn if missing):
- `prd.md` → Tech spec is more business-aligned with PRD context.
- `project-context.md` → Tech stack constraints inform NFR targets.

**Resolution protocol:**
1. READ `dependency-graph.yaml` → find this document's `requires` and `enriched-by`
2. For each BLOCKS dep: check file exists AND is non-empty
3. If BLOCKS dep missing → INFORM user → AUTO-INVOKE upstream skill → wait → continue
4. For each ENRICHES dep: check file exists
5. If ENRICHES dep missing → WARN → proceed (no "continue anyway?" prompt)
```

### Improvement 3: Auto-Invoke Upstream Skill — Recursive Resolution (What Nobody Does Yet)

No framework auto-generates missing prerequisites. We can be the first. The mechanism:

```markdown
**Auto-invocation protocol:**
1. Skill X starts → reads dependency-graph.yaml → finds requires: [A, B]
2. Check: does A exist? does B exist?
3. A exists, B missing → INFORM: "tech-spec requires architecture-diagram.md. Generating it now."
4. INVOKE skill `architecture-diagram` (which itself will check ITS dependencies)
5. architecture-diagram checks: requires [prd, user-stories] → both exist → proceeds
6. architecture-diagram completes → returns to tech-spec → tech-spec continues
```

This is **recursive** — if architecture-diagram's own deps are missing, it invokes those first. The recursion stops at `project-context` (which has `requires: []`).

**Safety guard:** Maximum recursion depth = 5 (covers the longest chain: project-context → product-vision → prd → user-stories → architecture-diagram → tech-spec). If depth exceeded, hard block with error.

### Improvement 4: Input Content Validation (from Neo v0)

Neo v0's structural validation (min_length, required_sections, min_items) was ahead of its time. Adapt it for SKILL.md:

```markdown
## INPUT VALIDATION

**architecture-diagram.md** (BLOCKS):
  - Must contain: `## System Context`, `## Container View`
  - Minimum length: 200 lines (a real architecture doc, not a stub)

**prd.md** (ENRICHES):
  - Must contain at least one `PRD-F-#` identifier
  - Must contain: `## Features`
```

This catches the edge case where someone creates an empty file just to bypass the existence check. A file that exists but is a stub fails validation just like a missing file.

### Improvement 5: Output Quality Gate per Skill (from Neo v0 + Compound Engineering)

Neo v0 had per-document output metrics (coverage %, pass/fail conditions). Compound Engineering has `.coverage-thresholds.json`. Add a lightweight version:

```markdown
## OUTPUT VALIDATION

Before marking this document as complete:
- [ ] All `BO-#` from product-vision.md are referenced (traceability)
- [ ] At least 3 `PRD-F-#` features defined (completeness)
- [ ] Each feature has MoSCoW priority assigned (prioritization)
- [ ] MVP boundary is explicitly defined (scope)

If any check fails → mark document as DRAFT, not COMPLETE.
```

This prevents half-baked documents from satisfying downstream dependencies. A DRAFT document does not satisfy a BLOCKS dependency.

### Improvement 6: Anti-Rationalization Rules (from Superpowers)

Add to the orchestrator skill a block of patterns the AI must never use to skip dependency enforcement:

```markdown
## ANTI-RATIONALIZATION RULES

NEVER skip dependency checks with these excuses:
- "The user seems to know what they want" → Dependencies still apply
- "I can infer the context from conversation" → Inferred context ≠ documented context
- "This is a simple/small project" → All projects need upstream documents
- "The user said continue anyway" → Only valid for ENRICHES, NEVER for BLOCKS
- "I'll add the missing info later" → Missing context produces cascading errors downstream
- "The upstream doc exists but seems incomplete" → Run INPUT VALIDATION, don't assume
- "I already have enough context from the chat" → Chat context is ephemeral; documents persist
```

### Improvement 7: Handoff Carries Dependency Status (existing + enhanced)

Our existing handoff protocol (discovery.json → planning.json → design.json → implementation.json) should include dependency resolution status:

```json
{
  "phase": "planning",
  "status": "complete",
  "documents": {
    "prd.md": { "status": "COMPLETE", "path": "docs/ets-docs/planning/prd.md", "ids": ["PRD-F-1", "PRD-F-2", "PRD-F-3"] },
    "user-stories.md": { "status": "COMPLETE", "path": "docs/ets-docs/planning/user-stories.md", "ids": ["US-1", "US-2", "US-3", "US-4"] },
    "feature-spec-auth.md": { "status": "DRAFT", "path": "docs/ets-docs/planning/feature-specs/feature-spec-auth.md" }
  },
  "unresolved_dependencies": [],
  "gate_result": "GO"
}
```

The next phase reads this handoff and knows exactly which documents are COMPLETE vs DRAFT before starting.

---

## 8. Implementation Priority

| Priority | Improvement | Effort | Impact | Source |
|----------|-------------|--------|--------|--------|
| **P0** | #1 Centralized dependency-graph.yaml | Medium | High | Neo v0 |
| **P0** | #2 BLOCKS vs ENRICHES classification | Low | High | BMAD + Neo v0 |
| **P1** | #3 Auto-invoke upstream skill | High | Very High | Novel (ours) |
| **P1** | #6 Anti-rationalization rules | Low | Medium | Superpowers |
| **P2** | #4 Input content validation | Medium | High | Neo v0 |
| **P2** | #5 Output quality gate per skill | Medium | Medium | Neo v0 + Compound |
| **P3** | #7 Handoff dependency status | Low | Medium | Existing + Neo v0 |

**Recommended execution order:** Start with P0 (graph + classification) since all other improvements depend on having the centralized graph. Then P1 (auto-invoke + anti-rationalization) for the headline feature. P2 and P3 add depth.

---

## 9. Summary

The research across 5 frameworks reveals that **no one has cracked the full dependency enforcement problem**. Each framework solves a piece:

- **BMAD** → Best at hard blocking (but no graph, no auto-invoke)
- **Superpowers** → Best at preventing AI rationalization (but purely behavioral)
- **Compound Engineering** → Best at coverage gates (but loop model, not pipeline)
- **Neo v0** → Best at declarative dependency modeling (but passive, never enforced at runtime)
- **ETUS PMDocs** → Best at phase handoffs (but too permissive on individual skill deps)

The proposed system combines all five strengths: Neo v0's declarative graph as the backbone, BMAD's hard blocking as the enforcement mechanism, auto-invocation as the novel contribution, Neo v0's structural validation for content quality, Superpowers' anti-rationalization as a behavioral safeguard, and our existing handoff protocol as the phase-level coordination layer.
