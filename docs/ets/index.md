# ETUS Workspace

This is the canonical document root for the ETUS documentation operating system.

## Structure

- `catalog/` — cross-project indexes
- `projects/{project-slug}/` — project-specific artifacts and state
- `schemas/` — JSON schemas for YAML frontmatter and state files

## Principles

- **Documentation Core** — Markdown in `projects/{project-slug}/...` is the canonical semantic context.
- **Workflow State** — YAML in `projects/{project-slug}/state/...` is the canonical progress and gate state.
- **Execution Adapter** — optional state files may exist under `state/` when an execution system is enabled.
- SQLite indexes and mirrors documents for search, memory, and fast lookups.
