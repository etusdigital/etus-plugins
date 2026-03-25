---
doc_meta:
  id: wire
  display_name: Wireframes
  pillar: Design
  owner_role: UX Lead
  summary: Defines screen layouts, UI states, and flow transitions across devices.
  order: 22
  gate: design
  requires:
  - uxs
  - ux
  - des
  optional: []
  feeds:
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
- Wireframes
- UI
- ETUS
ai_template_variables:
- product
- owner
- namespace
---

# Solo Wireframes - [Product Name]

**Author:** [Your Name] | **Date:** [YYYY-MM-DD]

## Wireframe Context

**Problem Statement:** See vis (Product Vision) for validated problem analysis.
**Design Requirements:** See des (Design Requirements) for component context.

### Problem Statement & Validation
- **Why:** What core problem does this solve? What's the business value?
- **What:** What are the essential user needs and MVP feature requirements?
- **Who:** Who are the primary users? What personas and pain points?
- **Where:** In what context/environment will users interact with this?
- **When:** At what journey touchpoints? What triggers usage?
- **How:** What interaction patterns solve the user problems?
- **How Much:** What's the MVP scope? Resource/time constraints?

### User Journey Integration
- **Journey Stage:** [Awareness/Consideration/Decision/Onboarding/Usage/Advocacy]
- **Entry Point:** How users discover/arrive at this screen
- **User Goal:** What users want to accomplish here
- **Success Criteria:** How we measure goal completion
- **Exit Actions:** Where users go next or leave

## 📱 Core Wireframe Specifications

### Screen 1: [SCREEN_NAME] - [Journey Stage]
**Purpose:** [One sentence describing user goal]  
**Priority:** High/Medium/Low  
**User Story:** "As a [user type], I want to [action] so that [benefit]"

**Layout Structure:**
- Header: [Navigation, branding, key actions]
- Main Content: [Primary user task area]  
- Secondary: [Supporting info, related actions]
- Footer: [Secondary nav, legal]

**Key Components:**
1. **[Component Name]** - [Function] | [Responsive behavior]
2. **[Component Name]** - [Function] | [Mobile adaptation]
3. **[Component Name]** - [Function] | [Interaction pattern]

**UI States:** Default | Loading | Empty | Error | Success

### Screen 2: [SCREEN_NAME] - [Journey Stage]
**Purpose:** [One sentence describing user goal]  
**Priority:** High/Medium/Low  
**User Story:** "As a [user type], I want to [action] so that [benefit]"

**User Flow Connection:** [Previous screen] → **Current** → [Next screen]

**Core Interactions:**
- Primary Action: [Main CTA and expected outcome]
- Secondary Actions: [Supporting actions and navigation]
- Error Recovery: [How users recover from failures]

**Mobile Adaptations:**
- Navigation: [Touch-optimized patterns]
- Content: [Priority content stacking]
- Interactions: [Gesture support, touch targets]

## 👥 Developer Context Extraction

### User Stories from Wireframes
**Epic:** [High-level feature description]

**Stories:**
1. "As a [user], I want [functionality] so that [value]"
   - **Acceptance Criteria:** See User Stories us-1 for detailed acceptance criteria
   - **Components Needed:** [List of UI components]

2. "As a [user], I want [functionality] so that [value]"
   - **Acceptance Criteria:** See User Stories us-2 for detailed acceptance criteria
   - **Data Requirements:** [API endpoints, data models]

### MVP Feature Prioritization
**Must Have (P0):** Essential for core user journey  
**Should Have (P1):** Important for user experience  
**Could Have (P2):** Nice-to-have for future iterations  

### Technical Requirements
- **Responsive Breakpoints:** Mobile (320px+) | Tablet (768px+) | Desktop (1024px+)
- **Key Interactions:** [Click/tap patterns, form behaviors, navigation]
- **Data Dependencies:** [Required APIs, local storage, state management]
- **Performance Needs:** [Loading targets, bundle size limits]

## ✅ Discovery Validation Checklist

### Requirements Coverage
- [ ] Core user problem clearly defined and validated
- [ ] User journey touchpoints mapped to wireframes
- [ ] MVP scope defined with clear priorities
- [ ] Success metrics and acceptance criteria documented
- [ ] Technical constraints and dependencies identified

### User Experience Validation  
- [ ] User goals align with wireframe functionality
- [ ] Information architecture supports task completion
- [ ] Error states and recovery paths defined
- [ ] Mobile experience prioritized appropriately
- [ ] Accessibility considerations integrated

### Developer Handoff Ready
- [ ] User stories extractable from wireframes
- [ ] Component requirements clearly specified  
- [ ] Data flow and API needs documented
- [ ] Responsive behavior patterns defined
- [ ] Implementation priority established

## 📝 Implementation Notes
**Next Steps:** [What needs to happen before development]  
**Assumptions:** [Key assumptions that need validation]  
**Constraints:** [Technical/business limitations to consider]  
**Risks:** [Potential issues and mitigation strategies]
