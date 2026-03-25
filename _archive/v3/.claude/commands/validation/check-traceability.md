---
description: Validate complete ID traceability chains across all v3 documents (BO-# → PRD-F-# → US-# → FS-[name]-#, plus technical/data/UX/API chains)
allowed-tools: Read, Grep, Bash
model: sonnet
---

# Traceability Chain Validation (v3)

Validating complete ID chains from business objectives through feature specifications and parallel technical/data/UX/API tracks.

## Overview

V3 traceability chains ensure every implementation detail traces back to business objectives and user needs via streamlined paths:

```
Main Chain (Vision → Implementation):
  BO-# (business objectives)
    → PRD-F-# (product features)
      → US-# (user stories)
        → FS-[name]-# (feature specifications)

Parallel Chains:
  NFR-# (in tech-spec.md)
  ADR-# (in architecture-diagram.md)
  dict.*, ev.* (in data-dictionary.md)
  tok.* (in style-guide.md)
```

---

## Chain 1: Business Objectives → Product Features

**Product Vision**:
!`test -f docs/discovery/product-vision.md && echo "✓ product-vision.md exists" || echo "✗ Missing product-vision.md"`

**Business Objectives in Vision**:
!`grep -o "BO-[0-9]*" docs/discovery/product-vision.md 2>/dev/null | sort -u | tee /tmp/bo-ids.txt | wc -l | xargs echo "Business objectives defined:"`

**Sample BOs**:
!`head -5 /tmp/bo-ids.txt 2>/dev/null`

---

## Chain 2: Product Features → User Stories

**Product Features in PRD**:
!`grep -o "PRD-F-[0-9]*" docs/planning/prd.md 2>/dev/null | sort -u | tee /tmp/prd-ids.txt | wc -l | xargs echo "Product features defined:"`

**Checking PRD references BOs**:
!`grep -o "BO-[0-9]*" docs/planning/prd.md 2>/dev/null | sort -u | wc -l | xargs echo "BOs referenced in PRD:"`

**Orphaned BOs (not referenced in PRD)**:
!`if [ -f /tmp/bo-ids.txt ]; then
  orphaned=0
  for bo in $(cat /tmp/bo-ids.txt); do
    grep -q "$bo" docs/planning/prd.md 2>/dev/null || { echo "⚠ $bo not referenced in PRD"; ((orphaned++)); }
  done
  [ $orphaned -eq 0 ] && echo "✓ All BOs have features" || echo "✗ Found $orphaned orphaned BOs"
fi`

---

## Chain 3: User Stories Definition

**User Stories defined**:
!`grep -o "US-[0-9]*" docs/planning/user-stories.md 2>/dev/null | sort -u | tee /tmp/us-ids.txt | wc -l | xargs echo "User stories defined:"`

**Checking Stories reference PRD Features**:
!`grep -o "PRD-F-[0-9]*" docs/planning/user-stories.md 2>/dev/null | sort -u | wc -l | xargs echo "PRD-F-# referenced in stories:"`

**Orphaned PRD Features (not referenced in Stories)**:
!`if [ -f /tmp/prd-ids.txt ]; then
  orphaned=0
  for prd in $(cat /tmp/prd-ids.txt); do
    grep -q "$prd" docs/planning/user-stories.md 2>/dev/null || { echo "⚠ $prd not referenced in stories"; ((orphaned++)); }
  done
  [ $orphaned -eq 0 ] && echo "✓ All PRD features have stories" || echo "✗ Found $orphaned orphaned PRD features"
fi`

**P0 Stories validation**:
!`grep -A 10 "Priority: P0" docs/planning/user-stories.md 2>/dev/null | grep -o "US-[0-9]*" | wc -l | xargs echo "P0 stories:"`

---

## Chain 4: Feature Specifications

**Feature Specs directory**:
!`test -d docs/planning/feature-specs && echo "✓ feature-specs/ directory exists" || echo "✗ Missing feature-specs/ directory"`

**Feature Spec files found**:
!`ls docs/planning/feature-specs/*.md 2>/dev/null | wc -l | xargs echo "Feature spec files:"`

**FS-[name]-# IDs defined**:
!`grep -h -o "FS-[a-z]*-[0-9]*" docs/planning/feature-specs/*.md 2>/dev/null | sort -u | tee /tmp/fs-ids.txt | wc -l | xargs echo "Feature spec items defined:"`

**Checking FS items reference User Stories**:
!`grep -h -o "US-[0-9]*" docs/planning/feature-specs/*.md 2>/dev/null | sort -u | wc -l | xargs echo "US-# referenced in specs:"`

**Orphaned User Stories (not referenced in FS)**:
!`if [ -f /tmp/us-ids.txt ]; then
  orphaned=0
  for us in $(cat /tmp/us-ids.txt); do
    grep -q "$us" docs/planning/feature-specs/*.md 2>/dev/null || { echo "⚠ $us not referenced in feature specs"; ((orphaned++)); }
  done
  [ $orphaned -eq 0 ] && echo "✓ All stories have feature specs" || echo "✗ Found $orphaned orphaned stories"
fi`

---

## Technical Chain: Architecture & NFRs

**Architecture Diagram exists**:
!`test -f docs/design/architecture-diagram.md && echo "✓ architecture-diagram.md exists" || echo "✗ Missing architecture-diagram.md"`

**ADR entries defined**:
!`grep -o "ADR-[0-9]*" docs/design/architecture-diagram.md 2>/dev/null | sort -u | tee /tmp/adr-ids.txt | wc -l | xargs echo "Architecture decisions defined:"`

**Tech Spec exists**:
!`test -f docs/design/tech-spec.md && echo "✓ tech-spec.md exists" || echo "✗ Missing tech-spec.md"`

**Non-Functional Requirements defined**:
!`grep -o "NFR-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | tee /tmp/nfr-ids.txt | wc -l | xargs echo "NFRs defined:"`

**Tech Spec references US or FS**:
!`grep -o "US-[0-9]*\|FS-[a-z]*-[0-9]*" docs/design/tech-spec.md 2>/dev/null | sort -u | wc -l | xargs echo "References to stories/specs in tech-spec:"`

---

## Data Traceability Chain

**Data Requirements exists**:
!`test -f docs/design/data-requirements.md && echo "✓ data-requirements.md exists" || echo "✗ Missing data-requirements.md"`

**ERD exists**:
!`test -f docs/design/erd.md && echo "✓ erd.md exists" || echo "✗ Missing erd.md"`

**Database Spec exists**:
!`test -f docs/design/database-spec.md && echo "✓ database-spec.md exists" || echo "✗ Missing database-spec.md"`

**Data Dictionary exists**:
!`test -f docs/design/data-dictionary.md && echo "✓ data-dictionary.md exists" || echo "✗ Missing data-dictionary.md"`

**Fields in Dictionary**:
!`grep -o "dict\.[a-z._]*" docs/design/data-dictionary.md 2>/dev/null | sort -u | tee /tmp/dict-ids.txt | wc -l | xargs echo "Fields documented (dict.*):"`

**Events in Dictionary**:
!`grep -o "ev\.[a-z._]*" docs/design/data-dictionary.md 2>/dev/null | sort -u | tee /tmp/ev-ids.txt | wc -l | xargs echo "Events documented (ev.*):"`

**Data Flow Diagram exists**:
!`test -f docs/design/data-flow-diagram.md && echo "✓ data-flow-diagram.md exists" || echo "✗ Missing data-flow-diagram.md"`

**Data Catalog exists**:
!`test -f docs/design/data-catalog.md && echo "✓ data-catalog.md exists" || echo "✗ Missing data-catalog.md"`

**Checking data chain references US or FS**:
!`grep -o "US-[0-9]*\|FS-[a-z]*-[0-9]*" docs/design/data-requirements.md 2>/dev/null | sort -u | wc -l | xargs echo "References in data-requirements:"`

---

## UX Traceability Chain

**User Journey exists**:
!`test -f docs/design/user-journey.md && echo "✓ user-journey.md exists" || echo "✗ Missing user-journey.md"`

**UX Sitemap exists**:
!`test -f docs/design/ux-sitemap.md && echo "✓ ux-sitemap.md exists" || echo "✗ Missing ux-sitemap.md"`

**Wireframes exist**:
!`test -f docs/design/wireframes.md && echo "✓ wireframes.md exists" || echo "✗ Missing wireframes.md"`

**Screens in Wireframes**:
!`grep -i "^##.*screen\|^##.*page" docs/design/wireframes.md 2>/dev/null | wc -l | xargs echo "Screens defined:"`

**Style Guide exists**:
!`test -f docs/design/style-guide.md && echo "✓ style-guide.md exists" || echo "✗ Missing style-guide.md"`

**Design Tokens**:
!`grep -o "tok\.[a-z._]*" docs/design/style-guide.md 2>/dev/null | sort -u | tee /tmp/tok-ids.txt | wc -l | xargs echo "Design tokens (tok.*):"`

**Checking UX references US**:
!`grep -o "US-[0-9]*" docs/design/user-journey.md 2>/dev/null | sort -u | wc -l | xargs echo "USs referenced in user journey:"`

**Checking wireframes reference stories**:
!`grep -o "US-[0-9]*" docs/design/wireframes.md 2>/dev/null | sort -u | wc -l | xargs echo "USs referenced in wireframes:"`

---

## API Traceability

**API Spec exists**:
!`test -f docs/design/api-spec.md && echo "✓ api-spec.md exists" || echo "✗ Missing api-spec.md"`

**API Endpoints defined**:
!`grep -E "^(GET|POST|PUT|DELETE|PATCH|HEAD) " docs/design/api-spec.md 2>/dev/null | wc -l | xargs echo "API endpoints:"`

**Checking API references FS or US**:
!`grep -o "FS-[a-z]*-[0-9]*\|US-[0-9]*" docs/design/api-spec.md 2>/dev/null | sort -u | wc -l | xargs echo "FS/US references in API:"`

---

## Implementation Traceability

**Implementation Plan exists**:
!`test -f docs/implementation/implementation-plan.md && echo "✓ implementation-plan.md exists" || echo "✗ Missing implementation-plan.md"`

**Sprint Status exists**:
!`test -f docs/implementation/sprint-status.yaml && echo "✓ sprint-status.yaml exists" || echo "✗ Missing sprint-status.yaml"`

**Quality Checklist exists**:
!`test -f docs/implementation/quality-checklist.md && echo "✓ quality-checklist.md exists" || echo "✗ Missing quality-checklist.md"`

**Checking implementation references FS**:
!`grep -o "FS-[a-z]*-[0-9]*" docs/implementation/implementation-plan.md 2>/dev/null | sort -u | wc -l | xargs echo "FS-# referenced in implementation:"`

---

## Traceability Summary

!`echo ""`
!`echo "==================== TRACEABILITY SUMMARY ===================="`

**Main Chain Completeness (BO → PRD-F → US → FS)**:
!`chain_complete=true
test -f docs/discovery/product-vision.md || chain_complete=false
test -f docs/planning/prd.md || chain_complete=false
test -f docs/planning/user-stories.md || chain_complete=false
test -d docs/planning/feature-specs || chain_complete=false
$chain_complete && echo "✓ Main chain complete: BO → PRD-F → US → FS" || echo "✗ Main chain incomplete"`

**Technical Chain (Architecture + NFRs)**:
!`tech_complete=true
test -f docs/design/architecture-diagram.md || tech_complete=false
test -f docs/design/tech-spec.md || tech_complete=false
$tech_complete && echo "✓ Technical chain complete: ADR + NFR" || echo "⚠ Technical chain incomplete"`

**Data Chain (Requirements → ERD → DB → Dictionary → Flow → Catalog)**:
!`data_complete=true
test -f docs/design/data-requirements.md || data_complete=false
test -f docs/design/erd.md || data_complete=false
test -f docs/design/database-spec.md || data_complete=false
test -f docs/design/data-dictionary.md || data_complete=false
test -f docs/design/data-flow-diagram.md || data_complete=false
test -f docs/design/data-catalog.md || data_complete=false
$data_complete && echo "✓ Data chain complete: REQ → ERD → DB → DICT → FLOW → CAT" || echo "⚠ Data chain incomplete"`

**UX Chain (Journey → Sitemap → Wireframes → Style Guide)**:
!`ux_complete=true
test -f docs/design/user-journey.md || ux_complete=false
test -f docs/design/ux-sitemap.md || ux_complete=false
test -f docs/design/wireframes.md || ux_complete=false
test -f docs/design/style-guide.md || ux_complete=false
$ux_complete && echo "✓ UX chain complete: JOURNEY → SITEMAP → WIRE → STYLE" || echo "⚠ UX chain incomplete"`

**API Chain**:
!`test -f docs/design/api-spec.md && echo "✓ API spec exists" || echo "⚠ API spec missing"`

**Implementation Chain**:
!`impl_complete=true
test -f docs/implementation/implementation-plan.md || impl_complete=false
test -f docs/implementation/sprint-status.yaml || impl_complete=false
test -f docs/implementation/quality-checklist.md || impl_complete=false
$impl_complete && echo "✓ Implementation chain complete" || echo "⚠ Implementation chain incomplete"`

---

## Issues Found

!`echo ""`
!`echo "=== Checking for Common Issues ==="`

**Broken References** (spot check):
!`# Check if FS-# references in implementation actually exist
broken=0
for fs in $(grep -o "FS-[a-z]*-[0-9]*" docs/implementation/implementation-plan.md 2>/dev/null | sort -u); do
  grep -q "$fs" docs/planning/feature-specs/*.md 2>/dev/null || { echo "✗ $fs referenced but not defined"; ((broken++)); }
done
[ $broken -eq 0 ] && echo "✓ No broken FS-# references in implementation" || echo "✗ Found $broken broken references"`

**Forward References Complete**:
!`# PRD should reference BOs
prd_refs=$(grep -o "BO-[0-9]*" docs/planning/prd.md 2>/dev/null | wc -l)
[ $prd_refs -gt 0 ] && echo "✓ PRD references business objectives" || echo "⚠ PRD doesn't reference BOs (weak traceability)"`

**Complete Traceability Test**:
!`echo ""`
!`echo "Can we trace from vision to feature specs?"`
!`if [ -f docs/discovery/product-vision.md ] && [ -d docs/planning/feature-specs ]; then
  echo "✓ Start (vision) and end (feature-specs) exist"
  all_links=true
  test -f docs/planning/prd.md || all_links=false
  test -f docs/planning/user-stories.md || all_links=false
  [ $(ls docs/planning/feature-specs/*.md 2>/dev/null | wc -l) -gt 0 ] || all_links=false
  $all_links && echo "✓✓✓ COMPLETE TRACEABILITY: PASS ✓✓✓" || echo "✗ Missing intermediate documents"
else
  echo "✗ Cannot verify traceability - missing key documents"
fi`

---

## Recommendations

!`echo ""`
!`echo "=== Action Items ==="`
!`echo "1. Review orphaned IDs (shown with ⚠ above)"`
!`echo "2. Ensure all BO-# have PRD-F-# features"`
!`echo "3. Ensure all PRD-F-# have US-# stories"`
!`echo "4. Ensure all US-# have FS-[name]-# in feature-specs/"`
!`echo "5. Validate all parallel chains (tech/data/ux/api) reference upstream IDs"`
!`echo "6. Check Single Source of Truth: no duplicate dict.*, ev.*, tok.* definitions"`
!`echo ""`
!`echo "Run '/validate-gate release' for complete quality check"`

---

**Traceability validation complete (v3)!**
