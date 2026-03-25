---
doc_meta:
  id: database-spec
  display_name: "Database Specification"
  pillar: Design
  phase: Data Design
  sequence: 3
  updated: "2026-03-14"
  status: template
---

# Database Specification

**Document:** database-spec.md
**Responsibility:** Define SQL schema, indices, and migration strategy (SINGLE SOURCE OF TRUTH)
**Recipients:** Database engineers, implementation engineers, DevOps

---
## Responsaveis

- **Owner:** Data/BI Lead
- **Contribuem:** Tech Lead, DBA, Dev team
- **Aprovacao:** Tech Lead


## Table of Contents

- [Database Engine Selection](#database-engine-selection)
- [Schema DDL](#schema-ddl-table-definitions)
- [Indices](#indices)
- [Constraints](#constraints)
- [Migration Strategy](#migration-strategy)
- [Seed Data](#seed-data)
- [Backup & Recovery](#backup--recovery)
- [Schema Validation](#schema-validation)
- [Next Steps](#next-steps)

---

## Database Engine Selection

**Selected Engine:** PostgreSQL 15+

**Justification:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Database Properties:**
- **Encoding:** UTF-8
- **Locale:** pt_BR.UTF-8
- **Timezone:** UTC (default)
- **Collation:** [Appropriate for Portuguese]

---

## Schema DDL (Table Definitions)

### Table: [ENTITY-A]

```sql
CREATE TABLE [ENTITY-A] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,

    CONSTRAINT [ENTITY-A]_status_check CHECK (status IN ('active', 'inactive', 'archived')),
    CONSTRAINT [ENTITY-A]_created_before_updated CHECK (created_at <= updated_at)
);

COMMENT ON TABLE [ENTITY-A] IS 'Entity description';
COMMENT ON COLUMN [ENTITY-A].id IS 'Unique identifier (UUID)';
COMMENT ON COLUMN [ENTITY-A].name IS 'Unique name of entity';
```

### Table: [ENTITY-B]

```sql
CREATE TABLE [ENTITY-B] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_a_id UUID NOT NULL,
    code VARCHAR(100) NOT NULL UNIQUE,
    amount NUMERIC(15, 2) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT [ENTITY-B]_entity_a_fk FOREIGN KEY (entity_a_id)
        REFERENCES [ENTITY-A](id) ON DELETE CASCADE,
    CONSTRAINT [ENTITY-B]_amount_positive CHECK (amount > 0)
);

COMMENT ON TABLE [ENTITY-B] IS 'Entity B description';
COMMENT ON COLUMN [ENTITY-B].entity_a_id IS 'Foreign key to ENTITY-A';
```

### Table: [ENTITY-C]

```sql
CREATE TABLE [ENTITY-C] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_a_id UUID NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT [ENTITY-C]_entity_a_fk FOREIGN KEY (entity_a_id)
        REFERENCES [ENTITY-A](id) ON DELETE CASCADE,
    CONSTRAINT [ENTITY-C]_status_check CHECK (status IN ('pending', 'active', 'inactive'))
);

COMMENT ON TABLE [ENTITY-C] IS 'One-to-one relationship with ENTITY-A';
```

### Table: [ENTITY-D]

```sql
CREATE TABLE [ENTITY-D] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_b_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT [ENTITY-D]_entity_b_fk FOREIGN KEY (entity_b_id)
        REFERENCES [ENTITY-B](id) ON DELETE CASCADE
);

COMMENT ON TABLE [ENTITY-D] IS 'Entity D description';
```

### Table: [ENTITY-E]

```sql
CREATE TABLE [ENTITY-E] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_c_id UUID NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT [ENTITY-E]_entity_c_fk FOREIGN KEY (entity_c_id)
        REFERENCES [ENTITY-C](id) ON DELETE CASCADE
);

COMMENT ON TABLE [ENTITY-E] IS 'Entity E description';
```

---

## Indices

### Performance Indices

```sql
-- Indices on Foreign Keys (CRITICAL for JOINs)
CREATE INDEX idx_[ENTITY-B]_entity_a_id ON [ENTITY-B](entity_a_id);
CREATE INDEX idx_[ENTITY-C]_entity_a_id ON [ENTITY-C](entity_a_id);
CREATE INDEX idx_[ENTITY-D]_entity_b_id ON [ENTITY-D](entity_b_id);
CREATE INDEX idx_[ENTITY-E]_entity_c_id ON [ENTITY-E](entity_c_id);

-- Indices on frequently queried fields
CREATE INDEX idx_[ENTITY-A]_status ON [ENTITY-A](status)
    WHERE deleted_at IS NULL;
CREATE INDEX idx_[ENTITY-B]_code ON [ENTITY-B](code);
CREATE INDEX idx_[ENTITY-B]_created_at ON [ENTITY-B](created_at DESC);

-- Composite indices for multi-column queries
CREATE INDEX idx_[ENTITY-B]_entity_a_status ON [ENTITY-B](entity_a_id, status);
```

### Soft Delete Indices

```sql
-- Partial indices for soft deletes (exclude deleted records)
CREATE INDEX idx_[ENTITY-A]_active ON [ENTITY-A](id, status)
    WHERE deleted_at IS NULL;
```

---

## Constraints

### Referential Integrity Constraints

| Relationship | Foreign Key | Reference | Delete Action | Update Action |
|---|---|---|---|---|
| [ENTITY-B] → [ENTITY-A] | `entity_a_id` | `[ENTITY-A].id` | CASCADE | CASCADE |
| [ENTITY-C] → [ENTITY-A] | `entity_a_id` | `[ENTITY-A].id` | CASCADE | CASCADE |
| [ENTITY-D] → [ENTITY-B] | `entity_b_id` | `[ENTITY-B].id` | CASCADE | CASCADE |
| [ENTITY-E] → [ENTITY-C] | `entity_c_id` | `[ENTITY-C].id` | CASCADE | CASCADE |

### Uniqueness Constraints

```sql
ALTER TABLE [ENTITY-A] ADD CONSTRAINT uk_[ENTITY-A]_name UNIQUE (name);
ALTER TABLE [ENTITY-B] ADD CONSTRAINT uk_[ENTITY-B]_code UNIQUE (code);
ALTER TABLE [ENTITY-C] ADD CONSTRAINT uk_[ENTITY-C]_entity_a_id UNIQUE (entity_a_id);
```

### Check Constraints

```sql
-- Status values
ALTER TABLE [ENTITY-A]
    ADD CONSTRAINT ck_[ENTITY-A]_status
    CHECK (status IN ('active', 'inactive', 'archived'));

-- Numeric constraints
ALTER TABLE [ENTITY-B]
    ADD CONSTRAINT ck_[ENTITY-B]_amount_positive
    CHECK (amount > 0);

-- Temporal constraints
ALTER TABLE [ENTITY-A]
    ADD CONSTRAINT ck_[ENTITY-A]_created_before_updated
    CHECK (created_at <= updated_at);
```

---

## Migration Strategy

### Migration Versioning

Pattern: `YYYYMMDD_HHMM_description.sql`

Example:
- `20260314_1400_create_initial_schema.sql`
- `20260314_1430_add_entity_c_table.sql`
- `20260315_0900_add_indexes.sql`

### Migration Tools

**Recommended:** Liquibase or Flyway

```yaml
migration:
  tool: flyway
  location: "db/migration"
  baseline_version: "1"
  validate_on_migrate: true
  clean_disabled: true  # IMPORTANT: Never clean in production
```

### Migration Process

1. **Local development:**
   ```bash
   flyway migrate
   ```

2. **Staging:**
   ```bash
   flyway validate
   flyway info
   flyway migrate
   ```

3. **Production (with backup):**
   ```bash
   pg_dump production > backup_$(date +%Y%m%d_%H%M%S).sql
   flyway validate
   flyway migrate
   ```

### Rollback Strategy

- **Manual reversals:** Each migration has corresponding rollback script
- **Migration retention:** Keep all migrations (never delete)
- **Post-rollback validation:** Run integrity tests

---

## Seed Data

### Initial Data (if applicable)

```sql
-- Insert initial configuration data
INSERT INTO [ENTITY-A] (id, name, description, status) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'Default Entity', 'System default entity', 'active'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Archive Entity', 'Entity for archives', 'active');
```

**Note:** Seeds must be idempotent (use `INSERT ... ON CONFLICT` if necessary)

---

## Backup & Recovery

### Backup Strategy

| Type | Frequency | Retention | Location |
|------|-----------|----------|----------|
| Full Backup | Daily (02:00 UTC) | 30 days | S3 |
| Incremental | Every 6 hours | 7 days | S3 |
| Transactional Log | Continuous | 7 days | S3 |

### Backup Procedure

```bash
# Full backup
pg_dump -h localhost -U postgres -Fc postgres > backup_full_$(date +%Y%m%d_%H%M%S).dump

# Backup with compression
pg_dump -h localhost -U postgres --compress=9 -Fc postgres > backup.sql.gz
```

### Recovery Time Objective (RTO)

- **RTO:** 4 hours
- **RPO:** 1 hour

### Recovery Procedure

```bash
# Restore full backup
pg_restore -h localhost -U postgres -d postgres backup_full.dump

# Recover transactional logs up to specific timestamp
pg_restore -h localhost -U postgres -x -Ft backup.tar | psql -d postgres
```

---

## Schema Validation

```sql
-- List all tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Validate constraints
SELECT constraint_name, constraint_type FROM information_schema.table_constraints
WHERE table_schema = 'public';

-- Check indices
SELECT indexname FROM pg_indexes WHERE schemaname = 'public';

-- Validate FKs
SELECT constraint_name, table_name, referenced_table_name
FROM information_schema.referential_constraints;
```

---


## O que fazer / O que nao fazer

**O que fazer:**
- Incluir COMMENT ON em todas as tabelas e colunas
- Documentar estrategia de indices com justificativa
- Versionar migrations com rollback
- Definir soft delete vs hard delete explicitamente

**O que nao fazer:**
- Nao duplicar DDL em outros documentos (SST e aqui)
- Nao criar indices sem analise de query patterns
- Nao usar CASCADE sem avaliar impacto
- Nao esquecer seeds idemponentes

## Next Steps

✅ Move to **data-dictionary** (Field definitions)
✅ Move to **api-spec** (Endpoints based on this schema)
