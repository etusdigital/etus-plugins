---
doc_meta:
  id: data-catalog
  display_name: "Data Catalog"
  pillar: Design
  phase: Data Design
  sequence: 6
  updated: "2026-03-14"
  status: template
---

# Data Catalog

**Document:** data-catalog.md
**Responsibility:** Inventory of data assets with classification, ownership, lineage, and governance
**Recipients:** Data stewards, data engineers, compliance, architects

---
## Responsaveis

- **Owner:** Data/BI Lead
- **Contribuem:** Tech Lead, Compliance, PM
- **Aprovacao:** Tech Lead + Compliance


## Data Asset Inventory

### Operational Tables

| ID | Asset Name | Storage | Type | Records (est.) | Size (GB) | Update Frequency | Owner |
|----|-----------|---------|------|----------------|-----------|------------------|-------|
| `cat.asset.001` | [DOMAIN-A] | PostgreSQL | Table | [Volume] | [Size] | Continuous | [Owner] |
| `cat.asset.002` | [DOMAIN-B] | PostgreSQL | Table | [Volume] | [Size] | Continuous | [Owner] |
| `cat.asset.003` | [DOMAIN-C] | PostgreSQL | Table | [Volume] | [Size] | Daily | [Owner] |

### Cache Storage

| ID | Asset Name | Storage | Type | TTL | Size (GB) | Hit Rate | Owner |
|----|-----------|---------|------|-----|-----------|----------|-------|
| `cat.asset.cache.001` | Domain Configuration | Redis | Cache | 5min | [Size] | [Rate]% | [Owner] |
| `cat.asset.cache.002` | User Sessions | Redis | Cache | 24h | [Size] | [Rate]% | [Owner] |

### Message Queues

| ID | Asset Name | Storage | Type | Throughput | Retention | Owner |
|----|-----------|---------|------|-----------|-----------|-------|
| `cat.asset.queue.001` | Asynchronous Reports | Redis Queue | Queue | [X] jobs/s | 7 days | [Owner] |
| `cat.asset.queue.002` | Data Synchronization | Redis Queue | Queue | [Y] jobs/s | 30 days | [Owner] |

### Views

| ID | Asset Name | Base Tables | Refresh Frequency | Owner |
|----|-----------|-------------|------------------|-------|
| `cat.asset.view.001` | Aggregated Report A | [DOMAIN-A], [DOMAIN-B] | Daily | [Owner] |
| `cat.asset.view.002` | Metrics Dashboard | [DOMAIN-C] | Real-time | [Owner] |

---

## Data Classification

### Classification Matrix

| Class | Definition | Data Examples | Protection Requirements | Access |
|-------|-----------|---|---|---|
| **Public (P)** | Non-sensitive information, unrestricted access | Public names, general descriptions | None | All |
| **Internal (I)** | Internal information, restricted to employees | Internal IDs, organizational structure | Controlled access | Employees |
| **Confidential (C)** | Sensitive business or customer data | Financial data, strategy, contacts | Encryption, audit | Specific |
| **Restricted (R)** | Personal data (PII) and highly sensitive | CPF, email, password, transaction history | Strong encryption, minimal access | Essential |

### Classification by Asset

| Asset | Class | Classified Fields | Justification |
|-------|-------|---|---|
| [DOMAIN-A] | **I** (mostly) **R** (id, email) | `id` (R), `email` (R), `name` (I), `created_at` (I) | Contains PII and unique identifiers |
| [DOMAIN-B] | **C** (mostly) **R** (amount) | `amount` (C), `code` (C), `status` (I) | Financial data is sensitive |
| Cache Configuration | **I** | All | Domain information only |
| Report Queue | **C** | All | May contain confidential data |

---

## Ownership and Stewardship

### Ownership Matrix

| Asset | Owner | Steward | Availability SLA | Integrity SLA | Contact |
|-------|-------|---------|---|---|---------|
| [DOMAIN-A] | Engineering | [Name] | 99.9% | Zero corruption | [Email] |
| [DOMAIN-B] | Product | [Name] | 99.5% | Zero corruption | [Email] |
| [DOMAIN-C] | Operations | [Name] | 99% | Zero corruption | [Email] |
| Cache Configuration | DevOps | [Name] | 99.5% | Eventual consistency | [Email] |
| Report Queue | Data | [Name] | 99% | At-least-once delivery | [Email] |

### Definitions

| Term | Meaning |
|------|---------|
| **Owner** | Responsible for strategic decisions about the asset (retention, schema changes) |
| **Steward** | Responsible operationally for quality, updates, documentation |
| **Availability SLA** | Guaranteed uptime (% of time accessible) |
| **Integrity SLA** | Correctness guarantee (zero corruption, eventual consistency, etc.) |

---

## Data Lineage

### Flow: [DOMAIN-A] → Processing → Report

```
Input: [DOMAIN-A] (raw, all rows)
  ↓
P1: Validation
  - Filter: deleted_at IS NULL
  - Reject: status NOT IN ('active', 'inactive')
  ↓ 80% pass rate
P2: Enrichment
  - JOIN with [DOMAIN-C] for context
  - Calculate derived fields
  ↓ 100% output
P3: Aggregation
  - GROUP BY status, date
  - Calculate SUM(amount), AVG(amount)
  ↓ 5 rows output (aggregated)
Output: Aggregated Report A (view)
```

### Flow: [DOMAIN-B] → Cache → API Response

```
Input: [DOMAIN-B] (table)
  ↓
P2: Enrichment (load + cache)
  - Load from DB if cache miss
  - Store in Redis for 5 minutes
  ↓
Cache: Domain Configuration (Redis)
  ↓ TTL 5min
P4: Serialization (API)
  - Convert to JSON
  - Add metadata
  ↓
Output: API Response (to clients)
```

### Lineage Matrix

| Source | Transformations | Destination | Latency | Frequency |
|--------|---|---|---|---|
| [DOMAIN-A] raw | P1 (validate) → P2 (enrich) | Aggregated Report A | 5 min | Daily |
| [DOMAIN-B] raw | P2 (enrich) → Cache | API Response | < 100ms | Continuous |
| [DOMAIN-C] raw | P1 (validate) | Async Queue | < 1s | Continuous |
| External System | P1 (ingest) → P3 (store) | [DOMAIN-A] | < 5s | Hourly |

---

## Data Quality Rules

### Quality SLAs

| Asset | Metric | Target | Critical Alert | Verification |
|-------|--------|--------|---|---|
| [DOMAIN-A] | Completeness (NOT NULL) | 99% | < 95% | Daily |
| [DOMAIN-A] | Duplication (unique fields) | 0 | > 10 dupes | Daily |
| [DOMAIN-B] | Referential Integrity | 100% | < 99.5% | Continuous |
| [DOMAIN-B] | Consistency (amount > 0) | 100% | < 99.9% | Continuous |
| Aggregated Report A | Freshness | < 1 day | > 2 days | Daily |
| Cache | Hit Rate | > 80% | < 70% | Hourly |

### Validation Rules (Great Expectations / dbt tests)

#### [DOMAIN-A]

```yaml
tests:
  - not_null:
      columns: [id, name, created_at]
  - unique:
      columns: [id, name]
  - relationships:
      column: id
      to: [DOMAIN-C].entity_a_id
  - accepted_values:
      column: status
      values: ['active', 'inactive', 'archived']
  - custom_sql:
      query: "SELECT COUNT(*) FROM [DOMAIN-A] WHERE created_at > updated_at"
      expected_result: 0
```

#### [DOMAIN-B]

```yaml
tests:
  - not_null:
      columns: [id, entity_a_id, amount]
  - unique:
      columns: [id, code]
  - relationships:
      column: entity_a_id
      to: [DOMAIN-A].id
  - in_range:
      column: amount
      min: 0.01
      max: 999999.99
  - dbt_expectations:
      - expression: "amount > 0"
        where: "status != 'deleted'"
```

### Quality Alerts

| Rule | Severity | Action | Owner |
|------|----------|--------|-------|
| NOT NULL violation > 1% | CRITICAL | Halt pipeline, notify owner | [Owner] |
| Foreign key violation > 0.1% | HIGH | Log violation, flag records | [Owner] |
| Amount < 0 found | CRITICAL | Reject transaction, alert | [Owner] |
| Cache hit rate < 70% | MEDIUM | Investigate, adjust TTL | [Owner] |

---

## Retention and Archival

### Retention Policy

| Asset | Operational Retention | Audit Retention | Archival | Purge |
|-------|---|---|---|---|
| [DOMAIN-A] (active) | Indefinite | 7 years | Yes (annual) | Never delete historical records |
| [DOMAIN-B] (transactions) | 3 years | 7 years | Yes (annual) | Anonymize after retention |
| Cache | 5min - 24h | No | No | Auto TTL |
| Queue | 7 days (completed) | 30 days (DLQ) | No | Auto-purge |

### Archival Process

```
1. Annually on December 31
2. Export data > 2 years to Parquet
3. Compress with gzip
4. Store in S3 "ets-archive" bucket
5. Maintain manifest index
6. Retain access for queries (via Athena if necessary)
```

---

## Data Governance

### Change Checklists

Every schema or data change requires:

- ✓ Owner approval
- ✓ Downstream impact test (lineage)
- ✓ data-dictionary.md update
- ✓ Quality rules validation
- ✓ Stakeholder communication
- ✓ Staging execution first
- ✓ Rollback plan documented

### Governance Reports

- **Monthly:** Access audit, quality violations, compliance check
- **Quarterly:** Ownership review, lineage updates, classification assessment
- **Annual:** Retention/archival cycle, SLA updates, steward training

---

## Access Matrix by Classification

| Class | Public | Employees | Engineering | Owner | DPO |
|-------|--------|---|---|---|---|
| **Public** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Internal** | ✗ | ✓ | ✓ | ✓ | ✓ |
| **Confidential** | ✗ | ✗ | ✓ | ✓ | ✓ |
| **Restricted (PII)** | ✗ | ✗ | ✗ | ✓ | ✓ |

---


## O que fazer / O que nao fazer

**O que fazer:**
- Classificar sensibilidade de cada asset (PII, interno, publico)
- Atribuir owner e steward para cada dataset
- Definir politica de retencao com base legal
- Documentar linhagem completa (source -> transform -> consumer)

**O que nao fazer:**
- Nao listar assets sem owner
- Nao classificar tudo como "interno" por preguica
- Nao definir retencao sem base em compliance
- Nao ignorar cache e filas como data assets

## Next Steps

✅ Data Design complete
✅ Move to **implementation** (Execution using data catalog)
✅ Move to **api-spec** (Design APIs based on data assets)
