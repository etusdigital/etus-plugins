# Elicit — Semantic Stress-Test

Run a focused interrogation on existing documentation to find ambiguities, contradictions, missing boundaries, and hidden assumptions.

## Usage

```bash
/elicit                    # Run on current project scope
/elicit [feature-slug]     # Run on specific feature
/elicit --focus=permissions # Focus on specific dimension
/elicit --focus=failures    # Focus on failure modes
/elicit --focus=consistency # Focus on cross-doc consistency
```

## What It Does

Does NOT create new product artifacts. It interrogates existing ones and generates a findings report.

**8 Interrogation Techniques:**
1. Developer simulation — "If I were implementing this, what would I still need to ask?"
2. Cross-doc consistency — Compare DB constraints vs data-dictionary vs API schema vs feature-spec
3. Vague quantifier scan — Search for "fast", "secure", "easy", "many", "few" without metrics
4. NG-# violation scan — Do downstream docs contradict non-goals?
5. EDGE-# resolution audit — For each EDGE-#, does a resolution exist downstream?
6. Missing error siblings — For each happy-path UC-#, does a corresponding error-path exist?
7. Permission matrix gap — Permission claims without formal role definition?
8. State machine completeness — For entities with states, are all transitions documented?

## Focus Dimensions

| Flag | Techniques Applied |
|------|-------------------|
| `--focus=permissions` | #7 Permission matrix gap (deep) |
| `--focus=failures` | #5 EDGE-# audit + #6 Missing error siblings + #8 State machine |
| `--focus=consistency` | #2 Cross-doc consistency + #4 NG-# violations |
| (no flag) | All 8 techniques |

## Output

Generates a findings report categorized by type:
- **EL-A-#** — Ambiguities
- **EL-C-#** — Contradictions
- **EL-B-#** — Missing boundaries
- **EL-H-#** — Hidden assumptions
- **EL-E-#** — Unresolved edges
- **EL-D-#** — Developer questions

The report is saved to `docs/ets/projects/{project-slug}/state/reports/elicit-report.md`.

## Execution

Spawn the validation skill `.claude/skills/validation/elicit/SKILL.md` with the scope argument.

Pass arguments:
- `$1` = feature-slug or empty for full project
- `--focus` = dimension filter (optional)
