#!/usr/bin/env python3
"""
state_utils.py — Re-export facade for backward compatibility.

The actual implementation is split across:
- yaml_io.py          — YAML parsing/dumping, frontmatter I/O
- state_defaults.py   — Default factories, normalization, path helpers, constants
- feature_lifecycle.py — Feature state management, ID extraction, phase routing, sync
- linear_sync.py      — Linear integration (mapping sync, cycle projection)

All public symbols are re-exported here so existing imports continue to work:
  from state_utils import sync_document_state, read_yaml_file, ...
"""

# yaml_io
from yaml_io import (  # noqa: F401
    FEATURE_BODY_TEMPLATE,
    dump_simple_yaml,
    parse_simple_yaml,
    read_frontmatter_markdown,
    read_yaml_file,
    write_frontmatter_markdown,
    write_yaml_file,
)

# state_defaults
from state_defaults import (  # noqa: F401
    FEATURE_DOC_KEYS,
    ID_PATTERNS,
    REPORT_DOC_TYPES,
    default_execution_status,
    default_execution_sync,
    default_feature_index,
    default_feature_status,
    default_project_status,
    default_workflow_state,
    docs_project_root,
    execution_status_path,
    execution_sync_path,
    feature_dir,
    normalize_execution_status,
    normalize_execution_sync,
    normalize_feature_index,
    normalize_feature_status,
    normalize_project_status,
    now_iso,
    rel_project_path,
    slugify,
    state_dir,
    title_from_slug,
)

# feature_lifecycle
from feature_lifecycle import (  # noqa: F401
    classify_etus_id,
    ensure_feature_state,
    ensure_project_state,
    extract_feature_slug,
    extract_ids_from_text,
    find_single_project_slug,
    list_project_slugs,
    sync_document_state,
)

# linear_sync
from linear_sync import (  # noqa: F401
    sync_linear_cycle,
    sync_linear_mapping,
)
