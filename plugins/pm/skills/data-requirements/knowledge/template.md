---
doc_meta:
  id: data-requirements
  display_name: "Data Requirements"
  pillar: Design
  phase: Data Design
  sequence: 1
  updated: "2026-03-14"
  status: template
---

# Data Requirements

**Document:** data-requirements.md
**Responsibility:** Define data requirements, primary entities, and integrity rules
**Recipients:** Data engineers, database architects, implementation engineers

---
## Responsaveis

- **Owner:** Data/BI Lead
- **Contribuem:** Tech Lead, PM
- **Aprovacao:** Tech Lead


## Data Requirements Overview

[Descriptive narrative of data requirements]

- **Scope:** What data needs to be captured and stored?
- **Volume:** How many records per entity?
- **Frequency:** How often is data created/updated?
- **Retention:** How long must data be retained?
- **Access:** Who accesses the data and how often?

---

## Entity Inventory

### Primary Entities

| Entity | Description | Source | Creation Frequency | Annual Volume (est.) |
|--------|-------------|--------|---------------------|----------------------|
| [Entity 1] | [Description of purpose] | [User Story ref] | [Frequency] | [Volume] |
| [Entity 2] | [Description of purpose] | [User Story ref] | [Frequency] | [Volume] |

### Support Entities

| Entity | Description | Relationship |
|--------|-------------|-----------------|
| [Support Entity 1] | [Description] | Related to [Entity X] |
| [Support Entity 2] | [Description] | Related to [Entity Y] |

---

## Data Volume Estimates

### Annual Projection

| Entity | Creates/Year | Updates/Year | Storage Est. (GB) | Growth % |
|--------|--------------|------------------|-------------------------|---------------|
| [Entity 1] | [Volume] | [Volume] | [Estimate] | [Growth rate] |
| [Entity 2] | [Volume] | [Volume] | [Estimate] | [Growth rate] |

### Total Data

- **Size at rest:** [X] GB (year 1)
- **Size in 3 years:** [Y] GB
- **Peak IOPS (writes):** [Z] events/second
- **Peak IOPS (reads):** [Z] queries/second

---

## Integrity Rules

### Entity Constraints

#### [Entity 1]
- **Primary key:** [field]
- **Unique keys:** [fields]
- **Foreign keys:** [relationships]
- **Validation rules:**
  - [Field X] must be [constraint]
  - [Field Y] must be [constraint]

#### [Entity 2]
- **Primary key:** [field]
- **Unique keys:** [fields]
- **Foreign keys:** [relationships]
- **Validation rules:**
  - [Field X] must be [constraint]
  - [Field Y] must be [constraint]

### Business Constraints

- [Rule 1]: [Description of business constraint]
- [Rule 2]: [Description of business constraint]
- [Rule 3]: [Description of business constraint]

### Consistency Guarantees

| Guarantee | Mechanism | Verification |
|-----------|-----------|------------|
| [Description] | [How it is guaranteed] | [How it is verified] |
| Non-duplication | [Mechanism] | [Verification] |
| Referential consistency | [Mechanism] | [Verification] |

---

## Privacy and Compliance Requirements

### Data Classification

| Class | Fields | Retention | Regulation | Protection |
|--------|--------|----------|-------------|----------|
| **Public Data** | [List] | Indefinite | N/A | None |
| **Internal Data** | [List] | [Period] | LGPD | Controlled access |
| **Confidential Data** | [List] | [Period] | LGPD, SOC2 | Encryption at rest |
| **Restricted Data (PII)** | [List] | [Period] | LGPD, GDPR | Encryption, limited access |

### Compliance Requirements

- **LGPD (General Data Protection Law)**
  - Consent: [Policy]
  - Right to be forgotten: [Policy]
  - Portability: [Policy]

- **SOC2 (if applicable)**
  - Access audit: Enabled
  - Encryption at rest: [Algorithm]
  - Encryption in transit: TLS 1.3

- **GDPR (if applicable)**
  - Legal basis: [List]
  - Data processor: [Designated]

### Security Requirements

- **Encryption at rest:** [Algorithm, key management]
- **Encryption in transit:** [Protocol, certificate]
- **Access control:** [RBAC/ABAC model]
- **Audit:** [Audited fields, retention]

---

## Data Lifecycle

### Creation

| Entity | Source | Frequency | Validations | Notes |
|--------|--------|-----------|------------|-------|
| [Entity 1] | [Source] | [Frequency] | [Validations] | [Notes] |
| [Entity 2] | [Source] | [Frequency] | [Validations] | [Notes] |

### Transformation

| Process | Input | Output | Frequency | SLA |
|---------|-------|--------|-----------|-----|
| [Process 1] | [Entity] | [Entity] | [Frequency] | [SLA] |
| [Process 2] | [Entity] | [Entity] | [Frequency] | [SLA] |

### Archival

- **Policy:** Data older than [X] months is moved to archive storage
- **Format:** [Archive format]
- **Location:** [Storage destination]
- **Recoverability:** [Recovery SLA]

### Deletion / Purge

- **Policy:** Data older than [X] years is permanently deleted
- **Trigger:** [Events that trigger deletion]
- **Confirmation:** [Confirmation process before deletion]
- **Audit:** [Deletion log retained for X years]

### Backup & Recovery

- **Backup frequency:** [Frequency]
- **Backup retention:** [Period]
- **Recovery Time Objective (RTO):** [Time]
- **Recovery Point Objective (RPO):** [Time]

---

## Data Dependencies and Relationships

### Cross-Entity Data Flow

```
[Entity A] → [Process 1] → [Entity B] → [Process 2] → [Entity C]
```

- **[Entity A] → [Entity B]:** [Description of transformation]
- **[Entity B] → [Entity C]:** [Description of transformation]

### Data Consumers

| Consumer | Entities | Frequency | Acceptable Latency |
|----------|----------|-----------|-------------------|
| [System 1] | [Entities] | [Frequency] | [Latency] |
| [System 2] | [Entities] | [Frequency] | [Latency] |

---


## O que fazer / O que nao fazer

**O que fazer:**
- Listar todas as entidades com proposito de negocio
- Estimar volumes com ordens de grandeza realistas
- Documentar regras de integridade por tipo (NOT NULL, UNIQUE, FK)
- Classificar dados por sensibilidade (PII, interno, publico)

**O que nao fazer:**
- Nao pular para DDL aqui (isso e database-spec)
- Nao inventar entidades sem base em user stories
- Nao estimar volumes sem dados ou benchmarks
- Nao ignorar requisitos de retencao e compliance

## Next Steps

✅ Move to **erd** (Entity-Relationship Diagram)
✅ Move to **database-spec** (Database Specification)
