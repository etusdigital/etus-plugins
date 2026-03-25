#!/bin/bash

# Post-Document-Save Hook
# Validates Single Source of Truth (SST) compliance when documents are saved
# Runs after Write or Edit tool saves a file
# Issues warnings but never blocks saves (exit 0 always)

set +e  # Continue on errors

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Counters
WARNINGS=0

# Resolve file path from arg or hook JSON on stdin.
RAW_INPUT="$(cat 2>/dev/null)"
FILEPATH="$1"

if [[ -z "$FILEPATH" && -n "$RAW_INPUT" ]]; then
  FILEPATH="$(RAW_INPUT="$RAW_INPUT" python3 - <<'PY'
import json, os
raw = os.environ.get("RAW_INPUT", "").strip()
if not raw:
    print("")
    raise SystemExit
try:
    event = json.loads(raw)
except Exception:
    print("")
    raise SystemExit
tool_input = event.get("tool_input", {})
print(tool_input.get("file_path") or tool_input.get("path") or "")
PY
)"
fi

# Check if we're in a docs directory (skip if not)
if [[ ! "$FILEPATH" =~ ^docs/ ]] && [[ ! "$FILEPATH" =~ ^implementation/ ]] && [[ ! "$FILEPATH" =~ /docs/ ]]; then
  exit 0
fi

FILENAME=$(basename "$FILEPATH")

# Echo warnings header
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "SST Validation Hook: $FILENAME"
echo "════════════════════════════════════════════════════════════════"

# ============================================================================
# RULE 1: "Given/When/Then" only in user-stories.md
# ============================================================================
if [[ "$FILENAME" != "user-stories.md" ]]; then
  if grep -q "Given.*When.*Then" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 1)${NC}: Found 'Given/When/Then' in non-user-stories document"
    echo "    File: $FILEPATH"
    echo "    Rule: Acceptance criteria belong ONLY in user-stories.md"
    echo "    Action: Move acceptance criteria to user-stories.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 2: "NFR-" definitions only in tech-spec.md
# ============================================================================
if [[ "$FILENAME" != "tech-spec.md" ]]; then
  if grep -q "^NFR-[0-9]\+" "$FILEPATH" 2>/dev/null || \
     grep -q "Non-Functional Requirement" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 2)${NC}: Found 'NFR-#' or 'Non-Functional Requirement' in non-tech-spec document"
    echo "    File: $FILEPATH"
    echo "    Rule: NFR definitions belong ONLY in tech-spec.md"
    echo "    Action: Move NFR definitions to tech-spec.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 3: "dict." definitions only in data-dictionary.md
# ============================================================================
if [[ "$FILENAME" != "data-dictionary.md" ]]; then
  if grep -q "dict\.[a-z_]*\.[a-z_]*" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 3)${NC}: Found 'dict.[domain].[field]' references in non-data-dictionary document"
    echo "    File: $FILEPATH"
    echo "    Rule: Data field definitions belong ONLY in data-dictionary.md"
    echo "    Note: References are ok, but definitions belong in data-dictionary.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 4: "ev." definitions only in data-dictionary.md
# ============================================================================
if [[ "$FILENAME" != "data-dictionary.md" ]]; then
  if grep -q "ev\.[a-z_]*\.[a-z_]*" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 4)${NC}: Found 'ev.[domain].[action]' references in non-data-dictionary document"
    echo "    File: $FILEPATH"
    echo "    Rule: Event definitions belong ONLY in data-dictionary.md"
    echo "    Note: References are ok, but definitions belong in data-dictionary.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 5: "tok." definitions only in style-guide.md
# ============================================================================
if [[ "$FILENAME" != "style-guide.md" ]]; then
  if grep -q "tok\.[a-z_]*\.[a-z_]*" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 5)${NC}: Found 'tok.[category].[name]' references in non-style-guide document"
    echo "    File: $FILEPATH"
    echo "    Rule: Design token definitions belong ONLY in style-guide.md"
    echo "    Note: References (in wireframes, etc) are ok, but definitions belong in style-guide.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 6: "CREATE TABLE" statements only in database-spec.md
# ============================================================================
if [[ "$FILENAME" != "database-spec.md" ]]; then
  if grep -q "CREATE TABLE" "$FILEPATH" 2>/dev/null || \
     grep -q "^CREATE " "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 6)${NC}: Found SQL DDL statements in non-database-spec document"
    echo "    File: $FILEPATH"
    echo "    Rule: DDL statements belong ONLY in database-spec.md"
    echo "    Action: Move CREATE TABLE, ALTER TABLE, etc. to database-spec.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 7: API schemas only in api-spec.md
# ============================================================================
if [[ "$FILENAME" != "api-spec.md" ]]; then
  if grep -q "GET\|POST\|PUT\|PATCH\|DELETE" "$FILEPATH" 2>/dev/null && \
     grep -q "Request:\|Response:\|parameters:" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 7)${NC}: Found API endpoint definitions in non-api-spec document"
    echo "    File: $FILEPATH"
    echo "    Rule: API endpoint schemas belong ONLY in api-spec.md"
    echo "    Note: References (in planning, etc) are ok, but full schemas belong in api-spec.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# RULE 8: Architecture Decisions only in tech-spec.md
# ============================================================================
if [[ "$FILENAME" != "tech-spec.md" ]]; then
  if grep -q "ADR-[0-9]\+" "$FILEPATH" 2>/dev/null || \
     grep -q "Architecture Decision" "$FILEPATH" 2>/dev/null; then
    echo ""
    echo -e "${RED}⚠️  WARNING (SST Rule 8)${NC}: Found 'ADR-#' or 'Architecture Decision' in non-tech-spec document"
    echo "    File: $FILEPATH"
    echo "    Rule: ADRs belong ONLY in tech-spec.md"
    echo "    Action: Move ADRs to tech-spec.md"
    ((WARNINGS++))
  fi
fi

# ============================================================================
# Summary
# ============================================================================
echo ""
if [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✓ SST Validation: All rules passed${NC}"
else
  echo -e "${YELLOW}✓ Document saved (${WARNINGS} SST warnings)${NC}"
  echo ""
  echo "Warnings are informational. Fix at next opportunity."
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Always exit 0 — hooks warn but never block
exit 0
