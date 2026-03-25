# Archetype: Workflow / Approval

## Description

Use when the feature involves approvals, state transitions, multi-step processes, or sequential authorization. This archetype surfaces hidden states, missing rejection flows, delegation gaps, and SLA blind spots that commonly cause rework during implementation.

## When to Activate

Activate this archetype when stories or problem framing mention:
- Approvals, reviews, sign-offs
- Status changes, state machines, workflows
- Multi-step processes with handoffs
- Sequential or parallel authorization
- Escalation or delegation

## Mandatory Probes

### Probe 1: State Enumeration
**Question:** "What are all the possible states this item can be in? List every one, including intermediate and error states."
- **Sufficient when:** 3+ named states with clear transitions between them
- **Insufficient when:** Only "pending and approved" mentioned, or states are vague ("in progress")

### Probe 2: Rejection Flow
**Question:** "When someone rejects, what happens? Does it go back to the requester? Is the requester notified? Can the rejector add a reason?"
- **Sufficient when:** Clear rejection path including notification, reason capture, and next action for the requester
- **Insufficient when:** "The person corrects and resends" with no detail on notification or state change

### Probe 3: Timeout / SLA
**Question:** "If nobody approves within X days, what should happen? Is there an escalation path or auto-action?"
- **Sufficient when:** Specific timeout duration + concrete action (escalate to manager, auto-approve, auto-reject, notify)
- **Insufficient when:** "I don't know" or "we'll figure it out later" → register as ASM-# with validation_required

### Probe 4: Delegation
**Question:** "Can someone delegate the approval to another person? Does the delegate have the same powers, or are there restrictions?"
- **Sufficient when:** Delegation rules defined (who can delegate, to whom, scope of delegated authority, audit trail)
- **Insufficient when:** "Yes, they can delegate" with no rules about scope or restrictions

### Probe 5: Audit Trail
**Question:** "Is there an audit trail? Who needs to see the approval history? Is it immutable or can entries be edited?"
- **Sufficient when:** Audit requirements specified (what is logged, who can view, retention period, immutability)
- **Insufficient when:** "Yes, we need an audit trail" with no specifics on content or access

### Probe 6: Reopen Conditions
**Question:** "Can something already approved be reopened or revoked? Under what conditions? Who has that power?"
- **Sufficient when:** Reopen/revoke rules specified (conditions, authorized roles, effect on downstream actions)
- **Insufficient when:** "Maybe, if something changes" with no defined conditions

### Probe 7: Parallel vs Sequential
**Question:** "Are there parallel approvals (multiple people must approve independently) or sequential (one after another)? Can the order change?"
- **Sufficient when:** Approval topology defined (parallel/sequential/hybrid), quorum rules if parallel, order rules if sequential
- **Insufficient when:** "Multiple people approve" with no topology specified

### Probe 8: Notifications
**Question:** "What notifications fire at each state transition? Who receives them? Through which channels (email, in-app, push)?"
- **Sufficient when:** Notification matrix covering each transition, recipients, channels, and content summary
- **Insufficient when:** "We send emails" with no mapping to specific transitions

## Anti-Patterns

1. **Implicit states** — The workflow has states that exist in practice but are never named or documented (e.g., "waiting for info" is a real state but not tracked)
2. **Impossible transitions not documented** — No explicit list of which state transitions are forbidden (e.g., "approved" cannot go back to "draft" without going through "reopened")
3. **SLA without consequence** — A timeout is defined but nothing happens when it triggers
4. **Happy-path-only design** — Only the approval path is designed; rejection, timeout, delegation, and revocation are afterthoughts

## Archetype Dimensions

These dimensions are added to `coverage-matrix.yaml` under `semantic_dimensions.archetype_dimensions`:

| Dimension | Covered when |
|-----------|-------------|
| `state_machine_defined` | All states enumerated with valid transitions and at least one invalid transition documented |
| `invalid_transitions_documented` | Explicit list of forbidden state changes exists |
| `sla_timeout_defined` | Timeout duration + triggered action specified for every approval step |
