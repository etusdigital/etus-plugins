---
doc_meta:
  id: cat
  display_name: Data Catalog
  pillar: Data
  owner_role: Data Steward
  summary: Inventories data assets, lineage, governance policies, and access controls.
  order: 17
  gate: technical
  requires:
  - dict
  - sql
  optional: []
  feeds: []
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
- Catalog
- Governance
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Data Catalog - [System Name]

**Author:** [Your Name]  
**Date:** [YYYY-MM-DD]  
**Context:** SOLO - MVP Data Asset Governance & Discovery

## Problem Context

**Problem Statement:** See vis (Product Vision) for validated problem analysis.
**Data Requirements:** See data (Data Requirements) for data needs justification.
**Database Design:** See db (Database Requirements) for system context.

## 📊 MVP Data Assets (MoSCoW Prioritization)

### 🔴 MUST Have - [Primary Data Asset]

**WHAT** - Asset Overview

- **Type:** [Table/API/Stream/File]
- **Purpose:** [Critical business capability enabled]
- **References:** See Data Dictionary for field definitions

**WHY** - Business Criticality

- **User Story:** As a [role], I need [this data] to [achieve outcome]
- **Blocked Features:** [List features that cannot work without this]
- **Revenue Impact:** [Direct revenue/cost implications]

**WHO** - Ownership & Users

- **Data Owner:** [Name - accountable for quality]
- **Data Steward:** [Name - maintains documentation]
- **Primary Consumers:** [Teams/services using this data]

**WHERE** - Access Points

- **Location:** `[database.schema.table or endpoint]`
- **Dev Access:** [How to access in development]
- **Prod Access:** [Production access procedure]
- **Documentation:** [Link to detailed docs]

**WHEN** - Temporal Aspects

- **Update Frequency:** [Real-time/Hourly/Daily]
- **Data Freshness Requirements:** See nfr-2 for data latency requirements
- **Retention Period:** [How long data is kept]

**HOW** - Integration Guidance

- **Access Pattern:** [REST/GraphQL/SQL/Stream]
- **Authentication:** [Required credentials/tokens]
- **Rate Limits:** [Requests per second/minute]
- **Example:** See Backend Requirements be for implementation

**HOW MUCH** - Scale & Cost

- **Current Volume:** [Records/GB]
- **Growth Rate:** [X% monthly]
- **Storage Cost:** [$X/month]
- **Query Cost:** [$X per million queries]

---

### 🟡 SHOULD Have - [Secondary Data Asset]

**WHAT** - Asset Overview

- **Type:** [Table/API/Stream/File]
- **Purpose:** [Enhanced capability enabled]

**WHY** - Business Value

- **User Story:** As a [role], I need [this data] to [achieve outcome]
- **Enhanced Features:** [Features improved by this data]

**WHO** - Ownership

- **Data Owner:** [Name]
- **Primary Consumers:** [Teams/services]

**WHERE** - Access Points

- **Location:** `[identifier]`
- **Access Docs:** [Link]

**WHEN** - Timing

- **Update Frequency:** [Schedule]
- **Freshness Requirements:** See nfr-2 for data latency requirements

**HOW MUCH** - Scale

- **Volume:** [Size]
- **Growth:** [Trend]

---

### 🟢 COULD Have - [Nice-to-Have Asset]

[Asset description focusing on purpose and priority]

### ⚫ WON'T Have (This Sprint)

- [Data asset we're explicitly not including]
- [Another deferred asset with reason]

## 🔗 Data Lineage & Dependencies

### Critical Data Flow

```
[Source System] ──ETL──> [Raw Data Lake]
                              │
                              ├──Transform──> [User Analytics]
                              │                    │
                              └──Aggregate──> [Business Metrics]
                                                  │
                                                  └──> [Dashboard]
```

### Dependency Matrix

| Consumer    | Depends On     | Update Trigger | Impact if Stale |
| ----------- | -------------- | -------------- | --------------- |
| [Service A] | [Data Asset 1] | Real-time      | [Impact]        |
| [Service B] | [Data Asset 2] | Daily batch    | [Impact]        |

## 📈 Analytics & Tracking Requirements

### Marketing Funnel Events

| Event              | Asset        | Properties                  | Purpose     |
| ------------------ | ------------ | --------------------------- | ----------- |
| user.signup        | User Table   | {source, campaign, device}  | Attribution |
| user.activated     | Activity Log | {feature, time_to_activate} | Engagement  |
| purchase.completed | Transaction  | {amount, product, channel}  | Revenue     |

### Product Analytics Tracking

- **Page Views:** Track all navigation with referrer
- **Feature Usage:** Log interactions with key features
- **Error Events:** Capture failures for improvement
- **Performance Metrics:** Load times, API latency

### Data Collection Requirements

- All events must include: timestamp, user_id, session_id
- PII must be excluded from event properties
- Events buffered locally if connection fails
- Reference Data Dictionary for event schemas

## ✅ Governance Essentials

### Data Quality Standards

- **Completeness:** [Required fields must be non-null]
- **Accuracy:** [Validation rules enforced at source]
- **Consistency:** [Cross-system reconciliation daily]
- **Monitoring:** [Automated quality checks every hour]

### Access Control Matrix

| Asset     | Default Access | Request Via        | Performance Requirements |
| --------- | -------------- | ------------------ | ------------------------ |
| [Asset 1] | Read-only      | [Form/API]         | 1 day                    |
| [Asset 2] | No access      | [Manager approval] | 3 days                   |

### Privacy & Compliance

- **PII Classification:** [Which assets contain PII]
- **Retention Policy:** [Legal requirements]
- **Audit Requirements:** [Access logging needs]
- See Data Dictionary for field-level classifications

## 🚀 Developer Quick Start

### Discovery Checklist

1. Check this catalog for asset location
2. Review Data Dictionary for field definitions
3. Check Backend Requirements for API specs
4. Request access if needed (see matrix above)
5. Use provided integration pattern

### Common Integration Patterns

- **Batch Processing:** [Schedule and approach]
- **Real-time Sync:** [Streaming configuration]
- **Caching Strategy:** [What to cache and TTL]

### Troubleshooting Guide

| Symptom          | Likely Cause             | Solution               |
| ---------------- | ------------------------ | ---------------------- |
| No data returned | Access not granted       | Check access matrix    |
| Stale data       | Cache or replication lag | Check nfr-2            |
| Schema mismatch  | Version drift            | Verify Data Dictionary |

---
