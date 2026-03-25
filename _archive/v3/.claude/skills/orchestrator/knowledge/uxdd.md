---
doc_meta:
  id: ux
  display_name: UX Design Doc
  pillar: Design
  owner_role: UX Lead
  summary: Captures flows, interaction patterns, copy cues, and accessibility requirements.
  order: 20
  gate: design
  requires:
  - jour
  - uxs
  optional: []
  feeds:
  - wire
  - des
  - fe
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
- UX
- Design
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# UX Design Doc — [Product Name]

**Author:** [Your Name]  
**Date:** [YYYY-MM-DD]  
**Context:** SOLO - Single developer project

---

## 🔍 Design Context

**Problem Statement:** See vis (Product Vision) for validated problem analysis.
**User Requirements:** See jour (User Journey) and des (Design Requirements) for design context.

**Design Foundation:**

- **Problem Context:** Validated through upstream analysis in Product Vision
- **User Context:** Defined in User Personas and User Journey mapping
- **Requirements:** Specified in Design Requirements document

**Market Context:**

- What do competitors offer that users might expect?
- What industry standards exist?
- What emerging user expectations should we consider?

---

## 🎯 DEFINE - Problem Statement & Requirements

**Problem Statement Template:**

```txt
Problem: [User group] needs [solution capability]
because [current pain point] causes [negative outcome]

Opportunity: If we provide [solution approach]
then users will [positive outcome] and business will [business benefit]
```

**User Journey Gap Analysis:**

- **Current Journey:** [How users accomplish goals today]
- **Pain Points:** [Specific friction points and frustrations]
- **Opportunity Areas:** [Where improvements will have highest impact]
- **Success Criteria:** [How we'll measure improvement]

---

## 🚀 DEVELOP - Feature Extraction & User Stories

**Core Feature Matrix:**

- **Must-Have (MVP):** [Essential features for launch]
- **Should-Have (Phase 2):** [Important but not critical]
- **Could-Have (Future):** [Nice to have additions]
- **Won't-Have (Out of Scope):** [Explicitly excluded]

**User Story Format:**

```txt
As a [user type]
I want [capability/feature]
So that [benefit/outcome]

Acceptance Criteria:
- [Specific requirement 1]
- [Specific requirement 2]
- [Edge case handling]
```

**Interaction Requirements:**

- **Primary Actions:** [Core user interactions]
- **System Responses:** [Expected feedback/outcomes]
- **Error Handling:** [Error states and recovery flows]
- **Loading States:** [Progress indicators and messaging]

---

## 📋 DELIVER - Implementation Context

**Developer Handoff:**

- **User Flow Priority:** [Sequence for development]
- **UI States Required:** [Loading, empty, error, success states]
- **Cross-References:** See stor for detailed requirements, jour for flow analysis
- **Success Metrics:** [KPIs to track post-launch]

**MVP Scope Definition:**

- **Core Value:** [Minimum viable user value]
- **Technical Constraints:** [Development limitations to consider]
- **Future Roadmap:** [Post-MVP enhancement plan]
