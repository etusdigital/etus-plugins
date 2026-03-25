---
doc_meta:
  id: sql
  display_name: Database Schema
  pillar: Data
  owner_role: Database Lead
  summary: Documents physical tables, keys, and indexes implementing the data model.
  order: 14
  gate: technical
  requires:
  - db
  - erd
  optional: []
  feeds:
  - dict
  - cat
uuid: <UUID>
version: 0.1.0
status: Draft
owners:
- <owner>
product: <product>
namespace: <namespace>
created: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
tags:
- Schema
- SQL
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Database Schema - [Project Name]

**Author:** [Your Name]  
**Date:** [YYYY-MM-DD]  
**Context:** MVP Internal Tool - Database Schema Documentation

## Database Schema Context

**Problem Statement:** See vis (Product Vision) for validated problem analysis.
**Database Requirements:** See db (Database Requirements) for schema context.
**Entity Relationships:** See erd (Entity Relationship Diagram) for data model structure.

**What problem does this database solve?**
[Describe the core problem that requires data storage/retrieval]

**Who will interact with this data?**

- Primary users: [User roles/personas]
- System actors: [Services/APIs that will access data]

**When is this data needed?**

- Real-time requirements: [Immediate access needs]
- Batch processing: [Scheduled/periodic needs]

**Where will this data be used?**

- Applications: [Web app, mobile, API, etc.]
- Environments: [Dev, staging, production]

**Why is this data structure necessary?**
[Business justification for the database design]

**How will the data flow?**

- Input sources: [Where data comes from]
- Processing: [How it's transformed]
- Output: [Where it goes]

**How much data volume?**

- Initial: [Expected records at launch]
- Growth: [Monthly/yearly projections]
- Peak load: [Concurrent users/transactions]

## 🚀 MVP Feature → Data Mapping

| Feature     | Data Requirements              | Entities Involved | Priority            |
| ----------- | ------------------------------ | ----------------- | ------------------- |
| [Feature 1] | [What data this feature needs] | [Tables/entities] | [Must/Should/Could] |
| [Feature 2] | [Data requirements]            | [Tables/entities] | [Must/Should/Could] |
| [Feature 3] | [Data requirements]            | [Tables/entities] | [Must/Should/Could] |

## 📊 Entity Discovery & Business Context

### Core Entities

**Entity 1: [Name]**

- Business purpose: [Why this entity exists]
- User journey touchpoint: [When users interact with this]
- Key attributes: [Critical fields]
- Business rules: [Validation/constraints from business logic]

**Entity 2: [Name]**

- Business purpose: [Why this entity exists]
- User journey touchpoint: [When users interact with this]
- Key attributes: [Critical fields]
- Business rules: [Validation/constraints]

### CRUD Operations Matrix

| Entity     | Create     | Read       | Update     | Delete     | Who Can Access |
| ---------- | ---------- | ---------- | ---------- | ---------- | -------------- |
| [Entity 1] | [Who/when] | [Who/when] | [Who/when] | [Who/when] | [Roles]        |
| [Entity 2] | [Who/when] | [Who/when] | [Who/when] | [Who/when] | [Roles]        |

### Relationships Map

- **[Entity A] ↔ [Entity B]**: [1:N/N:M] - [Business meaning: e.g., "Users can have multiple orders"]
- **[Entity B] ↔ [Entity C]**: [1:N/N:M] - [Business meaning]

## 🗄️ Physical Schema Design

### Database Configuration

- **Technology:** [PostgreSQL/MySQL/MongoDB/SQLite]
- **Version:** [If specific version required]
- **Environment:** [Development/Production considerations]

### Table Definitions

#### Table: `[table_name]`

**Business Purpose:** [What business entity/process this represents]

```sql
CREATE TABLE [table_name] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Core business fields
    [field_name] [TYPE] [NOT NULL/NULL] -- [Business meaning]
    [field_name] [TYPE] [CONSTRAINTS] -- [Business meaning]

    -- Relationships
    [foreign_key]_id UUID REFERENCES [table](id),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active'
);

-- Indexes for common queries
CREATE INDEX idx_[table]_[field] ON [table_name]([field]); -- [Query pattern this supports]
CREATE INDEX idx_[table]_status ON [table_name](status) WHERE status = 'active';
```

**Sample Data (for validation):**

```sql
-- Example record showing typical use case
INSERT INTO [table_name] ([fields]) VALUES
    ([values representing common scenario]);
```

### Data Validation Rules

| Field        | Business Rule                      | Database Constraint           |
| ------------ | ---------------------------------- | ----------------------------- |
| [field_name] | [e.g., "Must be unique per user"]  | `UNIQUE(user_id, field_name)` |
| [field_name] | [e.g., "Must be positive number"]  | `CHECK (field_name > 0)`      |
| [field_name] | [e.g., "Required for all records"] | `NOT NULL`                    |

## 🔒 Security & Privacy

**Sensitive Data Fields:**

- `[table.field]`: [PII/Sensitive] - [Encryption/hashing method]
- `[table.field]`: [PII/Sensitive] - [Protection approach]

**Access Control:**

- Public data: [Which tables/fields]
- Authenticated only: [Which tables/fields]
- Admin only: [Which tables/fields]

## ✅ MVP Validation Checklist

### Feature Coverage

- [ ] All MVP features have data support
- [ ] Each user story has required entities
- [ ] All business rules are enforceable
- [ ] Data relationships match business processes

### Technical Readiness

- [ ] Primary keys defined for all tables
- [ ] Foreign key relationships established
- [ ] Indexes for frequent query patterns
- [ ] Constraints match business rules

### Missing Requirements Check

- [ ] Are there user actions without data storage?
- [ ] Any business rules not captured in constraints?
- [ ] Audit/history requirements addressed?
- [ ] Search/filter requirements have indexes?

### Data Lifecycle

- [ ] How is data created? [Forms/APIs/imports]
- [ ] How is data updated? [Who can modify]
- [ ] How is data archived? [Soft delete/archive strategy]
- [ ] How is data deleted? [GDPR/compliance needs]

## 📝 Implementation Notes

**Critical Assumptions:**

- [List key assumptions about the data model]
- [Technology constraints assumed]

**Known Limitations:**

- [What this schema doesn't handle]
- [Features postponed post-MVP]

**Next Iterations:**

- [Planned schema evolution]
- [Performance optimizations needed]

---

**AI/Developer Notes:**

- Focus on MVP requirements only - avoid over-engineering
- This schema prioritizes rapid validation over optimization
- Security basics only - enhance before production
- Use provided SQL as starting point, adapt to specific database
