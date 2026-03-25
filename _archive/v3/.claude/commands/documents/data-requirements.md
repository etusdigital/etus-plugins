---
description: Generate Data Requirements Document (DRD)
argument-hint: [product-name]
allowed-tools: Task, Read, Write, Bash
model: sonnet
---

# Generate Data Requirements Document

Creating data requirements for: **$ARGUMENTS**

## Prerequisites

!`test -f docs/planning/user-stories.md && echo "✓ user-stories.md exists" || echo "⚠ Missing user stories (recommended to run /user-stories first)"`
!`test -d docs/planning/feature-specs && echo "✓ feature-specs/ exists" || echo "ℹ No feature specs yet (optional)"`

## Setup

!`mkdir -p docs/data && echo "✓ Created docs/design/"`

## Template Reference

Reference template: @.claude/skills/data-chain/knowledge/data-requirements.md

## Interactive Data Requirements

I'll help you define data requirements:

### Step 1: Review Functional Requirements

Read user stories and feature specs that involve data:

@docs/planning/user-stories.md

### Step 2: Data Entities (5W2H Analysis)

**Ask the user about each major data entity:**

For each entity (User, Product, Order, etc.):

1. **WHAT**: What data do we need to store about this entity?
2. **WHY**: Why do we need this entity? (business purpose)
3. **WHO**: Who creates/owns/accesses this data?
4. **WHEN**: When is this data created/updated/deleted?
5. **WHERE**: Where is this data used? (which features/flows)
6. **HOW**: How is this data accessed? (read patterns, write patterns)
7. **HOW MUCH**: How much data? (volume estimates, growth rate)

[Document each entity with 5W2H]

### Step 3: Data Quality Requirements

**Ask about data quality needs:**

1. **Accuracy**: How accurate must data be? Validation rules?
2. **Completeness**: What fields are required vs optional?
3. **Consistency**: How do we ensure data consistency across systems?
4. **Timeliness**: How fresh must data be? Real-time vs eventually consistent?
5. **Uniqueness**: What data must be unique? (email, username, IDs)

### Step 4: Data Governance

**Ask about data governance:**

1. **Ownership**: Who owns each data entity/domain?
2. **Access Control**: Who can read/write each entity?
3. **Retention**: How long do we keep data? Archival policies?
4. **Deletion**: Can data be deleted? Soft delete vs hard delete?
5. **Audit**: What data changes need to be audited/logged?

### Step 5: Compliance Requirements

**Ask about compliance needs:**

1. **Privacy regulations**: GDPR, CCPA, HIPAA requirements?
2. **PII handling**: What personally identifiable information exists?
3. **Data classification**: Public, internal, confidential, restricted?
4. **Right to be forgotten**: GDPR deletion requests?
5. **Data portability**: Export user data on request?
6. **Consent management**: Track user consent for data usage?

### Step 6: Confirm Data Requirements

"Here are the data requirements:

**Entities Identified:**
- User (email, name, preferences) - PII
- Product (name, price, inventory)
- Order (items, total, status)
[etc.]

**Data Quality:**
- Accuracy: Email validation, price constraints
- Uniqueness: Email, order ID
[etc.]

**Compliance:**
- GDPR compliant (EU users)
- PII: email, name, address
- Retention: 7 years for financial records
[etc.]

Are these data requirements complete?"

[Wait for confirmation]

## Generate Document

Generate `docs/design/data-requirements.md` (Data Requirements Document).

**Document Structure:**
- Data Entities Catalog
  - For each entity:
    - Entity name
    - 5W2H analysis
    - Attributes (high-level)
    - Volume estimates
    - Growth projections
- Data Quality Requirements
  - Accuracy requirements
  - Completeness rules
  - Consistency constraints
  - Timeliness needs
  - Uniqueness constraints
- Data Governance
  - Data ownership
  - Access control policies
  - Retention policies
  - Deletion policies
  - Audit requirements
- Compliance Requirements
  - Privacy regulations (GDPR, CCPA)
  - PII identification
  - Data classification
  - Right to be forgotten
  - Data portability
  - Consent management

## Validation

After generation:

!`test -f docs/design/data-requirements.md && echo "✓ data-requirements.md created" || echo "✗ Generation failed"`

**Data requirements checklist**:
!`if [ -f docs/design/data-requirements.md ]; then
  grep -ci "entity\|table" docs/design/data-requirements.md | xargs echo "Entities identified:"
  grep -ci "gdpr\|ccpa\|hipaa\|compliance" docs/design/data-requirements.md | xargs echo "Compliance mentions:"
  grep -ci "pii\|personal.*information" docs/design/data-requirements.md | xargs echo "PII references:"
fi`

## Next Steps

**Create entity relationship diagram**:
```
/erd
```

**Create database spec**:
```
/db-spec
```

Or run complete data chain:
```
/data-model
```

---

**Data requirements documented!** Entities, quality needs, governance, and compliance captured.
