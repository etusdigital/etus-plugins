---
doc_meta:
  id: sp
  display_name: Spike / Research
  pillar: Discovery
  owner_role: Tech Lead / Product Lead
  summary: Research investigation, feasibility study, or brainstorm documentation.
  order: 0
  requires: []
  feeds: [feature-brief, product-vision]
---

# Template: Spike / Research

**File:** `docs/ets/projects/{project-slug}/spikes/spike-{slug}.md`

**Purpose:** Document a research investigation, feasibility study, brainstorm, or proof of concept. Captures the question, methodology, findings, options, and decision.

## Responsaveis

- **Owner:** Tech Lead ou PM (dependendo do tipo de spike)
- **Contribuem:** Dev team, Design, Data
- **Aprovacao:** PM + Tech Lead

## Table of Contents
1. [Complete Structure](#complete-structure)
2. [Filling Notes](#filling-notes)
3. [Concrete Example](#concrete-example-minimal)
4. [Validation](#validation)

---

## Complete Structure

```markdown
# Spike: [Research Question]

**Date:** [DATE]
**Author:** [NAME]
**Time-box:** [hours/days allocated]
**Status:** [IN PROGRESS | COMPLETE | INCONCLUSIVE]
**Mode:** Spike/Research

---

## Research Question

[What are we trying to find out? Be specific.]

## Context

[Why does this matter now? What triggered this investigation?]

## Constraints

[Budget, timeline, technology, team skills, or other constraints that limit options.]

## Methodology

[How did we investigate? Tools used, sources consulted, experiments run.]

## Findings

### Key Finding 1: [Title]
[Details, evidence, data]

### Key Finding 2: [Title]
[Details, evidence, data]

### Key Finding 3: [Title]
[Details, evidence, data]

## Options Evaluated

### Option A: [Name]
- **Description:** [what it is]
- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **Effort:** [XS/S/M/L/XL]
- **Risk:** [Low/Medium/High]
- **Fit:** [How well does it meet our constraints?]

### Option B: [Name]
- **Description:** [what it is]
- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **Effort:** [XS/S/M/L/XL]
- **Risk:** [Low/Medium/High]
- **Fit:** [How well does it meet our constraints?]

### Option C: [Name]
- **Description:** [what it is]
- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **Effort:** [XS/S/M/L/XL]
- **Risk:** [Low/Medium/High]
- **Fit:** [How well does it meet our constraints?]

## Comparison Matrix

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| [Criterion 1] | [rating] | [rating] | [rating] |
| [Criterion 2] | [rating] | [rating] | [rating] |
| [Criterion 3] | [rating] | [rating] | [rating] |
| **Overall** | [score] | [score] | [score] |

## Recommendation

[Which option and why. If no recommendation yet, explain what's needed to decide.]

## Decision

- **Decision made:** [Yes/No]
- **Chosen option:** [A/B/C/None yet]
- **Rationale:** [Why this choice]
- **Next action:** [What happens next]

## Brainstorm Insights

[If BMAD CIS techniques were used, capture key insights here]

### Technique: [Name]
- [Insight 1]
- [Insight 2]

## Open Questions

### For Follow-up
- [Question that emerged during research]
- [Area that needs deeper investigation]


## O que fazer / O que nao fazer

**O que fazer:**
- Definir pergunta de pesquisa clara e time-boxed
- Documentar todas as opcoes avaliadas com evidencia
- Incluir recomendacao com justificativa
- Registrar o que foi descartado e por que

**O que nao fazer:**
- Nao pesquisar sem definir criterios de avaliacao antes
- Nao recomendar sem testar (PoC > opiniao)
- Nao extrapolar o time-box — spike com scope creep vira projeto
- Nao deixar spike sem conclusao (mesmo que seja "inconclusivo")

## Related Documents

- [Project Context if exists]
- [Product Vision if exists]
- [Linear issue if exists]
```

---

## Filling Notes

### Section: Research Question

- Be specific and answerable — not "should we use X?" but "Is X viable for our use case given constraints Y and Z?"
- A good research question can be answered with "Yes, because..." or "No, because..." or "It depends on..."
- If the question is too broad, split into multiple focused questions

### Section: Context

- Explain the trigger: what decision is blocked waiting for this answer?
- Include any prior knowledge or assumptions
- Mention who cares about the answer (stakeholders, teams)

### Section: Methodology

- Be explicit about how you investigated — future readers should be able to evaluate the rigor
- Include: sources consulted, tools used, experiments run, people consulted
- Note any limitations of the methodology ("We evaluated library X's documentation but did not build a prototype")

### Section: Findings

- Each finding should be a discrete, factual observation
- Support with evidence: data, benchmarks, documentation references, expert opinions
- Separate facts from interpretations — findings are what you observed, recommendations are what you think they mean
- Typically 3-5 key findings

### Section: Options Evaluated

- Present at least 2 options (even if one is "do nothing")
- Effort should be T-shirt sized: XS (<1 day), S (1-3 days), M (1-2 weeks), L (2-4 weeks), XL (>1 month)
- Risk considers: technical uncertainty, team familiarity, vendor dependency, reversibility
- Fit considers: alignment with constraints, existing tech stack, team skills

### Section: Comparison Matrix

- Pick 3-5 criteria most important for the decision
- Use consistent rating (numbers 1-5, or Good/Fair/Poor)
- Weight criteria if some are more important than others

### Section: Recommendation

- State your recommendation clearly and first — don't bury it
- Explain the WHY — what makes this option better than the alternatives
- If you can't recommend yet, explain exactly what's missing
- "No recommendation" is a valid outcome — document what's needed to decide

### Section: Decision

- Explicitly state whether a decision was made
- If decision is pending, state what needs to happen for a decision
- "Next action" should be concrete: "Create feature brief for Option A" or "Schedule meeting with team to discuss findings"

### Section: Brainstorm Insights

- Only include if BMAD CIS techniques were actually used
- Capture the insights that influenced the research direction or option evaluation
- Reference which technique produced which insight

---

## Concrete Example (Minimal)

```markdown
# Spike: Redis vs Memcached for Session Storage

**Date:** 2026-03-17
**Author:** Engineering Team
**Time-box:** 4 hours
**Status:** COMPLETE
**Mode:** Spike/Research

---

## Research Question

Should we use Redis or Memcached for user session storage, given our need to support 50K concurrent sessions with <10ms latency and our existing AWS infrastructure?

## Context

The current session storage (PostgreSQL with row-level locking) is a performance bottleneck. Response times spike during peak hours (5-7 PM) when concurrent sessions exceed 30K. The team agreed to move sessions to an in-memory store but hasn't decided which one.

## Constraints

- Must run on AWS (team already uses AWS managed services)
- Budget: <$500/month for session storage
- Team has no Redis or Memcached production experience
- Must support session expiration (TTL)
- Must handle 50K concurrent sessions at launch, 200K within 6 months

## Methodology

- Reviewed AWS documentation for ElastiCache (Redis) and ElastiCache (Memcached)
- Compared pricing for t3.medium instances
- Reviewed benchmarks from AWS re:Invent 2025 session on caching strategies
- Tested connection from a staging Lambda function to both ElastiCache engines

## Findings

### Key Finding 1: Redis Supports Data Structures Beyond Key-Value
Redis supports lists, sets, sorted sets, and hashes natively. Memcached is pure key-value. For sessions, both work, but Redis enables future use cases (rate limiting, feature flags) without adding another service.

### Key Finding 2: Memcached Has Slightly Lower Latency for Simple Gets
Memcached shows ~5-15% lower latency for simple GET operations in AWS benchmarks (0.3ms vs 0.35ms for Redis). Both are well under our 10ms requirement.

### Key Finding 3: Redis Has Built-in Persistence and Replication
Redis supports AOF/RDB persistence and automatic failover. Memcached loses all data on restart. For sessions, data loss means all users are logged out simultaneously — disruptive but not catastrophic.

## Options Evaluated

### Option A: AWS ElastiCache (Redis)
- **Description:** Managed Redis cluster with automatic failover
- **Pros:** Data persistence, replication, versatile data structures, large community
- **Cons:** Slightly higher latency for simple ops, more complex configuration
- **Effort:** S (2-3 days to implement)
- **Risk:** Low (well-documented, managed service)
- **Fit:** Strong — meets all constraints, provides growth path

### Option B: AWS ElastiCache (Memcached)
- **Description:** Managed Memcached cluster
- **Pros:** Simplest possible implementation, marginally faster for basic ops
- **Cons:** No persistence (mass logout on restart), no replication, limited to key-value
- **Effort:** XS (<1 day to implement)
- **Risk:** Medium (data loss on restart, no failover)
- **Fit:** Adequate for sessions only — no growth path

### Option C: Keep PostgreSQL + Add Connection Pooling
- **Description:** Optimize current approach with PgBouncer and session table partitioning
- **Pros:** No new technology to learn, no new service to manage
- **Cons:** Doesn't solve the fundamental problem (row locking), diminishing returns
- **Effort:** M (1-2 weeks to tune properly)
- **Risk:** Medium (may not achieve target performance)
- **Fit:** Poor — band-aid, not a solution

## Comparison Matrix

| Criterion | Redis | Memcached | PostgreSQL |
|-----------|-------|-----------|------------|
| Latency (<10ms) | Good | Good | Fair |
| Persistence | Good | Poor | Good |
| Scalability to 200K | Good | Good | Poor |
| Team learning curve | Fair | Good | Good |
| Future flexibility | Good | Poor | Fair |
| **Overall** | 4.2/5 | 3.0/5 | 2.4/5 |

## Recommendation

Redis (Option A). The marginal latency difference vs. Memcached is irrelevant for our use case (both are sub-1ms, we need <10ms). Redis provides persistence (avoiding mass logouts), replication (high availability), and a growth path for rate limiting and feature flags that we'll need in the next 6 months. The 2-3 extra days of implementation effort is worth the long-term flexibility.

## Decision

- **Decision made:** Yes
- **Chosen option:** A (Redis)
- **Rationale:** Best balance of performance, reliability, and future flexibility
- **Next action:** Create feature brief for "Migrate Session Storage to Redis"
```

---

## Validation

**Before finalizing Spike:**

- [ ] Research question is specific and answerable
- [ ] Context explains why this matters now
- [ ] At least 2 options evaluated with pros/cons/effort/risk
- [ ] Comparison is structured (matrix or equivalent)
- [ ] Recommendation is present with clear rationale (or "needs more research" with specifics)
- [ ] Decision section explicitly states whether a decision was made
- [ ] Next action is concrete
