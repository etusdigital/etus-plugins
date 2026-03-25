---
doc_meta:
  id: data-dictionary
  display_name: "Data Dictionary"
  pillar: Design
  phase: Data Design
  sequence: 4
  updated: "2026-03-14"
  status: template
---

# Data Dictionary

**Document:** data-dictionary.md
**Responsibility:** Define fields (dict.*), events (ev.*), and enumerated types (SINGLE SOURCE OF TRUTH)
**Recipients:** Developers, analysts, data engineers, QA

---
## Responsaveis

- **Owner:** Data/BI Lead
- **Contribuem:** Tech Lead, PM, Analistas
- **Aprovacao:** Tech Lead


## Table of Contents

- [Field Dictionary](#field-dictionary)
- [Event Catalog](#event-catalog)
- [Enumerated Types](#enumerated-types)
- [Traceability Matrix](#traceability-matrix)
- [Integrity Validation](#integrity-validation)
- [Next Steps](#next-steps)

---

## Field Dictionary

### Domain: [DOMAIN-A]

#### dict.[DOMAIN-A].id

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-A].id` |
| **Name** | ID of entity [DOMAIN-A] |
| **Data Type** | UUID |
| **Size** | 36 characters (RFC 4122) |
| **Nullable** | No |
| **Default** | `gen_random_uuid()` |
| **Constraints** | PRIMARY KEY, UNIQUE |
| **Example** | `550e8400-e29b-41d4-a716-446655440001` |
| **Description** | Unique identifier auto-generated (random UUIDv4) |
| **Use Cases** | Reference in FKs, logs, audit |
| **Notes** | Immutable after creation, never reused |

---

#### dict.[DOMAIN-A].name

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-A].name` |
| **Name** | Entity name |
| **Data Type** | VARCHAR(255) |
| **Nullable** | No |
| **Default** | — |
| **Constraints** | UNIQUE, NOT NULL |
| **Example** | `"Q1 2026 Billing"` |
| **Description** | Unique and descriptive name for the entity |
| **Use Cases** | Display in UI, search by name |
| **Notes** | Case-sensitive, spaces allowed |

---

#### dict.[DOMAIN-A].description

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-A].description` |
| **Name** | Description |
| **Data Type** | TEXT |
| **Nullable** | Yes |
| **Default** | NULL |
| **Constraints** | — |
| **Example** | `"Billing data for the first quarter of 2026"` |
| **Description** | Long text description (no practical limit) |
| **Use Cases** | Additional context in UI, documentation |
| **Notes** | Can contain line breaks, HTML not allowed |

---

#### dict.[DOMAIN-A].status

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-A].status` |
| **Name** | Entity status |
| **Data Type** | VARCHAR(50) |
| **Nullable** | No |
| **Default** | `'active'` |
| **Constraints** | CHECK (status IN ('active', 'inactive', 'archived')) |
| **Example** | `"active"` |
| **Description** | State of the entity in its lifecycle |
| **Use Cases** | Query filters, conditional logic |
| **Enum** | See `enum.entity_status` |
| **Notes** | Values: active, inactive, archived |

---

#### dict.[DOMAIN-A].created_at

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-A].created_at` |
| **Name** | Creation Timestamp |
| **Data Type** | TIMESTAMP WITH TIME ZONE |
| **Nullable** | No |
| **Default** | `CURRENT_TIMESTAMP` |
| **Constraints** | NOT NULL |
| **Example** | `2026-03-14 14:30:00+00:00` |
| **Description** | Exact moment of record creation in UTC |
| **Use Cases** | Audit, sorting, range queries |
| **Notes** | Immutable, always in UTC |

---

#### dict.[DOMAIN-A].updated_at

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-A].updated_at` |
| **Name** | Update Timestamp |
| **Data Type** | TIMESTAMP WITH TIME ZONE |
| **Nullable** | No |
| **Default** | `CURRENT_TIMESTAMP` |
| **Constraints** | NOT NULL, CHECK (updated_at >= created_at) |
| **Example** | `2026-03-14 15:45:00+00:00` |
| **Description** | Moment of most recent record update |
| **Use Cases** | Audit, cache invalidation, replication |
| **Notes** | Auto-updated on UPDATE, always >= created_at |

---

### Domain: [DOMAIN-B]

#### dict.[DOMAIN-B].entity_a_id

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-B].entity_a_id` |
| **Name** | Reference ID to [DOMAIN-A] |
| **Data Type** | UUID |
| **Nullable** | No |
| **Default** | — |
| **Constraints** | FOREIGN KEY → [DOMAIN-A].id |
| **Example** | `550e8400-e29b-41d4-a716-446655440001` |
| **Description** | Referential integrity reference to parent entity |
| **Use Cases** | JOINs, filtering, association |
| **Notes** | Deleting [DOMAIN-A] cascade-deletes related records |

---

#### dict.[DOMAIN-B].code

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-B].code` |
| **Name** | Unique Code |
| **Data Type** | VARCHAR(100) |
| **Nullable** | No |
| **Default** | — |
| **Constraints** | UNIQUE, NOT NULL |
| **Example** | `"INV-2026-001234"` |
| **Description** | Unique human-readable code (not UUID) |
| **Use Cases** | Reference in UIs, export, replication |
| **Pattern** | Sequential: `INV-YYYY-XXXXX` |
| **Notes** | Immutable, case-insensitive in business logic |

---

#### dict.[DOMAIN-B].amount

| Property | Value |
|----------|-------|
| **ID** | `dict.[DOMAIN-B].amount` |
| **Name** | Currency Amount |
| **Data Type** | NUMERIC(15, 2) |
| **Nullable** | No |
| **Default** | — |
| **Constraints** | CHECK (amount > 0) |
| **Example** | `1234.56` |
| **Description** | Monetary value in 2 decimal places |
| **Unit** | BRL (Brazilian Real) |
| **Use Cases** | Calculations, summations, reporting |
| **Notes** | Always positive, always 2 decimals |

---

## Event Catalog

### ev.[DOMAIN-A].created

| Property | Value |
|----------|-------|
| **Event ID** | `ev.[DOMAIN-A].created` |
| **Name** | [DOMAIN-A] Created |
| **Trigger** | INSERT in [DOMAIN-A] |
| **Frequency** | [Estimate: X events/day] |
| **Latency** | < 100ms (synchronous) |
| **Schema** | See payload below |
| **Consumers** | [System 1], [System 2] |
| **Retention** | 90 days (audit log) |

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "ev.[DOMAIN-A].created",
  "timestamp": "2026-03-14T14:30:00Z",
  "entity": {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "status": "active"
  },
  "actor": {
    "user_id": "uuid",
    "ip_address": "1.2.3.4"
  }
}
```

---

### ev.[DOMAIN-A].updated

| Property | Value |
|----------|-------|
| **Event ID** | `ev.[DOMAIN-A].updated` |
| **Name** | [DOMAIN-A] Updated |
| **Trigger** | UPDATE in [DOMAIN-A] with changes |
| **Frequency** | [Estimate: Y events/day] |
| **Latency** | < 100ms (synchronous) |
| **Schema** | See payload below |
| **Consumers** | [System 1], Cache Invalidator |
| **Retention** | 90 days (audit log) |

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "ev.[DOMAIN-A].updated",
  "timestamp": "2026-03-14T15:45:00Z",
  "entity_id": "uuid",
  "changes": {
    "status": {"from": "active", "to": "inactive"},
    "updated_at": "2026-03-14T15:45:00Z"
  },
  "actor": {
    "user_id": "uuid",
    "ip_address": "1.2.3.4"
  }
}
```

---

### ev.[DOMAIN-A].deleted

| Property | Value |
|----------|-------|
| **Event ID** | `ev.[DOMAIN-A].deleted` |
| **Name** | [DOMAIN-A] Deleted |
| **Trigger** | DELETE in [DOMAIN-A] (soft delete, deleted_at set) |
| **Frequency** | [Estimate: Z events/day] |
| **Latency** | < 100ms (synchronous) |
| **Schema** | See payload below |
| **Consumers** | Cache Invalidator, Audit Log |
| **Retention** | 1 year (audit log) |

**Payload:**
```json
{
  "event_id": "uuid",
  "event_type": "ev.[DOMAIN-A].deleted",
  "timestamp": "2026-03-14T16:00:00Z",
  "entity_id": "uuid",
  "entity_snapshot": {
    "id": "uuid",
    "name": "string"
  },
  "actor": {
    "user_id": "uuid",
    "ip_address": "1.2.3.4"
  }
}
```

---

## Enumerated Types

### enum.entity_status

| Value | Description | Transition Flow |
|-------|-------------|-----------------|
| `active` | Entity in normal operation | Created as active; can transition to inactive or archived |
| `inactive` | Entity temporarily disabled | Can return to active or go to archived |
| `archived` | Entity kept for historical reference | Final state (no outgoing transition) |

**State Machine:**
```
CREATE → active ↔ inactive → archived (TERMINAL)
```

---

### enum.payment_method

| Value | Description | Processor | Fee |
|-------|-------------|-----------|-----|
| `credit_card` | Credit card | Stripe | 2.9% + R$0.30 |
| `debit_card` | Debit card | Stripe | 1.99% + R$0.30 |
| `pix` | Instant PIX | Direct bank | Free |
| `boleto` | Bank ticket | Direct bank | R$5.00 |
| `wire_transfer` | Bank wire | Direct bank | R$15.00 |

---

## Traceability Matrix

| Document | ID | Dependencies |
|----------|--|----|
| user-stories.md | US-# | Uses dict.* and ev.* to describe data |
| api-spec.md | [endpoint] | References dict.* for schemas |
| implementation | [code] | Uses dict.* and ev.* for type generation |

---

## Integrity Validation

✓ All fields in database-spec.md have dict.* entry
✓ All events in user-stories.md have ev.* entry
✓ All enums mentioned have enum.* defined
✓ No orphaned fields (not referenced)
✓ No orphaned events (not consumed)

---


## O que fazer / O que nao fazer

**O que fazer:**
- Atribuir dict.* ID para cada campo (format: dict.[dominio].[campo])
- Incluir tipo, range valido, e significado de negocio
- Documentar todos os valores de enum com descricao
- Mapear dict.* para colunas do banco (cross-reference)

**O que nao fazer:**
- Nao definir semantica de campos em outros documentos (SST e aqui)
- Nao deixar campos sem descricao de negocio
- Nao criar dict.* IDs duplicados
- Nao omitir campos deprecados (documentar com data de sunset)

## Next Steps

✅ Move to **data-flow-diagram** (Data flow between systems)
✅ Move to **api-spec** (Endpoints based on dict.*)
