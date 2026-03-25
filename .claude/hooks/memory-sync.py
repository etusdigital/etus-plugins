#!/usr/bin/env python3
"""
memory-sync.py — PostToolUse hook for the ETUS PMDocs memory system.

Triggered automatically by Claude Code after every Write or Edit tool call.
Reads the event JSON from stdin, detects which document was saved,
updates the SQLite database, and regenerates project-state.md.

Exit codes:
  0 — always (this hook warns but never blocks)
"""

import sqlite3
import os
import sys
import json
import re
import tempfile
import traceback
from datetime import datetime, timezone
from path_utils import project_root_from, resolve_memory_dir, split_ets_path
from state_utils import normalize_project_status, read_yaml_file, sync_document_state


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

# ─────────────────────────────────────────────────────────────────────────────
# Paths — resolved relative to project root (CWD when hook runs)
# ─────────────────────────────────────────────────────────────────────────────
import hashlib as _hashlib

PROJECT_ROOT  = os.getcwd()
MEMORY_DIR    = resolve_memory_dir(PROJECT_ROOT)   # markdown views

# SQLite DB lives on the LOCAL filesystem (not virtiofs/FUSE, which blocks file locking).
_project_hash = _hashlib.md5(PROJECT_ROOT.encode()).hexdigest()[:8]
LOCAL_DB_DIR  = os.path.expanduser("~/.claude/etus-memory")
DB_PATH       = os.path.join(LOCAL_DB_DIR, f"memory-{_project_hash}.db")


# ─────────────────────────────────────────────────────────────────────────────
# Path → metadata detection  (same map as memory-init.py)
# ─────────────────────────────────────────────────────────────────────────────
PATH_MAP = [
    (r"state/reports/discovery\.json$",            "discovery",      "product",        "report-discovery"),
    (r"state/reports/opportunities\.json$",        "planning",       "product",        "report-opportunities"),
    (r"state/reports/solution-report\.json$",      "planning",       "product",        "report-solution"),
    (r"state/reports/planning\.json$",             "planning",       "product",        "report-planning"),
    (r"state/reports/design\.json$",               "design",         "product",        "report-design"),
    (r"state/reports/implementation\.json$",       "implementation", "product",        "report-implementation"),
    (r"features/[^/]+/solution-discovery\.(md|yaml)$", "feature",        "feature",        "solution-discovery"),
    (r"features/[^/]+/feature-status\.(md|yaml)$",     "feature",        "feature",        "feature-status"),
    (r"features/[^/]+/feature-brief\.(md|yaml)$",      "feature",        "feature",        "feature-brief"),
    (r"features/[^/]+/user-stories\.(md|yaml)$",       "feature",        "feature",        "user-stories"),
    (r"features/[^/]+/design-delta\.(md|yaml)$",       "feature",        "feature",        "design-delta"),
    (r"features/[^/]+/impl-plan\.(md|yaml)$",          "feature",        "feature",        "impl-plan"),
    (r"features/feature-brief-(.+)\.(md|yaml)$",  "feature",        "feature",        "feature-brief"),
    (r"features/user-stories-(.+)\.(md|yaml)$",   "feature",        "feature",        "user-stories"),
    (r"features/design-delta-(.+)\.(md|yaml)$",   "feature",        "feature",        "design-delta"),
    (r"features/impl-plan-(.+)\.(md|yaml)$",       "feature",        "feature",        "impl-plan"),
    (r"state/project-status\.(md|yaml)$",          "state",          "system",         "project-status"),
    (r"state/workflow-state\.(md|yaml)$",          "state",          "system",         "workflow-state"),
    (r"state/coverage-matrix\.(md|yaml)$",         "discovery",      "product",        "coverage-matrix"),
    (r"state/elicitation-state\.(md|yaml)$",       "discovery",      "system",         "elicitation-state"),
    (r"state/feature-index\.(md|yaml)$",           "state",          "system",         "feature-index"),
    (r"state/execution-status\.(md|yaml)$",        "state",          "system",         "execution-status"),
    (r"state/execution-sync\.(md|yaml)$",          "state",          "system",         "execution-sync"),
    (r"state/features/[^/]+\.(md|yaml)$",          "feature",        "feature",        "feature-state"),
    (r"bugs/tech-spec-(.+)\.(md|yaml)$",           "bug",            "bug",            "tech-spec-bug"),
    (r"spikes/spike-(.+)\.(md|yaml)$",             "spike",          "spike",          "spike"),
    (r"discovery/opportunity-pack\.(md|yaml)$",    "discovery",      "product",        "opportunity-pack"),
    (r"discovery/project-context\.",               "discovery",      "product",        "project-context"),
    (r"discovery/baseline\.",                       "discovery",      "product",        "baseline"),
    (r"discovery/discovery-report\.",              "discovery",      "product",        "discovery-report"),
    (r"discovery/product-vision\.",                "discovery",      "product",        "product-vision"),
    (r"planning/ost\.",                             "planning",       "product",        "ost"),
    (r"planning/prioritization\.",                 "planning",       "product",        "prioritization"),
    (r"planning/solution-discovery\.",             "planning",       "product",        "solution-discovery"),
    (r"planning/solution-experiments\.",           "planning",       "product",        "solution-experiments"),
    (r"planning/prd\.",                            "planning",       "product",        "prd"),
    (r"planning/user-stories\.",                   "planning",       "product",        "user-stories"),
    (r"planning/feature-specs/",                   "planning",       "product",        "feature-spec"),
    (r"architecture/architecture-diagram\.",       "design",         "product",        "architecture-diagram"),
    (r"architecture/tech-spec\.",                  "design",         "product",        "tech-spec"),
    (r"data/data-requirements\.",                  "design",         "product",        "data-requirements"),
    (r"data/erd\.",                                "design",         "product",        "erd"),
    (r"data/database-spec\.",                      "design",         "product",        "database-spec"),
    (r"data/data-dictionary\.",                    "design",         "product",        "data-dictionary"),
    (r"data/data-flow-diagram\.",                  "design",         "product",        "data-flow-diagram"),
    (r"data/data-catalog\.",                       "design",         "product",        "data-catalog"),
    (r"ux/user-journey\.",                         "design",         "product",        "user-journey"),
    (r"ux/ux-sitemap\.",                           "design",         "product",        "ux-sitemap"),
    (r"ux/wireframes\.",                           "design",         "product",        "wireframes"),
    (r"ux/style-guide\.",                          "design",         "product",        "style-guide"),
    (r"implementation/api-spec\.",                 "implementation", "product",        "api-spec"),
    (r"implementation/implementation-plan\.",      "implementation", "product",        "implementation-plan"),
    (r"implementation/quality-checklist\.",        "implementation", "product",        "quality-checklist"),
    (r"implementation/release-plan\.",             "implementation", "product",        "release-plan"),
    # ── Repo-level docs (outside docs/ets/) ──
    (r"docs/design/",                               "repo",           "reference",      "design-doc"),
    (r"docs/plans/",                                 "repo",           "reference",      "plan-doc"),
    (r"docs/design-notes/",                          "repo",           "reference",      "design-note"),
    (r"docs/[^/]+\.md$",                             "repo",           "reference",      "repo-doc"),
]

def detect_metadata(path: str):
    info = split_ets_path(path)
    inner_path = info.inner_path
    for pattern, phase, mode, doc_type in PATH_MAP:
        if re.search(pattern, inner_path):
            return phase, mode, doc_type
    filename = os.path.basename(path)
    return "unknown", "unknown", filename.rsplit(".", 1)[0]


# ─────────────────────────────────────────────────────────────────────────────
# Next-step inference
# ─────────────────────────────────────────────────────────────────────────────
NEXT_STEP_MAP = {
    ("discovery",      "product"):   "Run /plan opportunities to start opportunity focus",
    ("planning",       "product"):   "Run /solution or /plan requirements depending on planning state",
    ("design",         "product"):   "Run /implement to start Implementation phase",
    ("implementation", "product"):   "Run /validate to run the final documentation checks",
    ("feature",        "feature"):   "Continue Feature pipeline: solution-discovery → feature-brief → user-stories → design-delta → impl-plan",
    ("bug",            "bug"):       "Review tech-spec-bug.md and proceed with fix",
    ("spike",          "spike"):     "Review spike.md findings and decide on next action",
    ("repo",           "reference"): "Repo doc indexed — no pipeline action needed",
}

PHASE_ORDER = ["discovery", "planning", "design", "implementation"]

def infer_next_step(conn, phase: str, mode: str) -> str:
    if mode == "product":
        doc_types = {
            row["doc_type"]
            for row in conn.execute(
                "SELECT doc_type FROM documents WHERE mode='product'"
            ).fetchall()
        }
        if "opportunity-pack" not in doc_types:
            return "Run `/ideate` to start problem discovery"
        if "product-vision" not in doc_types:
            return "Run `/discover` to complete discovery"
        if "ost" not in doc_types or "prioritization" not in doc_types:
            return "Run `/plan opportunities` to structure and prioritize opportunities"
        if "solution-discovery" not in doc_types:
            return "Run `/solution` to select and validate the solution direction"
        if "prd" not in doc_types or "user-stories" not in doc_types:
            return "Run `/plan requirements` to define delivery requirements"
        if "tech-spec" not in doc_types:
            return "Run `/design` to start design"
        if "implementation-plan" not in doc_types:
            return "Run `/implement` to start implementation planning"
        return "Run `/validate` to run the final quality gate"
    return NEXT_STEP_MAP.get((phase, mode), "Continue with next step in the workflow")


def read_project_next_step(project_root: str, rel_path: str, fallback: str) -> str:
    info = split_ets_path(rel_path)
    if not info.is_new_root or not info.project_slug:
        return fallback

    project_status_path = os.path.join(
        project_root,
        "docs",
        "ets",
        "projects",
        info.project_slug,
        "state",
        "project-status.yaml",
    )
    project_status = normalize_project_status(read_yaml_file(project_status_path, {}), info.project_slug)
    return project_status.get("next_step", fallback)


# ─────────────────────────────────────────────────────────────────────────────
# project-state.md renderer  (minimal version — full version in memory-init.py)
# ─────────────────────────────────────────────────────────────────────────────
def render_project_state(conn) -> str:
    state = conn.execute("SELECT * FROM project_state WHERE id=1").fetchone()
    docs  = conn.execute(
        "SELECT path, doc_type, phase, mode, status, updated_at FROM documents ORDER BY updated_at DESC"
    ).fetchall()

    mode  = state["current_mode"]  if state else "not set"
    phase = state["current_phase"] if state else "not started"
    next_ = state["next_step"]     if state else "Run /start-project to begin"
    ts    = state["last_activity"] if state else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Documents list
    doc_lines = ""
    if docs:
        for d in docs:
            doc_lines += f"- `{d['path']}` — {d['doc_type']} ({d['status']}) — {d['updated_at'][:10]}\n"
    else:
        doc_lines = "(none yet)\n"

    # Mode-aware phase table
    if mode == "feature":
        rows_header = "| Step | Status | Last Activity |\n|------|--------|---------------|\n"
        rows_body = ""
        for step in ["solution-discovery", "feature-brief", "user-stories", "design-delta", "impl-plan"]:
            row = conn.execute(
                "SELECT status, updated_at FROM documents WHERE doc_type=? AND mode='feature' ORDER BY updated_at DESC LIMIT 1",
                (step,)
            ).fetchone()
            s = row["status"] if row else "not started"
            t = row["updated_at"][:10] if row else "—"
            rows_body += f"| {step} | {s} | {t} |\n"
        phase_table = rows_header + rows_body

    elif mode == "bug":
        rows_header = "| Step | Status | Last Activity |\n|------|--------|---------------|\n"
        row = conn.execute(
            "SELECT status, updated_at FROM documents WHERE mode='bug' ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        s = row["status"] if row else "not started"
        t = row["updated_at"][:10] if row else "—"
        phase_table = rows_header + f"| tech-spec (bug) | {s} | {t} |\n"

    elif mode == "spike":
        rows_header = "| Step | Status | Last Activity |\n|------|--------|---------------|\n"
        row = conn.execute(
            "SELECT status, updated_at FROM documents WHERE mode='spike' ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        s = row["status"] if row else "not started"
        t = row["updated_at"][:10] if row else "—"
        phase_table = rows_header + f"| spike doc | {s} | {t} |\n"

    else:  # product or not set
        rows_header = "| Phase | Status | Last Activity |\n|-------|--------|---------------|\n"
        rows_body = ""
        for p in ["discovery", "planning", "design", "implementation"]:
            row = conn.execute(
                "SELECT status, updated_at FROM documents WHERE phase=? ORDER BY updated_at DESC LIMIT 1", (p,)
            ).fetchone()
            s = row["status"] if row else "not started"
            t = row["updated_at"][:10] if row else "—"
            rows_body += f"| {p.capitalize()} | {s} | {t} |\n"
        phase_table = rows_header + rows_body

    return (
        "# Project State\n"
        "<!-- AUTO-GENERATED by memory-sync.py — do not edit directly. Source of truth: memory.db -->\n\n"
        f"**Last updated:** {ts}\n"
        f"**Current phase:** {phase}\n"
        f"**Current mode:** {mode}\n\n"
        "## Phase Status\n\n"
        f"{phase_table}\n"
        "## Documents Completed\n\n"
        f"{doc_lines}\n"
        "## Next Step\n\n"
        f"{next_}\n"
    )


# ─────────────────────────────────────────────────────────────────────────────
# repo-docs.md renderer
# ─────────────────────────────────────────────────────────────────────────────
def render_repo_docs(conn) -> str:
    rows = conn.execute(
        "SELECT path, filename, doc_type, status, updated_at FROM documents WHERE mode='reference' ORDER BY doc_type, path"
    ).fetchall()

    lines  = "# Repository Docs Index\n"
    lines += "<!-- AUTO-GENERATED by memory-sync.py — do not edit directly. Source of truth: memory.db -->\n\n"
    lines += "All `.md` files under `docs/` (excluding `docs/ets/` pipeline artifacts).\n"
    lines += "Skills can read this to find existing design docs, plans, and notes.\n\n"

    if not rows:
        lines += "(no repo docs indexed yet — save or index .md files under docs/)\n"
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
# Gate decision persistence
# ─────────────────────────────────────────────────────────────────────────────
def _propagate_gate_decisions(rel_path: str, phase: str, doc_type: str) -> None:
    """Gate decision persistence: when a gate has feedback (ITERATE/NO-GO),
    persist the feedback and rejected approaches to decisions.md
    so downstream phases know what was already tried and rejected."""
    if doc_type != "workflow-state":
        return
    try:
        abs_path = os.path.join(PROJECT_ROOT, rel_path) if not os.path.isabs(rel_path) else rel_path
        wf_data = read_yaml_file(abs_path, {})
        gates = wf_data.get("gates", {})
        memory_write_script = os.path.join(PROJECT_ROOT, ".claude", "hooks", "memory-write.py")
        if not os.path.exists(memory_write_script):
            return
        for gate_name, gate_info in gates.items():
            if not isinstance(gate_info, dict):
                continue
            status = gate_info.get("status", "")
            feedback = gate_info.get("feedback", "")
            rejected = gate_info.get("rejected_approaches", [])
            if status in ("iterate", "no-go", "ITERATE", "NO-GO") and feedback:
                rejected_text = "; ".join(rejected) if rejected else "none recorded"
                decision_text = (
                    f"Gate '{gate_name}' returned {status}. "
                    f"Feedback: {feedback}. "
                    f"Rejected approaches: {rejected_text}."
                )
                import subprocess
                subprocess.run(
                    [
                        sys.executable,
                        memory_write_script,
                        "decision",
                        decision_text,
                        f"Gate {gate_name} {status} — avoid re-proposing rejected approaches",
                        "validate-gate",
                        phase or "validation",
                        f"gate,{gate_name},{status}",
                    ],
                    cwd=PROJECT_ROOT,
                    timeout=10,
                    capture_output=True,
                )
    except Exception:
        pass  # Never block on gate propagation errors


# ─────────────────────────────────────────────────────────────────────────────
# Status detection from document content
# ─────────────────────────────────────────────────────────────────────────────
def detect_status(file_path: str) -> str:
    """Return 'complete' or 'draft' based on STATUS marker in the file."""
    try:
        abs_path = os.path.join(PROJECT_ROOT, file_path) if not os.path.isabs(file_path) else file_path
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            head = f.read(2000)
        if "STATUS: DRAFT" in head or "status: draft" in head.lower():
            return "draft"
        return "complete"
    except Exception:
        return "draft"


# ─────────────────────────────────────────────────────────────────────────────
# Main hook logic
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # 1. Read stdin event JSON
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)  # malformed input — never block

    # 2. Extract file path
    tool_input = event.get("tool_input", {})
    file_path  = tool_input.get("file_path", "") or tool_input.get("path", "")

    if not file_path:
        sys.exit(0)

    # 3. Only process .md/.yaml and state report .json files inside docs/
    norm_path = file_path.replace("\\", "/")
    if "/docs/" not in norm_path:
        sys.exit(0)
    if not (
        norm_path.endswith(".md")
        or norm_path.endswith(".yaml")
        or "/state/reports/" in norm_path and norm_path.endswith(".json")
    ):
        sys.exit(0)

    # Skip memory files themselves (avoid infinite loop)
    if "/.memory/" in norm_path:
        sys.exit(0)

    # 4. Ensure DB exists (init if first run)
    if not os.path.exists(DB_PATH):
        os.makedirs(MEMORY_DIR, exist_ok=True)    # markdown views dir (FUSE)
        os.makedirs(LOCAL_DB_DIR, exist_ok=True)  # SQLite dir (local fs)
        # Lazy init: import memory-init schema inline
        init_script = os.path.join(PROJECT_ROOT, ".claude/hooks/memory-init.py")
        if os.path.exists(init_script):
            import importlib.util
            spec = importlib.util.spec_from_file_location("memory_init", init_script)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            conn.executescript(mod.DDL)
            conn.execute("INSERT OR IGNORE INTO schema_meta VALUES ('version', '1')")
            conn.execute("INSERT OR IGNORE INTO project_state (id) VALUES (1)")
            conn.commit()
            conn.close()

    # 5. Connect to DB
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
    except Exception:
        sys.exit(0)  # DB not accessible — never block

    try:
        # 6. Detect metadata for this file
        # Use relative path from project root
        if os.path.isabs(file_path):
            rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        else:
            rel_path = file_path
        rel_path = rel_path.replace("\\", "/")

        filename  = os.path.basename(rel_path)
        phase, mode, doc_type = detect_metadata(rel_path)
        status    = detect_status(rel_path)
        now       = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 7. Upsert document record
        conn.execute("""
            INSERT INTO documents (path, filename, phase, mode, doc_type, status, updated_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                filename   = excluded.filename,
                phase      = excluded.phase,
                mode       = excluded.mode,
                doc_type   = excluded.doc_type,
                status     = excluded.status,
                updated_at = excluded.updated_at
        """, (rel_path, filename, phase, mode, doc_type, status, now, now))

        # 8. Sync YAML/frontmatter operational state
        sync_result = sync_document_state(PROJECT_ROOT, rel_path, phase, mode, doc_type, status)

        # 9. Update project_state (only for pipeline docs, not repo-level docs)
        if mode != "reference":
            next_step = infer_next_step(conn, phase, mode)
            next_step = read_project_next_step(PROJECT_ROOT, rel_path, next_step)
            conn.execute("""
                INSERT INTO project_state (id, current_phase, current_mode, last_document, last_activity, next_step)
                VALUES (1, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    current_phase  = excluded.current_phase,
                    current_mode   = excluded.current_mode,
                    last_document  = excluded.last_document,
                    last_activity  = excluded.last_activity,
                    next_step      = excluded.next_step
            """, (phase, mode, rel_path, now, next_step))

        conn.commit()

        # Gate decision persistence: when a gate has feedback (ITERATE/NO-GO),
        # persist the feedback and rejected approaches to decisions.md
        # so downstream phases know what was already tried and rejected.
        _propagate_gate_decisions(rel_path, phase, doc_type)

        # 10. Regenerate views (atomic writes)
        os.makedirs(MEMORY_DIR, exist_ok=True)
        _atomic_write(os.path.join(MEMORY_DIR, "project-state.md"), render_project_state(conn))

        # 11. Regenerate repo-docs.md view
        _atomic_write(os.path.join(MEMORY_DIR, "repo-docs.md"), render_repo_docs(conn))

    except Exception:
        # Never block on memory errors — just log to stderr quietly
        print(f"[memory-sync] Warning: {traceback.format_exc()}", file=sys.stderr)
    finally:
        conn.close()

    sys.exit(0)


if __name__ == "__main__":
    main()
