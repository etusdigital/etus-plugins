---
description: Generate Entity Relationship Diagram (ERD)
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Entity Relationship Diagram

Creating ERD for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/design/data-requirements.md && echo "✓ data-requirements.md exists" || echo "⚠ Missing data requirements (recommended to run /data-requirements first)"`

## Setup

!`mkdir -p docs/data && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/data-chain/knowledge/erd.md

## Interactive ERD Design

I'll help you design entity relationships:

### Step 1: Review Data Requirements

Read entities from data requirements:

@docs/design/data-requirements.md

### Step 2: Entity Definitions

**For each entity, ask:**

Let's define **[Entity Name]**:

1. **Attributes**: What fields/columns does this entity have?
   - Field name
   - Data type (string, integer, boolean, date, etc.)
   - Required vs optional
   - Default values
2. **Primary Key**: What uniquely identifies this entity?
3. **Description**: What does this entity represent?

[Define all entities with attributes]

### Step 3: Relationships

**Ask about relationships between entities:**

How are entities related?

**For each relationship:**
1. **Entities involved**: Which two entities?
2. **Relationship type**:
   - One-to-One (1:1)
   - One-to-Many (1:N)
   - Many-to-Many (M:N)
3. **Cardinality**: Required or optional on each side?
   - Mandatory (1 or more)
   - Optional (0 or more)
4. **Relationship name**: How to describe this connection?

**Examples:**
- User (1) → (N) Order: "A user can have multiple orders"
- Order (N) → (M) Product: "An order contains multiple products, a product appears in multiple orders"
- User (1) → (1) Profile: "A user has one profile"

[Document all relationships]

### Step 4: Mermaid ERD Diagram

**Confirm the ERD structure:**

"Here's the ERD I'll create:

**Entities:**
- User (id PK, email, name, created_at)
- Profile (id PK, user_id FK, bio, avatar_url)
- Order (id PK, user_id FK, total, status, created_at)
- OrderItem (id PK, order_id FK, product_id FK, quantity, price)
- Product (id PK, name, price, inventory)

**Relationships:**
- User 1 → N Order (one user, many orders)
- User 1 → 1 Profile (one user, one profile)
- Order 1 → N OrderItem (one order, many items)
- Product 1 → N OrderItem (one product, many order items)
- Order N → M Product (through OrderItem)

Does this ERD structure match your data model?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/erd.md` with Mermaid ERD diagram.

**Document Structure:**
- Entity Catalog
  - For each entity:
    - Entity name
    - Description
    - Attributes (field name, type, required/optional, description)
    - Primary key
    - Foreign keys
- Relationship Catalog
  - For each relationship:
    - Entities involved
    - Relationship type (1:1, 1:N, M:N)
    - Cardinality (mandatory/optional)
    - Description
- Mermaid ERD Diagram
  ```mermaid
  erDiagram
    USER ||--o{ ORDER : places
    USER ||--|| PROFILE : has
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "appears in"

    USER {
      int id PK
      string email
      string name
      datetime created_at
    }

    ORDER {
      int id PK
      int user_id FK
      decimal total
      string status
      datetime created_at
    }
  ```

## Validation

After generation:

!`test -f docs/design/erd.md && echo "✓ erd.md created" || echo "✗ Generation failed"`

**ERD checklist**:
!`if [ -f docs/design/erd.md ]; then
  grep -ci "entity\|table" docs/design/erd.md | xargs echo "Entities defined:"
  grep -ci "one-to-one\|one-to-many\|many-to-many\|1:1\|1:N\|M:N" docs/design/erd.md | xargs echo "Relationships defined:"
  grep -ci "mermaid" docs/design/erd.md | xargs echo "Mermaid diagrams:"
fi`

## Next Steps

**Create database specification**:
```
/db-spec
```

Or run complete data chain:
```
/data-model
```

---

**ERD generated!** Entity structure and relationships documented with Mermaid diagram.
