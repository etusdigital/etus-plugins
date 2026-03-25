---
description: Generate Database Specification — DDL + constraints + performance config (fuses old database-requirements + database-schema)
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Database Specification

Creating database-spec for: **$ARGUMENTS**

> **Purpose:** Single source of truth for physical database design: DDL, ORDER BY keys, TTLs, partitioning, constraints, indexing, migration strategy.
> **Fuses:** Previous database-requirements.md + database-schema.md into one document.

## Prerequisites

!`test -f docs/design/data-requirements.md && echo "✓ data-requirements.md exists" || echo "⚠ Missing data requirements (run /data-reqs first)"`
!`test -f docs/design/erd.md && echo "✓ erd.md exists" || echo "⚠ Missing ERD (run /erd first)"`

## Setup

!`mkdir -p docs/data && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/data-chain/knowledge/database-spec.md

## Interactive Discovery

### Step 1: Database Engine & Context

1. What database engine? (PostgreSQL / ClickHouse / MySQL / SQLite / etc.)
2. What's the expected data volume at launch?
3. What's the growth rate (records/month)?
4. What are the critical query patterns? (OLTP reads, OLAP aggregations, time-series)

### Step 2: Table Design (per entity from ERD)

For each table:
1. **Columns:** Name, type, nullable, default
2. **Primary key:** Strategy (auto-increment, UUID, composite)
3. **Engine-specific:** ORDER BY (ClickHouse), partitioning, TTL
4. **Constraints:** UNIQUE, CHECK, FOREIGN KEY
5. **Indexes:** Which columns, why

### Step 3: Performance Configuration

1. **Indexing strategy:** What gets indexed and why
2. **Partitioning:** By date? By tenant?
3. **Retention:** TTL policies per table
4. **Replication:** Single / Replicated

### Step 4: Migration Strategy

1. How are schema changes tracked? (migrations, liquibase, manual DDL)
2. Rollback policy
3. Zero-downtime strategy

## Generate Document

Generate `docs/design/database-spec.md`

**Structure:**
1. **Database Context** — Engine, volume, growth, query patterns
2. **DDL Statements** — CREATE TABLE per entity (SST for schema)
3. **Constraints & Indexes** — Business rule enforcement at DB level
4. **Performance Configuration** — ORDER BY, partitioning, TTL, replication
5. **Security Policies** — Access control, encryption, data classification
6. **Migration Strategy** — Version control, rollback, zero-downtime
7. **Capacity Planning** — Day 1, Month 1, Month 6 projections
8. **Risk Assessment** — Data loss, performance degradation, schema evolution

## Validation

!`test -f docs/design/database-spec.md && echo "✓ database-spec.md created" || echo "✗ Generation failed"`

!`if [ -f docs/design/database-spec.md ]; then
  grep -ci "CREATE TABLE" docs/design/database-spec.md | xargs echo "Tables defined:"
  grep -ci "INDEX" docs/design/database-spec.md | xargs echo "Index references:"
fi`

## Next Steps

```
/dictionary         # Define field semantics (dict.*)
/dfd                # Map data flow between services
```

---

**Database Specification generated!** DDL + constraints + performance config in a single document.
