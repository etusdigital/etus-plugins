#!/bin/sh
# check-changeset.sh — Require a changeset when release-relevant files change.
#
# Release-relevant = anything in plugins/, .claude/skills/, .claude/agents/,
# .claude/commands/, .claude/hooks/, or .claude-plugin/
#
# Exit 0 = no changeset needed or changeset exists, Exit 1 = missing changeset

# Get staged files
staged=$(git diff --cached --name-only 2>/dev/null)

if [ -z "$staged" ]; then
  exit 0
fi

# Check if any staged file is release-relevant
release_relevant=false
for file in $staged; do
  case "$file" in
    plugins/*|.claude/skills/*|.claude/agents/*|.claude/commands/*|.claude/hooks/*|.claude-plugin/*)
      release_relevant=true
      break
      ;;
  esac
done

if [ "$release_relevant" = false ]; then
  # No release-relevant files changed — changeset not required
  exit 0
fi

# Check if there's at least one changeset file (not README or config)
changeset_count=$(ls .changeset/*.md 2>/dev/null | grep -v README.md | wc -l | tr -d ' ')

if [ "$changeset_count" -eq 0 ]; then
  echo ""
  echo "  ⚠ Release-relevant files changed but no changeset found."
  echo "  Run: npx changeset"
  echo "  Then stage the generated .changeset/*.md file."
  echo ""
  echo "  Changed release-relevant files:"
  for file in $staged; do
    case "$file" in
      plugins/*|.claude/skills/*|.claude/agents/*|.claude/commands/*|.claude/hooks/*|.claude-plugin/*)
        echo "    - $file"
        ;;
    esac
  done
  echo ""
  echo "  To skip (hotfix): git commit --no-verify"
  exit 1
fi

echo "  ✓ Changeset exists ($changeset_count pending)"
exit 0
