---
doc_meta:
  id: erd
  display_name: "Entity-Relationship Diagram"
  pillar: Design
  phase: Data Design
  sequence: 2
  updated: "2026-03-14"
  status: template
---

# Entity-Relationship Diagram (ERD)

**Document:** erd.md
**Responsibility:** Visualize data structure with relationships and cardinalities
**Recipients:** Data architects, database engineers, developers

---
## Responsaveis

- **Owner:** Data/BI Lead
- **Contribuem:** Tech Lead, PM
- **Aprovacao:** Tech Lead


## Entity-Relationship Diagram

### Complete Diagram

```mermaid
erDiagram
    [ENTITY-A] ||--o{ [ENTITY-B] : contains
    [ENTITY-A] ||--|| [ENTITY-C] : has
    [ENTITY-B] }o--|| [ENTITY-D] : references
    [ENTITY-C] ||--|| [ENTITY-E] : related-to

    [ENTITY-A] {
        string id PK
        string name UK
        text description
        timestamp created_at
    }

    [ENTITY-B] {
        string id PK
        string entity_a_id FK
        string code UK
        decimal amount
        timestamp created_at
    }

    [ENTITY-C] {
        string id PK
        string entity_a_id FK "UNIQUE"
        string status
        timestamp updated_at
    }

    [ENTITY-D] {
        string id PK
        string entity_b_id FK
        text content
    }

    [ENTITY-E] {
        string id PK
        string entity_c_id FK
        string metadata
    }
```

### Symbol Legend

| Symbol | Meaning | Cardinality |
|--------|---------|-------------|
| `\|\|` | One | Exactly one |
| `}o` | Many | Zero or more |
| `o{` | Many | Optional zero or more |
| `\|\|--` | One to One | Both mandatory |
| `\|\|--o{` | One to Many | One mandatory, many optional |

---

## Entity Descriptions

### [ENTITY-A] - [Descriptive Name]

**Responsibility:** [Description of purpose]

**Key fields:**
- `id` (PK): Unique identifier
- `name` (UK): Alternative unique field
- `created_at`: Creation timestamp

**Invariants:**
- One [ENTITY-A] can have many [ENTITY-B] associated
- One [ENTITY-A] has exactly one [ENTITY-C] related

---

### [ENTITY-B] - [Descriptive Name]

**Responsibility:** [Description of purpose]

**Key fields:**
- `id` (PK): Unique identifier
- `entity_a_id` (FK): Reference to [ENTITY-A]
- `code` (UK): Unique code

**Invariants:**
- Many [ENTITY-B] belong to one [ENTITY-A]
- Each [ENTITY-B] must reference a valid [ENTITY-D]

---

### [ENTITY-C] - [Descriptive Name]

**Responsibility:** [Description of purpose]

**Key fields:**
- `id` (PK): Unique identifier
- `entity_a_id` (FK, UNIQUE): Exclusive reference to [ENTITY-A]

**Invariants:**
- One-to-one relationship with [ENTITY-A]
- One [ENTITY-C] has exactly one [ENTITY-E] related

---

### [ENTITY-D] - [Descriptive Name]

**Responsibility:** [Description of purpose]

**Key fields:**
- `id` (PK): Unique identifier
- `entity_b_id` (FK): Reference to [ENTITY-B]

**Invariants:**
- Many [ENTITY-D] can reference one [ENTITY-B]

---

### [ENTITY-E] - [Descriptive Name]

**Responsibility:** [Description of purpose]

**Key fields:**
- `id` (PK): Unique identifier
- `entity_c_id` (FK): Reference to [ENTITY-C]

**Invariants:**
- Relates to [ENTITY-C] in one-to-one relationship

---

## Relationship Matrix

| Entity A | Entity B | Type | Cardinality | Description |FK Name |
|----------|----------|------|-------------|-----------|---------|
| [ENTITY-A] | [ENTITY-B] | Composition | 1:N | One [A] contains many [B] | `entity_a_id` |
| [ENTITY-A] | [ENTITY-C] | Association | 1:1 | One [A] has one [C] | `entity_a_id` |
| [ENTITY-B] | [ENTITY-D] | Reference | N:1 | Many [B] reference one [D] | `entity_b_id` |
| [ENTITY-C] | [ENTITY-E] | Association | 1:1 | One [C] has one [E] | `entity_c_id` |

---

## Cardinality Rules

### One-to-One (1:1)

**Example:** [ENTITY-A] ↔ [ENTITY-C]

- One [ENTITY-A] has exactly one [ENTITY-C]
- One [ENTITY-C] belongs to exactly one [ENTITY-A]
- FK in [ENTITY-C] must have UNIQUE constraint
- Deleting [ENTITY-A] must delete [ENTITY-C] (cascade) or reject

### One-to-Many (1:N)

**Example:** [ENTITY-A] → [ENTITY-B]

- One [ENTITY-A] can have many [ENTITY-B]
- One [ENTITY-B] belongs to exactly one [ENTITY-A]
- FK in [ENTITY-B] references PK of [ENTITY-A]
- Deleting [ENTITY-A] must handle [ENTITY-B] (cascade, orphan, etc.)

### Many-to-Many (M:N)

**Example:** [If applicable]

- Many [ENTITY-X] can be related to many [ENTITY-Y]
- Requires intermediate junction table
- Both FKs in junction table form composite PK

---

## Relationship Validation

✓ All relationships have defined cardinality
✓ All FKs reference valid PKs
✓ No dangerous cycles (except valid self-references)
✓ One-to-one relationships have appropriate UNIQUE constraints
✓ Alternate keys (UK) documented

---


## O que fazer / O que nao fazer

**O que fazer:**
- Definir cardinalidade em todos os relacionamentos
- Resolver M:N com tabelas de juncao explicitas
- Incluir apenas atributos-chave no diagrama (PK, FK, UK)
- Validar que nao ha ciclos perigosos

**O que nao fazer:**
- Nao incluir todos os campos no diagrama (fica ilegivel)
- Nao deixar relacionamentos sem cardinalidade
- Nao criar entidades sem correspondencia no data-requirements
- Nao ignorar self-references ou relacionamentos recursivos

## Next Steps

✅ Move to **database-spec** (SQL DDL based on this ERD)
✅ Move to **data-dictionary** (Field definitions)
