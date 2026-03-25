---
doc_meta:
  id: data
  display_name: Data Requirements
  pillar: Data
  owner_role: Data Architect
  summary: Defines data scope, sources, quality rules, privacy posture, and retention
    policies.
  order: 11
  gate: technical
  requires:
  - srs
  optional: []
  feeds:
  - flow
  - db
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
- Data
- Requirements
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Data Requirements — [Project Name]

**Version:** [1.0]  
**Date:** [YYYY-MM-DD]  
**Status:** [Discovery/Validated/Approved]

## 🎯 Problem-Data Alignment

**Problem We're Solving:** See vis (Product Vision) for validated problem analysis.

**Data Context:** See srs (Software Requirements) for system context and data flow requirements.

**Without This Data:** [What fails or can't function - be specific]

## 📊 MVP Data Requirements

### Must Have (Day 1)

- [Critical data entity #1]: [Why essential for MVP]
- [Critical data entity #2]: [Why essential for MVP]
- [Critical validation]: [What breaks without this]
- [Core data flow]: [Minimum viable pipeline]

### Nice to Have (Post-MVP)

- [Enhanced feature data]: [Future improvement]
- [Analytics data]: [Not critical for launch]
- [Additional integrations]: [Can be added later]

## 👤 User Stories & Data Needs

### Story 1: [Primary User Flow]

**As a** [user type], **I need to** [action] **so that** [outcome]

- **Data Required:** [Specific fields/entities needed]
- **Validation Rules:** [What must be checked]
- **Edge Cases:** [Empty states, errors, limits]
- **Success Criteria:** [How we know it works]

### Story 2: [Secondary User Flow]

**As a** [user type], **I need to** [action] **so that** [outcome]

- **Data Required:** [Specific fields/entities needed]
- **Validation Rules:** [What must be checked]
- **Edge Cases:** [Empty states, errors, limits]
- **Success Criteria:** [How we know it works]

## 🏗️ Data Entities (MVP)

### Entity: [Primary Entity Name]

**Purpose:** [What this represents in the system]
**Source:** [Where this data comes from]

| Field        | Type           | Required | Validation | Notes       |
| ------------ | -------------- | -------- | ---------- | ----------- |
| id           | integer/string | Yes      | Unique     | Primary key |
| [field_name] | [type]         | Yes/No   | [Rule]     | [Context]   |
| [field_name] | [type]         | Yes/No   | [Rule]     | [Context]   |

### Entity: [Secondary Entity Name]

**Purpose:** [What this represents in the system]
**Source:** [Where this data comes from]

| Field        | Type           | Required | Validation | Notes       |
| ------------ | -------------- | -------- | ---------- | ----------- |
| id           | integer/string | Yes      | Unique     | Primary key |
| [field_name] | [type]         | Yes/No   | [Rule]     | [Context]   |

**Relationships:**

- [Entity A] → [Entity B]: [Relationship type and purpose]

## 🔄 Data Flow (MVP)

### Primary Flow: [Main User Action]

1. **Input:** User provides [data] via [interface/API]
2. **Validate:** Check [rules/constraints]
3. **Process:** [Transform/calculate/enrich]
4. **Store:** Save to [entity/table]
5. **Output:** Return [format] for [purpose]

### Error Handling:

- **Invalid Input:** [How to handle]
- **Missing Data:** [Default behavior]
- **System Failure:** [Fallback approach]

## 🚀 Implementation Roadmap

### Phase 1: Core Data (Week 1)

- [ ] Create [primary entity/table]
- [ ] Set up [main data source connection]
- [ ] Implement [critical validation rules]
- [ ] Build [essential CRUD operations]

### Phase 2: User Flows (Week 2)

- [ ] Connect [user story 1] to data layer
- [ ] Implement [data transformations]
- [ ] Add [error handling]
- [ ] Test with [realistic data volume]

### Before Launch:

- [ ] Verify all required fields populated
- [ ] Test edge cases with sample data
- [ ] Confirm data persistence works
- [ ] Document any data migrations needed

## ⚠️ Risks & Mitigations

### Data Quality Risks

| Risk              | Impact             | Mitigation            |
| ----------------- | ------------------ | --------------------- |
| [Incomplete data] | [Feature breaks]   | [Validation/defaults] |
| [Invalid formats] | [Processing fails] | [Input sanitization]  |

### Technical Risks

| Risk           | Impact             | Mitigation         |
| -------------- | ------------------ | ------------------ |
| [Data loss]    | [User frustration] | [Regular backups]  |
| [Slow queries] | [Poor UX]          | [Index key fields] |

## 📋 Quick Reference

### Data Sources

- **Primary:** [Main data input method]
- **Secondary:** [Backup or additional source]

### Key Validations

- [Field]: [Rule] - [Why important]
- [Field]: [Rule] - [Why important]

### Success Metrics

- [ ] All user stories have data support
- [ ] Core entities handle expected volume
- [ ] Data flows complete without errors
- [ ] Edge cases handled gracefully
