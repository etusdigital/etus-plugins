#!/usr/bin/env python3
"""
memory-init.py — Initializes (or migrates) the ETUS PMDocs persistent memory system.

Usage:
  python3 .claude/hooks/memory-init.py           # init/upgrade only
  python3 .claude/hooks/memory-init.py --migrate  # also import existing .md files into SQLite

Idempotent: safe to run multiple times. Uses CREATE TABLE IF NOT EXISTS and
INSERT OR IGNORE for migration, so existing data is never overwritten.
"""

import sqlite3
import os
import sys
import json
import re
import tempfile
from datetime import datetime, timezone
from path_utils import project_root_from, resolve_memory_dir, split_ets_path

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
import hashlib as _hashlib

PROJECT_ROOT  = project_root_from(__file__)
MEMORY_DIR    = resolve_memory_dir(PROJECT_ROOT)   # markdown views

# SQLite DB lives on the LOCAL filesystem (not virtiofs/FUSE, which blocks file locking).
# Keyed by a hash of the project path so multiple projects don't collide.
_project_hash = _hashlib.md5(PROJECT_ROOT.encode()).hexdigest()[:8]
LOCAL_DB_DIR  = os.path.expanduser("~/.claude/etus-memory")
DB_PATH       = os.path.join(LOCAL_DB_DIR, f"memory-{_project_hash}.db")

SCHEMA_VERSION = 1   # bump when making breaking schema changes


# ─────────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────────
DDL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Schema version tracker
CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Every document ever saved in docs/ets/
CREATE TABLE IF NOT EXISTS documents (
    path            TEXT PRIMARY KEY,   -- relative path from project root
    filename        TEXT NOT NULL,
    phase           TEXT,               -- discovery | planning | design | implementation | feature | bug | spike
    mode            TEXT,               -- product | feature | bug | spike
    doc_type        TEXT,               -- project-context | prd | user-stories | …
    status          TEXT DEFAULT 'draft',  -- draft | complete
    ids_generated   TEXT DEFAULT '[]', -- JSON array: ["BO-1","BO-2"]
    created_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- Current project state — singleton row (id always = 1)
CREATE TABLE IF NOT EXISTS project_state (
    id              INTEGER PRIMARY KEY CHECK (id = 1),
    current_phase   TEXT DEFAULT 'not started',
    current_mode    TEXT DEFAULT 'not set',
    last_document   TEXT,
    last_activity   TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    next_step       TEXT DEFAULT 'Run /start-project to begin'
);

-- Decisions log
CREATE TABLE IF NOT EXISTS decisions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    decision        TEXT NOT NULL,
    rationale       TEXT,
    source_skill    TEXT,
    phase           TEXT,
    tags            TEXT DEFAULT '[]',  -- JSON array
    status          TEXT DEFAULT 'active',  -- active | superseded | revoked
    created_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- User & team preferences
CREATE TABLE IF NOT EXISTS preferences (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    preference      TEXT NOT NULL,
    source_skill    TEXT,
    category        TEXT,   -- docs | naming | style | process | other
    created_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- Recurring patterns
CREATE TABLE IF NOT EXISTS patterns (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern         TEXT NOT NULL,
    source_skill    TEXT,
    applies_to      TEXT DEFAULT 'all',  -- all | discovery | planning | design | implementation | feature | bug | spike
    created_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- Linear issue mapping (ETUS IDs ↔ Linear IDs)
CREATE TABLE IF NOT EXISTS linear_mapping (
    etus_id         TEXT PRIMARY KEY,   -- BO-1, US-3, impl-7, FB-2, etc.
    linear_id       TEXT NOT NULL,      -- LIN-###
    title           TEXT,
    type            TEXT,               -- story | task | bug | feature
    status          TEXT,
    created_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at      TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
"""


# ─────────────────────────────────────────────────────────────────────────────
# Path → metadata detection
# ─────────────────────────────────────────────────────────────────────────────
# Maps path patterns to (phase, mode, doc_type)
PATH_MAP = [
    (r"state/reports/discovery\.json$",         "discovery",      "product",        "report-discovery"),
    (r"state/reports/opportunities\.json$",     "planning",       "product",        "report-opportunities"),
    (r"state/reports/solution-report\.json$",   "planning",       "product",        "report-solution"),
    (r"state/reports/planning\.json$",          "planning",       "product",        "report-planning"),
    (r"state/reports/design\.json$",            "design",         "product",        "report-design"),
    (r"state/reports/implementation\.json$",    "implementation", "product",        "report-implementation"),
    # Feature mode documents
    (r"features/[^/]+/solution-discovery\.md$",    "feature",        "feature",        "solution-discovery"),
    (r"features/[^/]+/feature-status\.md$",        "feature",        "feature",        "feature-status"),
    (r"features/[^/]+/feature-brief\.md$",         "feature",        "feature",        "feature-brief"),
    (r"features/[^/]+/user-stories\.md$",          "feature",        "feature",        "user-stories"),
    (r"features/[^/]+/design-delta\.md$",          "feature",        "feature",        "design-delta"),
    (r"features/[^/]+/impl-plan\.md$",             "feature",        "feature",        "impl-plan"),
    (r"features/feature-brief-(.+)\.md$",     "feature",        "feature",        "feature-brief"),
    (r"features/user-stories-(.+)\.md$",      "feature",        "feature",        "user-stories"),
    (r"features/design-delta-(.+)\.md$",      "feature",        "feature",        "design-delta"),
    (r"features/impl-plan-(.+)\.md$",         "feature",        "feature",        "impl-plan"),
    # Bug mode
    (r"bugs/tech-spec-(.+)\.md$",             "bug",            "bug",            "tech-spec-bug"),
    # Spike mode
    (r"spikes/spike-(.+)\.md$",               "spike",          "spike",          "spike"),
    # Product mode — discovery
    (r"state/project-status\.yaml$",           "state",          "system",         "project-status"),
    (r"state/workflow-state\.yaml$",           "state",          "system",         "workflow-state"),
    (r"state/coverage-matrix\.yaml$",          "discovery",      "product",        "coverage-matrix"),
    (r"state/feature-index\.yaml$",            "state",          "system",         "feature-index"),
    (r"state/execution-status\.yaml$",         "state",          "system",         "execution-status"),
    (r"state/execution-sync\.yaml$",           "state",          "system",         "execution-sync"),
    (r"state/features/[^/]+\.yaml$",           "feature",        "feature",        "feature-state"),
    (r"discovery/project-context\.md$",       "discovery",      "product",        "project-context"),
    (r"discovery/opportunity-pack\.md$",      "discovery",      "product",        "opportunity-pack"),
    (r"discovery/baseline\.md$",              "discovery",      "product",        "baseline"),
    (r"discovery/discovery-report\.md$",      "discovery",      "product",        "discovery-report"),
    (r"discovery/product-vision\.md$",        "discovery",      "product",        "product-vision"),
    # Product mode — planning
    (r"planning/ost\.md$",                    "planning",       "product",        "ost"),
    (r"planning/prioritization\.md$",         "planning",       "product",        "prioritization"),
    (r"planning/solution-discovery\.md$",     "planning",       "product",        "solution-discovery"),
    (r"planning/solution-experiments\.yaml$", "planning",       "product",        "solution-experiments"),
    (r"planning/prd\.md$",                    "planning",       "product",        "prd"),
    (r"planning/user-stories\.md$",           "planning",       "product",        "user-stories"),
    (r"planning/feature-specs/",              "planning",       "product",        "feature-spec"),
    # Product mode — architecture
    (r"architecture/architecture-diagram\.md$","design",        "product",        "architecture-diagram"),
    (r"architecture/tech-spec\.md$",          "design",         "product",        "tech-spec"),
    # Product mode — data design
    (r"data/data-requirements\.md$",          "design",         "product",        "data-requirements"),
    (r"data/erd\.md$",                        "design",         "product",        "erd"),
    (r"data/database-spec\.md$",              "design",         "product",        "database-spec"),
    (r"data/data-dictionary\.md$",            "design",         "product",        "data-dictionary"),
    (r"data/data-flow-diagram\.md$",          "design",         "product",        "data-flow-diagram"),
    (r"data/data-catalog\.md$",              "design",         "product",        "data-catalog"),
    # Product mode — UX design
    (r"ux/user-journey\.md$",                 "design",         "product",        "user-journey"),
    (r"ux/ux-sitemap\.md$",                   "design",         "product",        "ux-sitemap"),
    (r"ux/wireframes\.md$",                   "design",         "product",        "wireframes"),
    (r"ux/style-guide\.md$",                  "design",         "product",        "style-guide"),
    # Product mode — implementation
    (r"implementation/api-spec\.md$",         "implementation", "product",        "api-spec"),
    (r"implementation/implementation-plan\.md$","implementation","product",       "implementation-plan"),
    (r"implementation/quality-checklist\.md$","implementation", "product",        "quality-checklist"),
    (r"implementation/release-plan\.md$",     "implementation", "product",        "release-plan"),
    # ── Repo-level docs (outside docs/ets/) ──
    # These are reference/design documents that live in docs/ but aren't part of the ETUS pipeline.
    (r"docs/design/",                         "repo",           "reference",      "design-doc"),
    (r"docs/plans/",                          "repo",           "reference",      "plan-doc"),
    (r"docs/design-notes/",                   "repo",           "reference",      "design-note"),
    (r"docs/[^/]+\.md$",                      "repo",           "reference",      "repo-doc"),
]

def detect_metadata(path: str) -> tuple:
    """Return (phase, mode, doc_type) for docs/ets/ relative path."""
    info = split_ets_path(path)
    inner_path = info.inner_path
    for pattern, phase, mode, doc_type in PATH_MAP:
        if re.search(pattern, inner_path):
            return phase, mode, doc_type
    return "unknown", "unknown", os.path.basename(path).replace(".md", "")


# ─────────────────────────────────────────────────────────────────────────────
# Markdown view generators
# ─────────────────────────────────────────────────────────────────────────────

def render_project_state(conn) -> str:
    state = conn.execute("SELECT * FROM project_state WHERE id=1").fetchone()
    docs  = conn.execute(
        "SELECT path, doc_type, phase, status, updated_at FROM documents ORDER BY updated_at DESC"
    ).fetchall()

    mode  = state["current_mode"]  if state else "not set"
    phase = state["current_phase"] if state else "not started"
    last  = state["last_document"] if state else "(none)"
    next_ = state["next_step"]     if state else "Run /start-project to begin"
    ts    = state["last_activity"] if state else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build completed docs list
    doc_lines = ""
    if docs:
        for d in docs:
            doc_lines += f"- `{d['path']}` — {d['doc_type']} ({d['status']}) — {d['updated_at'][:10]}\n"
    else:
        doc_lines = "(none yet)\n"

    # Mode-aware phase table
    if mode in ("feature",):
        phase_table = (
            "| Step | Status | Last Activity |\n"
            "|------|--------|---------------|\n"
        )
        for step in ["solution-discovery", "feature-brief", "user-stories", "design-delta", "impl-plan"]:
            row = conn.execute(
                "SELECT status, updated_at FROM documents WHERE doc_type=? AND mode='feature' ORDER BY updated_at DESC LIMIT 1",
                (step,)
            ).fetchone()
            status = row["status"] if row else "not started"
            ts_row = row["updated_at"][:10] if row else "—"
            phase_table += f"| {step} | {status} | {ts_row} |\n"
    elif mode == "bug":
        phase_table = (
            "| Step | Status | Last Activity |\n"
            "|------|--------|---------------|\n"
        )
        row = conn.execute(
            "SELECT status, updated_at FROM documents WHERE mode='bug' ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        status = row["status"] if row else "not started"
        ts_row = row["updated_at"][:10] if row else "—"
        phase_table += f"| tech-spec (bug) | {status} | {ts_row} |\n"
    elif mode == "spike":
        phase_table = (
            "| Step | Status | Last Activity |\n"
            "|------|--------|---------------|\n"
        )
        row = conn.execute(
            "SELECT status, updated_at FROM documents WHERE mode='spike' ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        status = row["status"] if row else "not started"
        ts_row = row["updated_at"][:10] if row else "—"
        phase_table += f"| spike doc | {status} | {ts_row} |\n"
    else:  # product or not set
        phase_table = (
            "| Phase | Status | Last Activity |\n"
            "|-------|--------|---------------|\n"
        )
        for p in ["discovery", "planning", "design", "implementation"]:
            rows = conn.execute(
                "SELECT status, updated_at FROM documents WHERE phase=? ORDER BY updated_at DESC LIMIT 1", (p,)
            ).fetchone()
            status = rows["status"] if rows else "not started"
            ts_row = rows["updated_at"][:10] if rows else "—"
            phase_table += f"| {p.capitalize()} | {status} | {ts_row} |\n"

    return f"""# Project State
<!-- AUTO-GENERATED by memory-sync.py — do not edit directly. Source of truth: memory.db -->

**Last updated:** {ts}
**Current phase:** {phase}
**Current mode:** {mode}

## Phase Status

{phase_table}
## Documents Completed

{doc_lines}
## Next Step

{next_}
"""


def render_decisions(conn) -> str:
    rows = conn.execute(
        "SELECT id, decision, rationale, source_skill, phase, tags, status, created_at FROM decisions ORDER BY created_at DESC"
    ).fetchall()

    lines = "# Decisions Log\n"
    lines += "<!-- AUTO-GENERATED by memory-write.py — do not edit directly. Source of truth: memory.db -->\n\n"
    lines += "Decisions made during this project. Skills should NOT re-question these unless the user explicitly asks to revisit.\n\n"
    lines += "## How to use\n"
    lines += "- Before proposing approaches, check if a relevant decision already exists here\n"
    lines += "- If it does, state \"We previously decided [X] because [Y]\" and proceed\n"
    lines += "- Only add new decisions when the user makes a choice between approaches\n\n"
    lines += "## Decisions\n\n"

    if not rows:
        lines += "(none yet — decisions will be logged as the project progresses)\n"
    else:
        for r in rows:
            tags = json.loads(r["tags"]) if r["tags"] else []
            tags_str = f" `{'` `'.join(tags)}`" if tags else ""
            lines += f"### DEC-{r['id']:03d} — {r['decision']}\n"
            lines += f"- **Rationale:** {r['rationale'] or '—'}\n"
            lines += f"- **Source:** {r['source_skill'] or '—'} | **Phase:** {r['phase'] or '—'}{tags_str}\n"
            lines += f"- **Status:** {r['status']} | **Logged:** {r['created_at'][:10]}\n\n"

    return lines


def render_preferences(conn) -> str:
    rows = conn.execute(
        "SELECT id, preference, source_skill, category, created_at FROM preferences ORDER BY created_at DESC"
    ).fetchall()

    lines = "# User & Team Preferences\n"
    lines += "<!-- AUTO-GENERATED by memory-write.py — do not edit directly. Source of truth: memory.db -->\n\n"
    lines += "Preferences discovered during interactions. Skills should apply these automatically without re-asking.\n\n"
    lines += "## How to use\n"
    lines += "- Read this file at the start of every skill\n"
    lines += "- Apply preferences silently (don't announce \"I see you prefer X\")\n"
    lines += "- Add new preferences when the user expresses a clear preference\n\n"
    lines += "## Preferences\n\n"

    if not rows:
        lines += "(none yet — preferences will be captured as the project progresses)\n"
    else:
        by_cat = {}
        for r in rows:
            cat = r["category"] or "other"
            by_cat.setdefault(cat, []).append(r)
        for cat, items in sorted(by_cat.items()):
            lines += f"### {cat.capitalize()}\n\n"
            for r in items:
                lines += f"- **PREF-{r['id']:03d}:** {r['preference']} _(from {r['source_skill'] or '—'}, {r['created_at'][:10]})_\n"
            lines += "\n"

    return lines


def render_patterns(conn) -> str:
    rows = conn.execute(
        "SELECT id, pattern, source_skill, applies_to, created_at FROM patterns ORDER BY created_at DESC"
    ).fetchall()

    lines = "# Project Patterns\n"
    lines += "<!-- AUTO-GENERATED by memory-write.py — do not edit directly. Source of truth: memory.db -->\n\n"
    lines += "Patterns discovered during this project that should be applied consistently across all documents.\n\n"
    lines += "## How to use\n"
    lines += "- Read this file when generating any document\n"
    lines += "- Apply patterns automatically\n"
    lines += "- Add new patterns when recurring needs are identified\n\n"
    lines += "## Patterns\n\n"

    if not rows:
        lines += "(none yet — patterns will emerge as documents are created)\n"
    else:
        for r in rows:
            lines += f"### PAT-{r['id']:03d} — applies to: `{r['applies_to']}`\n"
            lines += f"{r['pattern']}\n"
            lines += f"_(from {r['source_skill'] or '—'}, {r['created_at'][:10]})_\n\n"

    return lines


def render_linear_mapping(conn) -> str:
    rows = conn.execute(
        "SELECT etus_id, linear_id, title, type, status, created_at, updated_at FROM linear_mapping ORDER BY etus_id"
    ).fetchall()

    lines = "# Linear Issue Mapping\n"
    lines += "<!-- AUTO-GENERATED by memory-write.py — do not edit directly. Source of truth: memory.db -->\n\n"
    lines += "Mapping between ETUS document IDs and Linear issue IDs. Maintained automatically by skills with LINEAR SYNC.\n\n"
    lines += "| ETUS ID | Linear ID | Title | Type | Status | Updated |\n"
    lines += "|---------|-----------|-------|------|--------|----------|\n"

    if not rows:
        lines += "\n_(No mappings yet — will be populated during planning and implementation phases)_\n"
    else:
        for r in rows:
            lines += f"| {r['etus_id']} | {r['linear_id']} | {r['title'] or '—'} | {r['type'] or '—'} | {r['status'] or '—'} | {r['updated_at'][:10]} |\n"

    return lines


def render_repo_docs(conn) -> str:
    rows = conn.execute(
        "SELECT path, filename, doc_type, status, updated_at FROM documents WHERE mode='reference' ORDER BY doc_type, path"
    ).fetchall()

    lines  = "# Repository Docs Index\n"
    lines += "<!-- AUTO-GENERATED by memory-init.py — do not edit directly. Source of truth: memory.db -->\n\n"
    lines += "All `.md` files under `docs/` (excluding `docs/ets/` pipeline artifacts).\n"
    lines += "Skills can read this to find existing design docs, plans, and notes.\n\n"

    if not rows:
        lines += "(no repo docs indexed yet — run `python3 .claude/hooks/memory-init.py --migrate` or `memory-write.py index-docs`)\n"
    else:
        by_type = {}
        for r in rows:
            by_type.setdefault(r["doc_type"], []).append(r)
        for dtype, items in sorted(by_type.items()):
            lines += f"## {dtype.replace('-', ' ').title()}\n\n"
            for r in items:
                lines += f"- `{r['path']}` — {r['status']} — {r['updated_at'][:10]}\n"
            lines += "\n"

    return lines


# ─────────────────────────────────────────────────────────────────────────────
# Regenerate all markdown views
# ─────────────────────────────────────────────────────────────────────────────

def _atomic_write(path: str, content: str) -> None:
    """Write content to a file atomically using tempfile + os.replace."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(path),
        prefix=".tmp_",
        suffix=os.path.splitext(path)[1],
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def regenerate_all_views(conn):
    views = {
        "project-state.md": render_project_state(conn),
        "decisions.md":     render_decisions(conn),
        "preferences.md":   render_preferences(conn),
        "patterns.md":      render_patterns(conn),
        "linear-mapping.md":render_linear_mapping(conn),
        "repo-docs.md":     render_repo_docs(conn),
    }
    for filename, content in views.items():
        _atomic_write(os.path.join(MEMORY_DIR, filename), content)


# ─────────────────────────────────────────────────────────────────────────────
# Migration: import existing .md content into SQLite (best-effort)
# ─────────────────────────────────────────────────────────────────────────────

def migrate_existing_docs(conn):
    """Scan all of docs/ for existing .md/.yaml files and state report .json files and register them."""
    docs_root = os.path.join(PROJECT_ROOT, "docs")
    if not os.path.isdir(docs_root):
        print("  docs/ not found, skipping document migration.")
        return 0

    count = 0
    try:
        for root, _, files in os.walk(docs_root):
            for fname in files:
                if not (
                    fname.endswith(".md")
                    or fname.endswith(".yaml")
                    or root.replace("\\", "/").endswith("/state/reports") and fname.endswith(".json")
                ):
                    continue
                full_path = os.path.join(root, fname)
                rel_path  = os.path.relpath(full_path, PROJECT_ROOT)
                # Skip memory directory itself and handoff files
                if ".memory" in rel_path or ".handoff" in rel_path:
                    continue
                phase, mode, doc_type = detect_metadata(rel_path)
                mtime = datetime.fromtimestamp(
                    os.path.getmtime(full_path), tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
                conn.execute("""
                    INSERT OR IGNORE INTO documents (path, filename, phase, mode, doc_type, status, updated_at, created_at)
                    VALUES (?, ?, ?, ?, ?, 'complete', ?, ?)
                """, (rel_path, fname, phase, mode, doc_type, mtime, mtime))
                count += 1

        conn.commit()
    except Exception as exc:
        conn.rollback()
        print(f"  ERROR during migration, rolled back: {exc}", file=sys.stderr)
        raise
    return count


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    migrate_flag = "--migrate" in sys.argv

    os.makedirs(MEMORY_DIR, exist_ok=True)    # markdown views dir (FUSE)
    os.makedirs(LOCAL_DB_DIR, exist_ok=True)  # SQLite dir (local fs)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(DDL)

    # Track schema version
    conn.execute("INSERT OR IGNORE INTO schema_meta VALUES ('version', ?)", (str(SCHEMA_VERSION),))
    conn.execute("INSERT OR IGNORE INTO schema_meta VALUES ('created_at', ?)",
                 (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),))
    conn.execute("INSERT OR IGNORE INTO project_state (id) VALUES (1)")
    conn.commit()

    print(f"✓ memory.db initialized at {DB_PATH}")
    print(f"  Schema version: {SCHEMA_VERSION}")

    if migrate_flag:
        print("  Migrating existing documents…")
        n = migrate_existing_docs(conn)
        print(f"  Migrated {n} documents.")

    print("  Regenerating markdown views…")
    regenerate_all_views(conn)
    print("  ✓ project-state.md, decisions.md, preferences.md, patterns.md, linear-mapping.md updated")

    conn.close()
    print("\nDone. Memory system ready.")


if __name__ == "__main__":
    main()
