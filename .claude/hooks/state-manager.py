#!/usr/bin/env python3
"""
state-manager.py — explicit bootstrap helpers for ETUS state files.

Usage:
  python3 .claude/hooks/state-manager.py init-project <project-slug> [execution_adapter] [mode]
  python3 .claude/hooks/state-manager.py ensure-feature <project-slug> <feature-slug> [execution_adapter] [title]
  python3 .claude/hooks/state-manager.py sync-cycle <project-slug> <cycle-id> [cycle-name] [state] [start] [end] [story-ids] [task-ids]
"""

from __future__ import annotations

import os
import sys

from state_utils import ensure_feature_state, ensure_project_state, sync_linear_cycle


HELP = """
state-manager.py

Commands:
  init-project <project-slug> [execution_adapter] [mode]
      Create docs/ets/projects/<project-slug>/... plus state files.
      execution_adapter: none | local | linear (default: none)
      mode: product | feature | bug | spike (default: product)

  ensure-feature <project-slug> <feature-slug> [execution_adapter] [title]
      Ensure feature folder and feature-status.md exist.

  sync-cycle <project-slug> <cycle-id> [cycle-name] [state] [start] [end] [story-ids] [task-ids]
      Project a Linear cycle into docs/ets/projects/<project-slug>/state/.
      story-ids and task-ids are comma-separated.
"""


def cmd_init_project(args: list[str]) -> int:
    if not args:
        print("Usage: init-project <project-slug> [execution_adapter] [mode]", file=sys.stderr)
        return 1
    project_slug = args[0]
    execution_adapter = args[1] if len(args) > 1 else "none"
    mode = args[2] if len(args) > 2 else "product"
    ensure_project_state(os.getcwd(), project_slug, execution_adapter=execution_adapter, mode=mode)
    print(f"✓ Project state initialized: docs/ets/projects/{project_slug}/state/")
    return 0


def cmd_ensure_feature(args: list[str]) -> int:
    if len(args) < 2:
        print("Usage: ensure-feature <project-slug> <feature-slug> [execution_adapter] [title]", file=sys.stderr)
        return 1
    project_slug = args[0]
    feature_slug = args[1]
    execution_adapter = args[2] if len(args) > 2 else "none"
    title = args[3] if len(args) > 3 else None
    path = ensure_feature_state(
        os.getcwd(),
        project_slug,
        feature_slug,
        execution_adapter=execution_adapter,
        title=title,
    )
    print(f"✓ Feature state ensured: {path}")
    return 0


def cmd_sync_cycle(args: list[str]) -> int:
    if len(args) < 2:
        print(
            "Usage: sync-cycle <project-slug> <cycle-id> [cycle-name] [state] [start] [end] [story-ids] [task-ids]",
            file=sys.stderr,
        )
        return 1
    project_slug = args[0]
    cycle_id = args[1]
    cycle_name = args[2] if len(args) > 2 else ""
    state = args[3] if len(args) > 3 else "active"
    start = args[4] if len(args) > 4 else ""
    end = args[5] if len(args) > 5 else ""
    story_ids = [item.strip() for item in (args[6] if len(args) > 6 else "").split(",") if item.strip()]
    task_ids = [item.strip() for item in (args[7] if len(args) > 7 else "").split(",") if item.strip()]
    path = sync_linear_cycle(
        os.getcwd(),
        project_slug,
        cycle_id,
        cycle_name=cycle_name,
        state=state,
        start=start,
        end=end,
        story_ids=story_ids,
        task_ids=task_ids,
    )
    print(f"✓ Linear cycle projected locally: {path}")
    return 0


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print(HELP.strip())
        return 0

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "init-project":
        return cmd_init_project(args)
    if command == "ensure-feature":
        return cmd_ensure_feature(args)
    if command == "sync-cycle":
        return cmd_sync_cycle(args)

    print(f"Unknown command: {command}", file=sys.stderr)
    print(HELP.strip(), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
