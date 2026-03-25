---
name: impl-packet
description: >
  Use when generating a consolidated developer handoff document. Triggers on
  'handoff', 'dev packet', 'implementation packet', 'what does the dev need',
  'developer handoff', 'consolidate for dev', or 'engineering brief'.
model: sonnet
version: 1.0.0
argument-hint: "[feature-slug] [--scope=feature|sprint]"
---

# Implementation Packet — Developer Handoff Skill

## Purpose

Generate a single consolidated document per feature (or per sprint) that contains everything engineering needs to implement. This document is NON-AUTHORITATIVE — it summarizes and consolidates content from authoritative source documents but does NOT redefine any content. If the source document changes, the packet should be regenerated.

## When to Use

- After Implementation Readiness Gate passes (Gate 3)
- When a developer asks "what do I need to build this feature?"
- Before sprint planning to consolidate scope for engineering
- After `/correct-course` to regenerate with updated scope

## SST Derivation Table

The packet pulls from authoritative sources. Each section cites its authority.

| Section | Authority Document |
|---------|-------------------|
| Context & Non-Goals | feature-brief.md + NG-# registry (product-vision or PRD) |
| Actors & Permissions | opportunity-pack.md + feature-spec permission matrix |
| Business Rules | feature-brief FB-# + feature-spec business rules |
| Acceptance Criteria | user-stories.md (filtered by feature US-#) |
| Error Handling | feature-spec error handling matrix (EDGE-#) |
| State Machine | feature-spec state machine section |
| API Contracts | api-spec.md (filtered by feature endpoints) |
| Data Mutations & Validation | database-spec.md + data-dictionary.md |
| Performance NFR-# | tech-spec.md (filtered by relevant NFR-#) |
| Observability | tech-spec.md observability section |
| Tasks impl-# | implementation-plan.md (filtered by feature) |
| Open Questions | ASM-# open + outstanding questions from all sources |

## Critical Rule: NON-AUTHORITATIVE

This packet is a **read-only consolidation**. It MUST NOT:
- Redefine acceptance criteria (authority: user-stories.md)
- Change NFR targets (authority: tech-spec.md)
- Modify API schemas (authority: api-spec.md)
- Add new business rules (authority: feature-spec)
- Create new error scenarios (authority: feature-spec)

If the packet reveals a gap (missing section in source doc), it flags the gap but does NOT fill it.

## Scope Resolution

1. If `--scope=feature` + `[feature-slug]` → generate packet for one feature
2. If `--scope=sprint` → generate packet per feature in the current sprint (read from implementation-plan.md sprint assignments)
3. Default: `--scope=feature` if feature-slug provided, ask user otherwise

## Generation Logic

For each section in the SST Derivation Table:

1. **Read** the authority document
2. **Filter** to content relevant to the target feature (by feature-slug, FS-#, US-# references)
3. **Extract** the relevant section content
4. **Format** into the packet template (see knowledge/template.md)
5. **Validate** that the section is non-empty

### Missing-Section Detection

If the authority document does not contain the expected section:

```
## {Section Name} [Authority: {doc}]

> MISSING — {authority-doc} does not contain this section.
> Run `/elicit` to identify the gap, or update the source document directly.
```

This flag is a signal to the team, not a blocker. The packet can be generated with missing sections.

## Regeneration

The packet can be regenerated at any time. It is always derived, never manually edited. If a developer finds an issue in the packet, the fix goes into the authority document, not the packet.

## Output Path

```
docs/ets/projects/{project-slug}/implementation/packets/
  implementation-packet-{feature-slug}.md
```

Or for sprint scope:
```
docs/ets/projects/{project-slug}/implementation/packets/
  sprint-{N}-{feature-slug}.md
```

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard.

1. **Scope confirmation** — Before generating, confirm the feature scope with the user: "I'll generate a packet for feature `{feature-slug}`. This will pull from: {list of authority docs found}. Any docs missing? Proceed?"
2. **Missing section review** — After generation, present all missing sections and ask: "These sections are flagged as missing from source docs. Want to run `/elicit` to investigate, or proceed as-is?"
3. **Handoff options:**
   1. Packet complete — share with engineering (Recommended)
   2. Run `/elicit` — investigate missing sections
   3. Regenerate — after fixing source documents
   4. Generate for another feature

## WORKFLOW

### Step 1: Scope Resolution
- **Input:** `$ARGUMENTS` (feature-slug, --scope)
- **Action:** Determine target feature(s) and locate all authority documents
- **Output:** Feature scope + document inventory

### Step 2: Authority Document Loading
- **Input:** Document inventory
- **Action:** Read each authority document, extract sections relevant to the feature
- **Output:** Content bundle per section

### Step 3: Packet Assembly
- **Input:** Content bundle
- **Action:** Assemble content into the packet template (knowledge/template.md)
- **Output:** Draft packet

### Step 4: Missing-Section Detection
- **Input:** Draft packet
- **Action:** Scan for empty or missing sections, flag with MISSING marker
- **Output:** Annotated packet with gap flags

### Step 5: Scope Confirmation
- **Action:** Present the packet summary to the user:
  - Sections populated: N/12
  - Sections missing: N/12 (list)
  - Authority docs found: N (list)
  - Authority docs missing: N (list)
- **Approval:** Ask user to confirm or adjust before saving

### Step 6: Save Artifact
- **Action:**
  1. Verify directory exists → create with `mkdir -p`
  2. Write packet to `docs/ets/projects/{project-slug}/implementation/packets/implementation-packet-{feature-slug}.md`
- **Output:** File written to disk

### Step 7: Handoff
- **Action:** Display CLOSING SUMMARY and present handoff options

## CLOSING SUMMARY

After saving, display:

```text
implementation-packet-{feature-slug}.md saved to
  docs/ets/projects/{project-slug}/implementation/packets/

Sections: {N}/12 populated, {N}/12 missing
Authority docs: {N} found, {N} missing
Missing sections: {list if any}

Next steps:
  1. Share with engineering
  2. Run /elicit to investigate gaps
  3. Regenerate after fixing source docs
```

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| Feature-slug not found in any doc | High | Ask user to confirm slug | List available features |
| Authority doc missing entirely | Medium | Flag in packet as MISSING | Generate partial packet |
| Authority doc is DRAFT status | Low | Include content with DRAFT warning | Proceed with warning |
| No implementation-plan.md | Medium | Skip tasks section | Flag in packet |
| No api-spec.md | Medium | Skip API section | Flag in packet |
