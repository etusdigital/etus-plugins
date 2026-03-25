---
description: Refine existing product vision with additional context and HMW statements
argument-hint: [feedback-or-context]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Refine Product Vision

Iterate on existing product vision document with additional context, feedback, or insights.

## Overview

This command helps you improve an existing vision by:
- Adding new insights from user research or market feedback
- Refining problem statements with deeper 5W2H analysis
- Expanding How Might We (HMW) opportunities
- Updating North Star Metric targets based on new data
- Incorporating stakeholder feedback
- Strengthening evidence base (Evidence-based)

## Prerequisites

!`test -f docs/discovery/product-vision.md && echo "✓ product-vision.md exists" || echo "✗ Missing product-vision.md - run /vision first"`

!`if [ -f docs/discovery/product-vision.md ]; then
  grep -o "BO-[0-9]*" docs/discovery/product-vision.md | wc -l | xargs echo "Current business objectives:"
  grep -qi "North Star Metric" docs/discovery/product-vision.md && echo "✓ NSM defined"
  grep -c "5W2H" docs/discovery/product-vision.md | xargs echo "5W2H analyses:"
fi`

## Gather Current Context

Reading existing vision for refinement...

!`if [ -f docs/discovery/product-vision.md ]; then
  echo "=== Current Vision Summary ==="
  head -50 docs/discovery/product-vision.md | tail -40
fi`

## Refinement Context

**Feedback/Context**: $ARGUMENTS

Common refinement scenarios:
1. **User Research Findings**: New pain points discovered
2. **Competitive Analysis**: Market positioning changes
3. **Stakeholder Feedback**: Executive input on priorities
4. **Metric Updates**: Baseline data now available
5. **Scope Changes**: Must features need adjustment
6. **HMW Expansion**: New opportunity areas identified

## Invoke Vision Refinement

Using feature-development-chain skill with iteration mode to:
- Re-analyze problem with updated 5W2H framework
- Incorporate new evidence and data points
- Refine HMW statements based on feedback
- Update NSM targets if baseline changed
- Strengthen business objectives with new insights
- Maintain traceability to existing BO-# IDs

**Refining vision with context: "$ARGUMENTS"**

The skill will:
1. **Read** current product-vision.md
2. **Analyze** feedback/context provided
3. **Apply** 5W2H to new insights
4. **Generate** updated HMW statements
5. **Preserve** existing BO-# IDs (or create new ones)
6. **Update** NSM if baseline/target changed
7. **Write** refined product-vision.md

## Validation

After refinement:

!`if [ -f docs/discovery/product-vision.md ]; then
  echo "✓ Vision refined"
  grep -o "BO-[0-9]*" docs/discovery/product-vision.md | sort -u | wc -l | xargs echo "Business objectives:"
  grep -qi "North Star Metric" docs/discovery/product-vision.md && echo "✓ NSM present"

  # Check 5W2H coverage
  coverage=0
  for element in WHAT WHO WHERE WHEN WHY HOW "HOW MUCH"; do
    grep -qi "$element" docs/discovery/product-vision.md && ((coverage++))
  done
  echo "5W2H coverage: $coverage/7"

  # Check HMW statements
  grep -c "How might we\\|HMW" docs/discovery/product-vision.md | xargs echo "HMW statements:"

  # Check evidence
  grep -c "Evidence:\\|Data:\\|Research:" docs/discovery/product-vision.md | xargs echo "Evidence citations:"
fi`

## Compare Changes

To see what changed:

!`if [ -f docs/discovery/product-vision.md.backup ]; then
  echo "=== Changes from previous version ==="
  diff -u docs/discovery/product-vision.md.backup docs/discovery/product-vision.md | head -30
else
  echo "⚠ No backup found - first refinement"
fi`

## Gate Check

Verify vision still passes Discover Gate:

!`echo "Checking Discover Gate criteria..."`

!`if [ -f docs/discovery/product-vision.md ]; then
  # Check 5W2H coverage (need 7/7)
  count=0
  grep -i "WHAT" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHO" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHERE" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHEN" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "WHY" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "HOW" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))
  grep -i "HOW MUCH" docs/discovery/product-vision.md >/dev/null 2>&1 && ((count++))

  if [ $count -eq 7 ]; then
    echo "✓ PASS: 5W2H coverage complete (7/7)"
  else
    echo "⚠ WARNING: 5W2H coverage incomplete ($count/7)"
  fi

  # Check NSM
  grep -qi "North Star Metric.*baseline.*target" docs/discovery/product-vision.md
  if [ $? -eq 0 ]; then
    echo "✓ PASS: NSM with baseline/target/window"
  else
    echo "⚠ WARNING: NSM incomplete"
  fi

  # Check Must features
  must_count=$(grep -ci "MUST" docs/discovery/product-vision.md)
  if [ $must_count -ge 3 ] && [ $must_count -le 5 ]; then
    echo "✓ PASS: 3-5 Must features identified ($must_count)"
  else
    echo "⚠ WARNING: Must features should be 3-5 (found: $must_count)"
  fi
fi`

## Refinement Impact Analysis

Check if refinement affects downstream documents:

!`echo "=== Downstream Impact Assessment ==="`

!`if [ -f docs/planning/prd.md ]; then
  echo "⚠ PRD exists - verify BO-# references still valid"
  grep -o "BO-[0-9]*" docs/planning/prd.md | sort -u | xargs echo "PRD references:"
fi`

!`if [ -f docs/planning/user-stories.md ]; then
  echo "⚠ Stories exist - verify alignment with refined vision"
fi`

## Next Steps

**Downstream Updates**:
If vision changed significantly, consider updating:
```
/prd               # Update product requirements
/validate-gate discover  # Re-validate Discover gate
```

**Continue workflow**:
```
/define            # Proceed with Define phase
/check-traceability  # Verify BO-# links still valid
```

**Further refinement**:
```
/refine-vision "additional feedback or context"
```

---

**Vision refinement complete!** Review changes and update downstream documents if needed.
