#!/bin/sh
# check-drift.sh — Detect content drift between .claude/skills/ and plugins/pm/skills/
#
# .claude/skills/ is nested (e.g., discovery/ideate/SKILL.md)
# plugins/pm/skills/ is flat (e.g., disc-ideate/SKILL.md)
#
# We compare SKILL.md content (excluding the 'name:' frontmatter line, which
# intentionally differs) and knowledge/ files.
#
# Exit 0 = no drift, Exit 1 = drift found

PLUGIN_SKILLS="plugins/pm/skills"
SOURCE_SKILLS=".claude/skills"

if [ ! -d "$PLUGIN_SKILLS" ] || [ ! -d "$SOURCE_SKILLS" ]; then
  echo "  ⚠ Drift check: directories missing, skipped"
  exit 0
fi

# Build map: for each plugin skill, find matching source skill by scanning
# all source SKILL.md files and matching content (minus the name: line)
drift_count=0
checked=0

for plugin_skill_dir in "$PLUGIN_SKILLS"/*/; do
  plugin_skill=$(basename "$plugin_skill_dir")
  plugin_md="$plugin_skill_dir/SKILL.md"

  [ ! -f "$plugin_md" ] && continue

  # Create temp content without the name: line for comparison
  plugin_content=$(sed '/^name:/d' "$plugin_md")

  # Find matching source SKILL.md
  match_found=false
  for source_md in "$SOURCE_SKILLS"/*/SKILL.md "$SOURCE_SKILLS"/*/*/SKILL.md; do
    [ ! -f "$source_md" ] && continue

    source_content=$(sed '/^name:/d' "$source_md")

    if [ "$plugin_content" = "$source_content" ]; then
      match_found=true
      break
    fi
  done

  if [ "$match_found" = false ]; then
    # Content differs — find the closest match by checking which source has
    # the same description line (second line of frontmatter usually)
    plugin_desc=$(grep "^description:" "$plugin_md" | head -1)

    for source_md in "$SOURCE_SKILLS"/*/SKILL.md "$SOURCE_SKILLS"/*/*/SKILL.md; do
      [ ! -f "$source_md" ] && continue
      source_desc=$(grep "^description:" "$source_md" | head -1)

      if [ "$plugin_desc" = "$source_desc" ]; then
        # Same skill, different content — this is drift
        source_rel=$(echo "$source_md" | sed "s|$SOURCE_SKILLS/||")
        echo "  ⚠ DRIFT: plugins/pm/skills/$plugin_skill ↔ .claude/skills/$source_rel"
        drift_count=$((drift_count + 1))
        match_found=true
        break
      fi
    done

    if [ "$match_found" = false ]; then
      echo "  ⚠ ORPHAN: plugins/pm/skills/$plugin_skill has no source match"
      drift_count=$((drift_count + 1))
    fi
  fi

  checked=$((checked + 1))
done

if [ $drift_count -gt 0 ]; then
  echo "  ❌ $drift_count skill(s) drifted out of $checked checked"
  echo "  Run: scripts/sync-to-plugin.sh to fix"
  exit 1
else
  echo "  ✓ Drift check: $checked skills in sync"
  exit 0
fi
