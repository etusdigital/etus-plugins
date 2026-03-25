---
description: Validate gate criteria for current phase (discovery|planning|implementation-readiness)
argument-hint: discovery|planning|implementation-readiness
allowed-tools: Read, Grep, Bash
model: sonnet
---

# Gate Validation

Validating **$ARGUMENTS** gate criteria

## Gate Selection

Checking which gate to validate: **$ARGUMENTS**

Valid gates: `discovery`, `planning`, `implementation-readiness`

---

# Discovery Gate Validation

!`if [ "$ARGUMENTS" = "discovery" ]; then echo "Running Discovery Gate validation..."; fi`

## Vision Completeness

**One-line vision statement**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -A 1 "^# " docs/discovery/product-vision.md 2>/dev/null | head -2 || echo "✗ product-vision.md not found"; fi`

**5W2H Analysis Check**:
!`if [ "$ARGUMENTS" = "discovery" ]; then
  count=0
  grep -i "WHAT" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHO" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHERE" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHEN" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHY" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "HOW" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "HOW MUCH" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  echo "5W2H coverage: $count/7"
  [ $count -ge 7 ] && echo "✓ Complete" || echo "✗ Incomplete"
fi`

**North Star Metric**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -i "north star" docs/discovery/product-vision.md >/dev/null 2>&1 && echo "✓ NSM defined" || echo "✗ NSM missing"; fi`

**Critical Success Drivers**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -i "critical success" docs/discovery/product-vision.md >/dev/null 2>&1 && echo "✓ CSDs defined" || echo "✗ CSDs missing"; fi`

**Kill Criteria**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -i "kill criteria" docs/discovery/product-vision.md >/dev/null 2>&1 && echo "✓ Kill criteria defined" || echo "✗ Kill criteria missing"; fi`

## Business Case Section

**Business Case in product-vision.md**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -i "business case\|business objectives" docs/discovery/product-vision.md >/dev/null 2>&1 && echo "✓ Business case documented" || echo "✗ Business case missing"; fi`

**Business Objectives (BO-#)**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -o "BO-[0-9]*" docs/discovery/product-vision.md 2>/dev/null | sort -u | wc -l | xargs echo "Business objectives found:"; fi`

**ROI Justification**:
!`if [ "$ARGUMENTS" = "discovery" ]; then grep -i "ROI\|return on investment" docs/discovery/product-vision.md >/dev/null 2>&1 && echo "✓ ROI documented" || echo "✗ ROI missing"; fi`

## Project Constitution

**project-context.md exists**:
!`if [ "$ARGUMENTS" = "discovery" ]; then test -f docs/project-context.md && echo "✓ project-context.md found" || echo "✗ project-context.md missing"; fi`

## Decision

!`if [ "$ARGUMENTS" = "discovery" ]; then
  test -f docs/discovery/product-vision.md && test -f docs/project-context.md && \
  grep -i "north star" docs/discovery/product-vision.md >/dev/null 2>&1 && \
  grep -i "kill criteria" docs/discovery/product-vision.md >/dev/null 2>&1 && \
  grep -i "business case\|business objectives" docs/discovery/product-vision.md >/dev/null 2>&1 && \
  echo "✓✓✓ DISCOVERY GATE: PASS ✓✓✓" || \
  echo "✗✗✗ DISCOVERY GATE: FAIL ✗✗✗"
fi`

---

# Planning Gate Validation

!`if [ "$ARGUMENTS" = "planning" ]; then echo "Running Planning Gate validation..."; fi`

## Requirements Completeness

**PRD exists**:
!`if [ "$ARGUMENTS" = "planning" ]; then test -f docs/planning/prd.md && echo "✓ prd.md found" || echo "✗ prd.md missing"; fi`

**Product Features (PRD-F-#) with MoSCoW**:
!`if [ "$ARGUMENTS" = "planning" ]; then
  prd_count=$(grep -o "PRD-F-[0-9]*" docs/planning/prd.md 2>/dev/null | sort -u | wc -l)
  moscow_found=$(grep -i "must\|should\|could\|won't" docs/planning/prd.md 2>/dev/null | wc -l)
  echo "Product features found: $prd_count"
  [ $moscow_found -gt 0 ] && echo "✓ MoSCoW prioritization present" || echo "✗ MoSCoW prioritization missing"
fi`

**User Stories (US-#) with Given/When/Then**:
!`if [ "$ARGUMENTS" = "planning" ]; then
  us_count=$(grep -o "US-[0-9]*" docs/planning/user-stories.md 2>/dev/null | sort -u | wc -l)
  echo "User stories found: $us_count"
  given=$(grep -c "^Given" docs/planning/user-stories.md 2>/dev/null || echo 0)
  when=$(grep -c "^When" docs/planning/user-stories.md 2>/dev/null || echo 0)
  then=$(grep -c "^Then" docs/planning/user-stories.md 2>/dev/null || echo 0)
  echo "Given/When/Then scenarios: $given/$when/$then"
  [ $given -ge 3 ] && echo "✓ Adequate acceptance criteria coverage" || echo "✗ Need more scenarios"
fi`

**Feature Specs for Complex Features**:
!`if [ "$ARGUMENTS" = "planning" ]; then
  fs_count=$(find docs/planning/feature-specs -name "*.md" 2>/dev/null | wc -l)
  echo "Feature spec files found: $fs_count"
  [ $fs_count -gt 0 ] && echo "✓ Feature specs exist" || echo "⚠ No feature specs (may be optional for simple features)"
fi`

**No TBD in P0 scope**:
!`if [ "$ARGUMENTS" = "planning" ]; then grep -i "TBD\|TODO\|FIXME" docs/planning/user-stories.md 2>/dev/null | grep -i "P0" >/dev/null && echo "✗ TBD found in P0 stories" || echo "✓ No TBD in P0"; fi`

## Traceability Chain

**Complete chain check**:
!`if [ "$ARGUMENTS" = "planning" ]; then
  echo "Traceability: vis → BO-# → PRD-F-# → US-# → FS-*"
  test -f docs/discovery/product-vision.md && echo "✓ vis"
  grep -q "BO-[0-9]" docs/discovery/product-vision.md 2>/dev/null && echo "✓ BO-#"
  grep -q "PRD-F-[0-9]" docs/planning/prd.md 2>/dev/null && echo "✓ PRD-F-#"
  grep -q "US-[0-9]" docs/planning/user-stories.md 2>/dev/null && echo "✓ US-#"
  [ -d docs/planning/feature-specs ] && [ -n "$(find docs/planning/feature-specs -name '*.md' 2>/dev/null)" ] && echo "✓ FS-*" || echo "⚠ FS-* (optional)"
fi`

## Decision

!`if [ "$ARGUMENTS" = "planning" ]; then
  test -f docs/planning/prd.md && test -f docs/planning/user-stories.md && \
  grep -q "PRD-F-[0-9]" docs/planning/prd.md 2>/dev/null && \
  grep -q "US-[0-9]" docs/planning/user-stories.md 2>/dev/null && \
  ! (grep -i "TBD\|TODO\|FIXME" docs/planning/user-stories.md 2>/dev/null | grep -i "P0" >/dev/null) && \
  echo "✓✓✓ PLANNING GATE: PASS ✓✓✓" || \
  echo "✗✗✗ PLANNING GATE: FAIL ✗✗✗"
fi`

---

# Implementation-Readiness Gate Validation

!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then echo "Running Implementation-Readiness Gate validation..."; fi`

## Architecture Track

**architecture-diagram.md exists**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then test -f docs/design/architecture-diagram.md && echo "✓ architecture-diagram.md found" || echo "✗ Missing"; fi`

**tech-spec.md with NFR-# and ADR-#**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  test -f docs/design/tech-spec.md && echo "✓ tech-spec.md found" || echo "✗ Missing"
  grep -o "NFR-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | wc -l | xargs echo "NFRs found:"
  grep -o "ADR-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | wc -l | xargs echo "ADRs found:"
fi`

## Data Track

**Data documents (7 expected)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  echo "Data documents:"
  test -f docs/design/data-requirements.md && echo "✓ data-requirements.md"
  test -f docs/design/erd.md && echo "✓ erd.md"
  test -f docs/design/database-spec.md && echo "✓ database-spec.md"
  test -f docs/design/data-dictionary.md && echo "✓ data-dictionary.md"
  test -f docs/design/data-flow-diagram.md && echo "✓ data-flow-diagram.md"
  test -f docs/design/data-catalog.md && echo "✓ data-catalog.md"
  data_count=$(ls docs/design/*.md 2>/dev/null | wc -l)
  echo "Total: $data_count/6 core data files"
fi`

## UX Track

**UX documents (4 expected)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  echo "UX documents:"
  test -f docs/design/user-journey.md && echo "✓ user-journey.md"
  test -f docs/design/ux-sitemap.md && echo "✓ ux-sitemap.md"
  test -f docs/design/wireframes.md && echo "✓ wireframes.md"
  test -f docs/design/style-guide.md && echo "✓ style-guide.md"
  ux_count=$(ls docs/design/*.md 2>/dev/null | wc -l)
  echo "Total: $ux_count/4 core UX files"
fi`

## Implementation Track

**API spec**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then test -f docs/implementation/api-spec.md && echo "✓ api-spec.md found" || echo "✗ Missing"; fi`

**Implementation plan**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then test -f docs/implementation/implementation-plan.md && echo "✓ implementation-plan.md found" || echo "✗ Missing"; fi`

## Single Source of Truth Validation

**tok.* tokens (ONLY in style-guide.md)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  tok_count=$(grep -r "tok\.[a-z.]*" docs/ --include="*.md" 2>/dev/null | grep -v "style-guide.md" | wc -l)
  [ $tok_count -eq 0 ] && echo "✓ tok.* only in style-guide.md" || echo "✗ tok.* found in $tok_count other files (violation!)"
fi`

**dict.* fields (ONLY in data-dictionary.md)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  dict_count=$(grep -r "dict\.[a-z.]*" docs/ --include="*.md" 2>/dev/null | grep -v "data-dictionary.md" | wc -l)
  [ $dict_count -eq 0 ] && echo "✓ dict.* only in data-dictionary.md" || echo "✗ dict.* found in $dict_count other files (violation!)"
fi`

**ev.* events (ONLY in data-dictionary.md)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  ev_count=$(grep -r "ev\.[a-z.]*" docs/ --include="*.md" 2>/dev/null | grep -v "data-dictionary.md" | wc -l)
  [ $ev_count -eq 0 ] && echo "✓ ev.* only in data-dictionary.md" || echo "✗ ev.* found in $ev_count other files (violation!)"
fi`

**DDL statements (ONLY in database-spec.md)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  ddl_count=$(grep -r "CREATE TABLE\|ALTER TABLE\|DROP TABLE" docs/ --include="*.md" 2>/dev/null | grep -v "database-spec.md" | wc -l)
  [ $ddl_count -eq 0 ] && echo "✓ DDL only in database-spec.md" || echo "✗ DDL found in $ddl_count other files (violation!)"
fi`

## Supporting Documents

**sprint-status.yaml exists**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then test -f docs/sprint-status.yaml && echo "✓ sprint-status.yaml found" || echo "✗ Missing"; fi`

**quality-checklist.md exists**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then test -f docs/quality-checklist.md && echo "✓ quality-checklist.md found" || echo "✗ Missing"; fi`

## Total Document Count

**Base documentation (21 expected)**:
!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  doc_count=$(find docs/ -name "*.md" -o -name "*.yaml" -type f 2>/dev/null | wc -l)
  echo "Total documents found: $doc_count (expecting ~21+ base docs)"
  [ $doc_count -ge 21 ] && echo "✓ Adequate documentation" || echo "✗ Missing documentation"
fi`

## Decision

!`if [ "$ARGUMENTS" = "implementation-readiness" ]; then
  arch_ok=0
  data_ok=0
  ux_ok=0
  impl_ok=0
  sst_ok=0

  [ -f docs/design/architecture-diagram.md ] && [ -f docs/design/tech-spec.md ] && ((arch_ok=1))
  data_count=$(ls docs/design/*.md 2>/dev/null | wc -l)
  [ $data_count -ge 6 ] && ((data_ok=1))
  ux_count=$(ls docs/design/*.md 2>/dev/null | wc -l)
  [ $ux_count -ge 4 ] && ((ux_ok=1))
  [ -f docs/implementation/api-spec.md ] && [ -f docs/implementation/implementation-plan.md ] && ((impl_ok=1))

  tok_count=$(grep -r "tok\.[a-z.]*" docs/ --include="*.md" 2>/dev/null | grep -v "style-guide.md" | wc -l)
  dict_count=$(grep -r "dict\.[a-z.]*" docs/ --include="*.md" 2>/dev/null | grep -v "data-dictionary.md" | wc -l)
  ev_count=$(grep -r "ev\.[a-z.]*" docs/ --include="*.md" 2>/dev/null | grep -v "data-dictionary.md" | wc -l)
  ddl_count=$(grep -r "CREATE TABLE\|ALTER TABLE\|DROP TABLE" docs/ --include="*.md" 2>/dev/null | grep -v "database-spec.md" | wc -l)
  [ $tok_count -eq 0 ] && [ $dict_count -eq 0 ] && [ $ev_count -eq 0 ] && [ $ddl_count -eq 0 ] && ((sst_ok=1))

  if [ $arch_ok -eq 1 ] && [ $data_ok -eq 1 ] && [ $ux_ok -eq 1 ] && [ $impl_ok -eq 1 ] && [ $sst_ok -eq 1 ]; then
    echo "✓✓✓ IMPLEMENTATION-READINESS GATE: PASS ✓✓✓"
  else
    echo "✗✗✗ IMPLEMENTATION-READINESS GATE: FAIL ✗✗✗"
    [ $arch_ok -eq 0 ] && echo "  ✗ Architecture track incomplete"
    [ $data_ok -eq 0 ] && echo "  ✗ Data track incomplete"
    [ $ux_ok -eq 0 ] && echo "  ✗ UX track incomplete"
    [ $impl_ok -eq 0 ] && echo "  ✗ Implementation track incomplete"
    [ $sst_ok -eq 0 ] && echo "  ✗ SST violations detected"
  fi
fi`

!`if [ "$ARGUMENTS" = "implementation-readiness" ] && [ $arch_ok -eq 1 ] && [ $data_ok -eq 1 ] && [ $ux_ok -eq 1 ] && [ $impl_ok -eq 1 ] && [ $sst_ok -eq 1 ]; then
  echo ""
  echo "===================="
  echo "✓✓✓ READY FOR IMPLEMENTATION ✓✓✓"
  echo "===================="
  echo ""
  echo "All documentation complete and consistent. Begin development using generated specifications."
fi`

---

## Invalid Gate

!`if [ "$ARGUMENTS" != "discovery" ] && [ "$ARGUMENTS" != "planning" ] && [ "$ARGUMENTS" != "implementation-readiness" ]; then
  echo "✗ Invalid gate: $ARGUMENTS"
  echo ""
  echo "Valid gates:"
  echo "  discovery - Validate problem, vision, and business case"
  echo "  planning - Validate requirements completeness"
  echo "  implementation-readiness - Validate all technical specs and SST consistency"
  echo ""
  echo "Usage: /validate-gate [gate-name]"
fi`
