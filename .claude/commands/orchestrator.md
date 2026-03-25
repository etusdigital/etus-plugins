# Orchestrator

Run the complete ETUS workflow: ideation layer + 4 product phases.

## Usage

```
/orchestrator              -> Start from Phase 1 (or resume from last completed phase)
/orchestrator planning     -> Jump to specific phase
/orchestrator resume       -> Detect current state and continue
```

## Workflow

### Phase Detection

1. Read `docs/ets/projects/{project-slug}/state/`
2. Find the latest completed phase:
   - `reports/implementation.json` exists -> all phases complete
   - `reports/design.json` exists -> ready for Implementation
   - `reports/planning.json` exists -> ready for Design
   - `reports/solution-report.json` exists -> ready for Requirements
   - `reports/opportunities.json` exists -> ready for Solution Discovery
   - `reports/discovery.json` exists -> ready for Opportunity Focus
   - `coverage-matrix.yaml` exists -> ready for Discovery
   - nothing exists -> start with Ideate
3. If $ARGUMENTS specifies a phase -> jump there
4. If "resume" -> start from next incomplete phase

### Execution Loop

For each phase:

**Opening Layer: Ideate**
1. Read the ideate.md command from .claude/commands/
2. Generate `docs/ets/projects/{project-slug}/discovery/opportunity-pack.md`
3. Generate `docs/ets/projects/{project-slug}/state/coverage-matrix.yaml`
4. Present Ideation Readiness Gate
5. Wait for user decision: GO / ITERATE

**Phase 1: Discovery**
1. Read the discover.md command from .claude/commands/
2. Use opportunity-pack + coverage-matrix as upstream context
3. Spawn the discovery-agent following discover.md instructions
4. When agent returns, verify `docs/ets/projects/{project-slug}/state/reports/discovery.json` was written
5. Present Discovery Gate (from validate.md routing)
6. Wait for user decision: GO / ITERATE / NO-GO

**Phase 2A: Opportunity Focus** (only if Discovery Gate = GO)
1. Read the plan.md command from .claude/commands/
2. Read `docs/ets/projects/{project-slug}/state/reports/discovery.json` for upstream context
3. Construct agent prompt: command content + handoff context
4. Spawn the planning-agent in `opportunities` mode
5. Verify `docs/ets/projects/{project-slug}/state/reports/opportunities.json` was written
6. Present Opportunity Focus Gate
7. Wait for user decision: GO / ITERATE

**Phase 2B: Solution Discovery** (only if Opportunity Focus Gate = GO)
1. Read the solution.md command from .claude/commands/
2. Read `docs/ets/projects/{project-slug}/state/reports/opportunities.json`
3. Spawn the planning-agent with the solution-discovery skill
4. Verify `docs/ets/projects/{project-slug}/state/reports/solution-report.json` was written
5. Present Solution Readiness Gate
6. Wait for user decision: GO / ITERATE / NO-GO

**Phase 2C: Requirements Definition** (only if Solution Readiness Gate = GO)
1. Read the plan.md command from .claude/commands/
2. Read `docs/ets/projects/{project-slug}/state/reports/solution-report.json` for upstream context
3. Spawn the planning-agent in `requirements` mode
4. Verify `docs/ets/projects/{project-slug}/state/reports/planning.json` was written
5. Present Requirements Gate
6. Wait for user decision: GO / DESCOPE / ITERATE

**Phase 3: Design** (only if Planning Gate = GO or DESCOPE)
1. Read the design.md command from .claude/commands/
2. Read `docs/ets/projects/{project-slug}/state/reports/planning.json`
3. Execute Stage 1 (architecture-agent, sequential)
4. Execute Stage 2 (data + ux + api agents, parallel)
5. Execute Stage 3 (merge + cross-validate)
6. Verify `docs/ets/projects/{project-slug}/state/reports/design.json` was written
7. Present Implementation Readiness Gate
8. Wait for user decision: GO / REDESIGN / ITERATE

**Phase 4: Implementation** (only if Design Gate = GO)
1. Read the implement.md command from .claude/commands/
2. Read `docs/ets/projects/{project-slug}/state/reports/design.json`
3. Spawn the implementation-agent
4. Verify `docs/ets/projects/{project-slug}/state/reports/implementation.json` was written
5. All product-mode documents complete

### Context Chain

```
(nothing) -> state/coverage-matrix.yaml
             -> state/reports/discovery.json
             -> state/reports/opportunities.json
             -> state/reports/solution-report.json
             -> state/reports/planning.json
             -> state/reports/design.json
             -> state/reports/implementation.json
```

Each phase reads the previous handoff and passes it as context to the agent.
The orchestrator is the glue that reads handoffs and chains commands.

### Decision Handling

| Decision | Action |
|----------|--------|
| GO | Continue to next phase |
| ITERATE | Re-run current phase (increment iteration counter in handoff) |
| NO-GO | Stop workflow, preserve all generated docs |
| DESCOPE | User marks features as Won't, update PRD, continue |
| REDESIGN | Return to specific design sub-phase (data/ux/api/arch) |

$ARGUMENTS
