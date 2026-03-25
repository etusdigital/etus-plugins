# Validate

Run quality checks on documentation. Accepts a phase or check type as argument.

## Usage

```
/validate ideate        -> Ideation Readiness Gate
/validate discover      -> Discovery Gate
/validate opportunities -> Opportunity Focus Gate
/validate solution      -> Solution Readiness Gate
/validate plan          -> Requirements Gate (legacy alias)
/validate design        -> Implementation Readiness Gate
/validate sst           -> Single Source of Truth check
/validate traceability  -> ID traceability chain check
/validate all           -> Run all checks
```

## Routing

Based on $ARGUMENTS:

### Gate Validation (ideate | discover | opportunities | solution | plan | design)

Spawn the validate-gate skill with phase = $ARGUMENTS.

**Ideation Readiness Gate checklist:**
- [ ] opportunity-pack.md exists and is populated?
- [ ] coverage-matrix.yaml exists and meets the threshold for the mode?
- [ ] Problem is defined independently from the proposed solution?
- [ ] Actors, JTBDs, journeys, use cases, and edge cases are explicitly mapped?
- [ ] Guardrails and blocking questions are explicit?

**Discovery Gate checklist:**
- [ ] 5W2H interview complete (all 7 dimensions addressed)?
- [ ] Problem clearly defined and validated with user?
- [ ] Business opportunity quantified (market size, revenue potential)?
- [ ] At least 1 BO-# defined in product-vision.md?
- [ ] Vision statement is clear and specific?

**Opportunity Focus Gate checklist:**
- [ ] OST contains opportunities instead of backlog items?
- [ ] Prioritization is evidence-backed?
- [ ] The selected `O-#` items are clear enough to enter solution discovery?

**Solution Readiness Gate checklist:**
- [ ] `solution-discovery.md` exists in Planning mode, or `features/{feature-slug}/solution-discovery.md` exists in Feature mode?
- [ ] At least 2 `SOL-#` options were considered unless scope is trivially narrow?
- [ ] Value/usability/viability/feasibility risks were evaluated?
- [ ] A recommended solution exists?
- [ ] Unresolved risks are explicit?

**Requirements Gate checklist:**
- [ ] All PRD-F-# trace to at least one BO-#?
- [ ] MoSCoW prioritization complete (all features categorized)?
- [ ] MVP scope defined (Must-have features only)?
- [ ] All delivery requirements trace to `SOL-#`?
- [ ] All US-# have Given/When/Then acceptance criteria?
- [ ] Complex features (>3 business rules) have feature specs?

**Implementation Readiness Gate checklist:**
- [ ] Architecture addresses all NFR-# targets?
- [ ] Data model covers all entities from user stories?
- [ ] All wireframe components reference tok.* from style-guide?
- [ ] API spec covers all user-facing operations?
- [ ] No cross-validation conflicts between data/ux/api?

Present the checklist interactively. Ask for GO/NO-GO/ITERATE decision.

### SST Check (sst)

Spawn the check-sst skill (forked Explore agent — read-only scan).
Checks that each content type is defined in exactly one document:
- Given/When/Then only in user-stories.md
- NFR-# targets only in tech-spec.md
- ADR-# decisions only in tech-spec.md
- DDL (CREATE TABLE) only in database-spec.md
- dict.*/ev.* definitions only in data-dictionary.md
- tok.* design tokens only in style-guide.md
- API schemas only in api-spec.md

Returns violation report with file, line, and correction needed.

### Traceability Check (traceability)

Spawn the check-traceability skill (forked Explore agent — read-only scan).
Validates the complete ID chain: ACT/JTBD/JOUR/UC/EDGE -> BO/O/SOL -> PRD-F/FB -> US -> FS -> impl
Reports orphan IDs (defined but never referenced) and broken links (referenced but undefined).

### Full Validation (all)

Run sst + traceability in parallel, then present combined report with:
- Total violations found
- Severity breakdown (critical / warning / info)
- Recommended fixes

$ARGUMENTS
