---
doc_meta:
  id: erd
  display_name: Entity Relationship Diagram
  pillar: Data
  owner_role: Data Architect
  summary: Maps conceptual entities and relationships to guide schema design.
  order: 12
  gate: technical
  requires:
  - data
  optional: []
  feeds:
  - sql
  - be
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
- ERD
- DataModel
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Entity Relationship Diagram - [System Name]

**Author:** [Your Name]  
**Date:** [YYYY-MM-DD]  
**Context:** SOLO - Single developer project

## Entity Context

**Problem Statement:** See vis (Product Vision) for validated problem analysis.
**Data Requirements:** See data (Data Requirements) for data context.

**What** data needs to exist to solve the core problem?

- [List primary data entities required for MVP]

**Who** will interact with this data and how?

- [Primary users, admins, system actors]

**Where** will data be accessed, created, or modified?

- [User interfaces, API endpoints, background processes]

**When** do data creation, updates, and lifecycle events occur?

- [Timing of data operations, workflows]

**Why** are these entities essential for solving the user problem?

- [Business justification for each major entity]

**How** will data flow through the user journey?

- [High-level data flow and transformations]

**How much** data volume and complexity is expected?

- [Scale considerations for MVP vs future]

## 🎯 Problem & Context Statement

**User Problem:** [Clear problem statement this data model solves]
**Success Metrics:** [How will we measure if this data structure works]
**MVP Scope:** [What must work for launch vs future iterations]

## 👥 User Journey Data Mapping

**Journey Step 1:** [User action/screen]

- Data touched: [Entities involved]
- Operations: [Create/Read/Update/Delete]

**Journey Step 2:** [Next user action]

- Data touched: [Entities involved]
- Operations: [Create/Read/Update/Delete]

[Continue for key journey steps...]

## 🗄️ Database Model Overview

**System Name:** [Your application name]
**Database Type:** [Technology agnostic - specify in implementation]
**Purpose:** [What this data model supports]

## 🏗️ Entity Definitions

### [Entity Name] - MVP Core

**Business Purpose:** [Why this entity is essential for solving user problems]
**User Story Connection:** [Which user stories require this entity]

**Core Attributes:**

- **id** - Primary Key - Unique identifier
- **[essential_field]** - [Type] - [MVP requirement justification]
- **[essential_field]** - [Type] - [MVP requirement justification]
- **created_at/updated_at** - Timestamps

**Business Rules:** [Validation constraints that prevent user problems]

### [Entity Name] - MVP Supporting

**Business Purpose:** [How this supports core entities]
**User Story Connection:** [Related user stories]

**Core Attributes:**

- **id** - Primary Key
- **[foreign_key]** - Reference to core entity
- **[supporting_field]** - [Type] - [Supporting data purpose]

**Business Rules:** [Essential constraints only]

## 🔗 Key Relationships

### [Entity A] → [Entity B]

- **Business Logic:** [Why this relationship exists from user perspective]
- **Type:** [1:1, 1:N, N:M] - [User scenario that drives this]
- **Cascade:** [What happens when parent is deleted - business impact]

## 🎨 ERD Diagram

```mermaid
erDiagram
    [CORE_ENTITY] {
        id PK
        [essential_fields]
        created_at
        updated_at
    }

    [SUPPORTING_ENTITY] {
        id PK
        [core_entity_id] FK
        [supporting_fields]
        created_at
        updated_at
    }

    [CORE_ENTITY] ||--o{ [SUPPORTING_ENTITY] : "[business relationship]"
```

## ✅ MVP Validation Checklist

**Discovery Completeness:**

- [ ] All user stories have supporting data entities
- [ ] Each entity has clear business justification
- [ ] User journey data touchpoints are mapped
- [ ] Requirements are validated for core entities

**Technical Completeness:**

- [ ] No orphaned entities (all connected to user value)
- [ ] Relationships support required user flows
- [ ] Business rules prevent common user errors
- [ ] Data model supports success metrics measurement

**Developer Context:**

- [ ] Each entity's business purpose is clear
- [ ] Relationship business logic is documented
- [ ] MVP scope vs future scope is defined

---
