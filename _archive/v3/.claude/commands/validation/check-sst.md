---
description: Validate Single Source of Truth (SST) compliance - ensure no duplicate definitions across documents in v3 system
allowed-tools: Read, Grep, Bash
model: sonnet
---

# Single Source of Truth Validation (v3)

Ensuring each concept has exactly ONE authoritative definition location in the v3 solo-templates system.

## Overview

**Single Source of Truth (SST)** means each concept is defined in exactly ONE place, and all other documents REFERENCE it (not redefine it).

This prevents:
- ❌ Duplicate definitions that can drift out of sync
- ❌ Inconsistent specifications across documents
- ❌ Update conflicts when changes are needed

**V3 Directory Structure:**
- `docs/discovery/` — project-context.md, product-vision.md
- `docs/planning/` — prd.md, user-stories.md, feature-specs/
- `docs/design/` — architecture-diagram.md, tech-spec.md, data-*.md, user-journey.md, ux-sitemap.md, wireframes.md, style-guide.md, api-spec.md
- `docs/implementation/` — implementation-plan.md, sprint-status.yaml, quality-checklist.md

---

## Rule 1: Given/When/Then → ONLY in User Stories

**Authoritative Source**: `docs/planning/user-stories.md`

**Validation**:
!`echo "=== Given/When/Then Validation ==="`
!`stories_gwt=$(grep -c "^Given\|^When\|^Then" docs/planning/user-stories.md 2>/dev/null || echo 0)
echo "Given/When/Then in user-stories.md: $stories_gwt scenarios"
[ $stories_gwt -gt 0 ] && echo "✓ Acceptance criteria defined in stories" || echo "⚠ No Given/When/Then found in stories"`

**Checking for violations**:
!`violations=0
for file in docs/design/*.md docs/planning/prd.md docs/planning/feature-specs/*.md; do
  if [ -f "$file" ] && grep -q "^Given\|^When\|^Then" "$file" 2>/dev/null; then
    echo "✗ VIOLATION: Given/When/Then found in $file"
    ((violations++))
  fi
done
[ $violations -eq 0 ] && echo "✓ Given/When/Then only in user-stories.md" || echo "✗ Found $violations SST violations"`

**Why**: Acceptance criteria belong to user stories. Feature specs and other docs should reference `US-#` IDs, not restate criteria.

---

## Rule 2: NFR Numeric Targets → ONLY in Tech Spec

**Authoritative Source**: `docs/design/tech-spec.md`

**Validation**:
!`echo ""`
!`echo "=== NFR Targets Validation ==="`
!`nfrs=$(grep -o "NFR-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | wc -l || echo 0)
echo "NFRs defined in tech-spec.md: $nfrs"`
[ $nfrs -gt 0 ] && echo "✓ NFRs defined in tech spec" || echo "⚠ No NFRs in tech spec"`

**Checking for violations** (numeric performance targets outside tech-spec):
!`violations=0
for file in docs/discovery/*.md docs/planning/*.md docs/design/*.md; do
  if [ -f "$file" ] && [ "$file" != "docs/design/tech-spec.md" ]; then
    # Check for patterns like "< 200ms" or "99.9% uptime" outside tech-spec
    if grep -E "[0-9]+\s*(ms|seconds?|minutes?)|[0-9]+\.?[0-9]*%.*uptime|[0-9]+ concurrent" "$file" 2>/dev/null | grep -v "NFR-" >/dev/null; then
      echo "⚠ Potential NFR target in $file (should reference NFR-# instead)"
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ NFR targets only in tech-spec.md" || echo "⚠ Found $violations potential violations"`

**Why**: Non-functional requirements with quantified targets (200ms, 99.9%, etc.) belong in tech-spec.md. Other docs should reference `NFR-#` IDs.

---

## Rule 3: Design Tokens (tok.*) → ONLY in Style Guide

**Authoritative Source**: `docs/design/style-guide.md`

**Validation**:
!`echo ""`
!`echo "=== Design Token Validation ==="`
!`tokens=$(grep -o "tok\.[a-z._]*" docs/design/style-guide.md 2>/dev/null | sort -u | wc -l || echo 0)
echo "Design tokens in style-guide.md: $tokens"`
[ $tokens -gt 0 ] && echo "✓ Tokens defined in style guide" || echo "⚠ No tok.* tokens in style guide"`

**Checking for violations** (tok.* definitions outside style-guide):
!`violations=0
definition_pattern="tok\.[a-z._]*.*[:=]"
for file in docs/design/wireframes.md docs/design/ux-sitemap.md docs/design/user-journey.md; do
  if [ -f "$file" ]; then
    if grep -E "$definition_pattern" "$file" 2>/dev/null >/dev/null; then
      echo "✗ VIOLATION: tok.* definition in $file"
      grep -E "$definition_pattern" "$file" | head -3
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ tok.* only defined in style-guide.md" || echo "✗ Found $violations SST violations"`

**References allowed** (tok.* usage without definition):
!`references=0
for file in docs/design/wireframes.md docs/design/ux-sitemap.md docs/design/user-journey.md; do
  if [ -f "$file" ]; then
    refs=$(grep -o "tok\.[a-z._]*" "$file" 2>/dev/null | wc -l || echo 0)
    [ $refs -gt 0 ] && echo "✓ $file references $refs tokens" && ((references+=refs))
  fi
done
[ $references -gt 0 ] && echo "✓ Other design docs reference tok.* (allowed)" || echo "⚠ No token references found"`

**Why**: Design tokens (colors, spacing, typography) are defined ONCE in style-guide.md. Other docs reference `tok.color.primary`, not `#3B82F6`.

---

## Rule 4: Field Definitions (dict.*) → ONLY in Data Dictionary

**Authoritative Source**: `docs/design/data-dictionary.md`

**Validation**:
!`echo ""`
!`echo "=== Field Definition Validation ==="`
!`fields=$(grep -o "dict\.[a-z._]*" docs/design/data-dictionary.md 2>/dev/null | sort -u | wc -l || echo 0)
echo "Field definitions in data-dictionary.md: $fields"`
[ $fields -gt 0 ] && echo "✓ Fields defined in dictionary" || echo "⚠ No dict.* fields in dictionary"`

**Checking for violations** (dict.* definitions outside data-dictionary):
!`violations=0
definition_pattern="dict\.[a-z._]*.*[:=]"
for file in docs/design/data-erd.md docs/design/database-spec.md docs/design/data-flow-diagram.md; do
  if [ -f "$file" ]; then
    if grep -E "$definition_pattern" "$file" 2>/dev/null >/dev/null; then
      echo "✗ VIOLATION: dict.* definition in $file"
      grep -E "$definition_pattern" "$file" | head -3
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ dict.* only defined in data-dictionary.md" || echo "✗ Found $violations SST violations"`

**References allowed**:
!`references=0
for file in docs/design/api-spec.md docs/design/database-spec.md docs/design/data-erd.md; do
  if [ -f "$file" ]; then
    refs=$(grep -o "dict\.[a-z._]*" "$file" 2>/dev/null | wc -l || echo 0)
    [ $refs -gt 0 ] && echo "✓ $file references $refs fields" && ((references+=refs))
  fi
done
[ $references -gt 0 ] && echo "✓ Design docs reference dict.* (allowed)" || echo "⚠ No field references found"`

**Why**: Field semantics (meaning, validation, format) are defined in data-dictionary.md. Database and API schemas reference `dict.user.email`, not redefine "email format: regex...".

---

## Rule 5: Event Definitions (ev.*) → ONLY in Data Dictionary

**Authoritative Source**: `docs/design/data-dictionary.md`

**Validation**:
!`echo ""`
!`echo "=== Event Definition Validation ==="`
!`events=$(grep -o "ev\.[a-z._]*" docs/design/data-dictionary.md 2>/dev/null | sort -u | wc -l || echo 0)
echo "Event definitions in data-dictionary.md: $events"`
[ $events -gt 0 ] && echo "✓ Events defined in dictionary" || echo "⚠ No ev.* events in dictionary"`

**Checking for violations** (ev.* definitions outside data-dictionary):
!`violations=0
definition_pattern="ev\.[a-z._]*.*[:=]"
for file in docs/design/api-spec.md docs/design/data-flow-diagram.md docs/discovery/project-context.md; do
  if [ -f "$file" ]; then
    if grep -E "$definition_pattern" "$file" 2>/dev/null >/dev/null; then
      echo "✗ VIOLATION: ev.* definition in $file"
      grep -E "$definition_pattern" "$file" | head -3
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ ev.* only defined in data-dictionary.md" || echo "✗ Found $violations SST violations"`

**References allowed**:
!`references=0
for file in docs/design/api-spec.md docs/design/data-flow-diagram.md docs/implementation/implementation-plan.md; do
  if [ -f "$file" ]; then
    refs=$(grep -o "ev\.[a-z._]*" "$file" 2>/dev/null | wc -l || echo 0)
    [ $refs -gt 0 ] && echo "✓ $file references $refs events" && ((references+=refs))
  fi
done
[ $references -gt 0 ] && echo "✓ Design/implementation docs reference ev.* (allowed)" || echo "⚠ No event references found"`

**Why**: Event schemas (telemetry, analytics) are defined in data-dictionary.md. Other docs track `ev.user.created`, not redefine event structure.

---

## Rule 6: DDL Statements → ONLY in Database Spec

**Authoritative Source**: `docs/design/database-spec.md`

**Validation**:
!`echo ""`
!`echo "=== DDL Validation ==="`
!`tables=$(grep -ci "CREATE TABLE" docs/design/database-spec.md 2>/dev/null || echo 0)
echo "CREATE TABLE statements in database-spec.md: $tables"`
[ $tables -gt 0 ] && echo "✓ DDL defined in database spec" || echo "⚠ No DDL in database spec"`

**Checking for violations** (CREATE TABLE outside database-spec):
!`violations=0
for file in docs/design/data-erd.md docs/design/data-catalog.md; do
  if [ -f "$file" ]; then
    if grep -qi "CREATE TABLE" "$file" 2>/dev/null; then
      echo "✗ VIOLATION: CREATE TABLE in $file"
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ DDL only in database-spec.md" || echo "✗ Found $violations SST violations"`

**Why**: DDL (Data Definition Language) belongs in database-spec.md. ERD shows relationships, data-catalog describes metadata, but only database-spec has `CREATE TABLE`.

---

## Rule 7: API Endpoint Schemas → ONLY in API Spec

**Authoritative Source**: `docs/design/api-spec.md`

**Validation**:
!`echo ""`
!`echo "=== API Schema Validation ==="`
!`api_endpoints=$(grep -E "^(GET|POST|PUT|DELETE|PATCH|OPTIONS) " docs/design/api-spec.md 2>/dev/null | wc -l || echo 0)
echo "API endpoints in api-spec.md: $api_endpoints"`
[ $api_endpoints -gt 0 ] && echo "✓ API endpoints defined" || echo "⚠ No API endpoints in api-spec"`

**Checking for violations** (request/response schemas outside api-spec):
!`violations=0
for file in docs/design/tech-spec.md docs/design/database-spec.md; do
  if [ -f "$file" ]; then
    # Check for JSON schema definitions (not references)
    if grep -E "^\{.*:.*\}$|^\"Request\":|^\"Response\":" "$file" 2>/dev/null | grep -v "api-spec" >/dev/null; then
      echo "⚠ Potential API schema in $file (should reference api-spec instead)"
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ API schemas only in api-spec.md" || echo "⚠ Found $violations potential violations"`

**Why**: Request/response schemas belong in api-spec.md. Tech specs and database specs should reference API endpoints, not duplicate schemas.

---

## Rule 8: Architecture Decisions → ONLY in Architecture Diagram

**Authoritative Source**: `docs/design/architecture-diagram.md`

**Validation**:
!`echo ""`
!`echo "=== Architecture Decision Validation ==="`
!`adrs=$(grep -o "ADR-[0-9]*" docs/design/architecture-diagram.md 2>/dev/null | sort -u | wc -l || echo 0)
echo "Architecture decisions in architecture-diagram.md: $adrs"`
[ $adrs -gt 0 ] && echo "✓ ADRs defined in architecture diagram" || echo "⚠ No ADRs in architecture diagram"`

**Checking for violations** (ADR-# definitions outside architecture-diagram):
!`violations=0
for file in docs/design/tech-spec.md docs/planning/prd.md; do
  if [ -f "$file" ]; then
    if grep -q "^ADR-[0-9]" "$file" 2>/dev/null; then
      echo "✗ VIOLATION: ADR definition in $file"
      ((violations++))
    fi
  fi
done
[ $violations -eq 0 ] && echo "✓ ADR-# only in architecture-diagram.md" || echo "✗ Found $violations SST violations"`

**Why**: Architecture decisions (ADR-#) are defined in architecture-diagram.md. Other docs reference decisions, not restate them.

---

## Rule 9: Business Objectives → ONLY in Product Vision (Discovery)

**Authoritative Source**: `docs/discovery/product-vision.md`

**Validation**:
!`echo ""`
!`echo "=== Business Objectives Validation ==="`
!`bos=$(grep -o "BO-[0-9]*" docs/discovery/product-vision.md 2>/dev/null | sort -u | wc -l || echo 0)
echo "Business objectives in product-vision.md: $bos"`
[ $bos -gt 0 ] && echo "✓ Business objectives defined in vision" || echo "⚠ No BO-# in product vision"`

**References allowed** (BO-# in other discovery/planning docs):
!`references=0
for file in docs/discovery/project-context.md docs/planning/prd.md; do
  if [ -f "$file" ]; then
    refs=$(grep -o "BO-[0-9]*" "$file" 2>/dev/null | wc -l || echo 0)
    [ $refs -gt 0 ] && echo "✓ $file references $refs business objectives" && ((references+=refs))
  fi
done
[ $references -gt 0 ] && echo "✓ Other docs reference BO-# (allowed)" || echo "⚠ No BO-# references found"`

**Why**: Business objectives (BO-#) are defined in product-vision.md. Planning and design docs reference them, showing traceability.

---

## Single Source of Truth Summary

!`echo ""`
!`echo "==================== SST COMPLIANCE SUMMARY ===================="`

**Total Violations**:
!`total_violations=0

# Count Given/When/Then violations
for file in docs/design/*.md docs/planning/prd.md docs/planning/feature-specs/*.md; do
  [ -f "$file" ] && grep -q "^Given\|^When\|^Then" "$file" 2>/dev/null && ((total_violations++))
done

# Count tok.* violations
for file in docs/design/wireframes.md docs/design/ux-sitemap.md docs/design/user-journey.md; do
  [ -f "$file" ] && grep -qE "tok\.[a-z._]*.*[:=]" "$file" 2>/dev/null && ((total_violations++))
done

# Count dict.* violations
for file in docs/design/data-erd.md docs/design/database-spec.md; do
  [ -f "$file" ] && grep -qE "dict\.[a-z._]*.*[:=]" "$file" 2>/dev/null && ((total_violations++))
done

# Count ev.* violations
for file in docs/design/api-spec.md docs/design/data-flow-diagram.md; do
  [ -f "$file" ] && grep -qE "ev\.[a-z._]*.*[:=]" "$file" 2>/dev/null && ((total_violations++))
done

# Count DDL violations
for file in docs/design/data-erd.md docs/design/data-catalog.md; do
  [ -f "$file" ] && grep -qi "CREATE TABLE" "$file" 2>/dev/null && ((total_violations++))
done

# Count API schema violations
for file in docs/design/tech-spec.md docs/design/database-spec.md; do
  [ -f "$file" ] && grep -qE "^\{.*:.*\}$|^\"Request\":|^\"Response\":" "$file" 2>/dev/null && ((total_violations++))
done

echo "Total SST violations found: $total_violations"

if [ $total_violations -eq 0 ]; then
  echo ""
  echo "✓✓✓ SINGLE SOURCE OF TRUTH: COMPLIANT ✓✓✓"
  echo ""
  echo "All definitions have exactly one authoritative source."
  echo "Other documents properly reference (not redefine) concepts."
else
  echo ""
  echo "✗✗✗ SINGLE SOURCE OF TRUTH: VIOLATIONS FOUND ✗✗✗"
  echo ""
  echo "Fix violations above to maintain SST compliance."
fi`

---

## SST Best Practices

!`echo ""`
!`echo "=== V3 SST Guidelines ==="`
!`echo ""`
!`echo "✓ DEFINE in authoritative source:"`
!`echo "  - Given/When/Then → docs/planning/user-stories.md"`
!`echo "  - NFR-# targets → docs/design/tech-spec.md"`
!`echo "  - tok.* tokens → docs/design/style-guide.md"`
!`echo "  - dict.* fields → docs/design/data-dictionary.md"`
!`echo "  - ev.* events → docs/design/data-dictionary.md"`
!`echo "  - CREATE TABLE → docs/design/database-spec.md"`
!`echo "  - API schemas → docs/design/api-spec.md"`
!`echo "  - ADR-# decisions → docs/design/architecture-diagram.md"`
!`echo "  - BO-# objectives → docs/discovery/product-vision.md"`
!`echo ""`
!`echo "✓ REFERENCE in all other docs:"`
!`echo "  - Use IDs: US-#, NFR-#, tok.color.primary, dict.user.email"`
!`echo "  - Link to sources: e.g., 'See BO-1 in product-vision.md'"`
!`echo "  - Don't restate: Copy values, paste definitions, duplicate schemas"`
!`echo ""`
!`echo "✗ NEVER:"`
!`echo "  - Define the same concept in multiple places"`
!`echo "  - Copy-paste definitions (they drift)"`
!`echo "  - Inline values without reference (updates break)"`
!`echo "  - Create duplicate schema definitions"`

---

**Single Source of Truth validation complete!**
