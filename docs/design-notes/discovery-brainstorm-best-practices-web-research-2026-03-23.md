# Discovery + Brainstorm Best Practices Research

**Date:** 2026-03-23  
**Scope:** Best practices and facilitation dynamics for discovery interviews and brainstorming, translated into ETUS PMDocs implications  
**Goal:** Identify what excellent teams do in discovery and ideation so ETUS can become significantly better at extracting product intent before specification.

---

## Why This Research Matters

If ETUS wants to become exceptionally good at interviewing, the most important place to improve is not every phase equally.

The highest-leverage phases are:

1. **Discovery / ideation intake** — where we extract the real problem, context, actors, behavior, and unmet needs
2. **Brainstorm / solution exploration** — where we convert evidence into candidate directions without prematurely locking into a solution

These phases have very different jobs:

- Discovery should reduce **misunderstanding**
- Brainstorm should reduce **premature certainty**

ETUS already contains pieces of both, but the web research reinforces that mature teams treat them as distinct modes with different dynamics, artifacts, and facilitation rules.

---

## Research Base

This synthesis draws primarily from:

- GOV.UK Service Manual — user research and service standard
- Nielsen Norman Group — semistructured interview guidance
- Design Council — Double Diamond
- IDEO Design Kit — HCD methods for synthesis and brainstorming
- Product Talk / Teresa Torres — story-based interviews and opportunity solution trees
- Google Design Sprint Kit / Relay — ideation, HMW, assumptions, critique, error recovery, remote facilitation

---

## Part 1 — What Great Discovery Looks Like

## 1. Discovery starts from user behavior, not requested features

The strongest cross-source pattern is that discovery should focus on:

- what users are trying to do
- how they do it today
- what context shapes their behavior
- what breaks
- what matters in their own words

This appears clearly in GOV.UK guidance on understanding users and in Product Talk's story-based interviewing approach.

**Implication for ETUS**

ETUS should not let discovery begin with "What feature do you want?" as the dominant frame.

It should begin with:

- what happened
- when it happened
- who was involved
- what they did
- what went wrong
- what they did next

That means the discovery core should use **story extraction**, not just requirements elicitation.

---

## 2. The best discovery interviews are story-based and past-focused

Product Talk strongly emphasizes asking for **specific past experiences** instead of hypothetical or generic answers.

Nielsen Norman Group's semistructured interview example reinforces the same pattern with prompts like:

- walk me through
- can you give me an example
- what happened
- why is that important to you

This is a much better pattern than:

- what do you usually do
- what features do you want
- would you use X

Because those questions invite:

- aspiration
- rationalization
- abstraction
- weak memory summaries

**Implication for ETUS**

Discovery prompts should prefer:

- "Me conta da última vez que isso aconteceu"
- "Me conduz passo a passo pelo que você fez"
- "O que aconteceu depois?"
- "Pode me dar um exemplo concreto?"
- "Por que isso foi importante para você?"

And ETUS should explicitly avoid over-reliance on:

- hypotheticals
- generalized summaries
- direct feature-request harvesting

---

## 3. Discovery should be semistructured, not scripted and not free-form

NNGroup's semistructured interview guidance implies a balanced pattern:

- a stable guide for consistency
- flexible follow-up probes
- active listening
- structured depth

This is important for ETUS because it means:

- a rigid checklist is too brittle
- a fully improvisational interview is too inconsistent

**Implication for ETUS**

ETUS needs a real semistructured interview model:

- core questions per module
- follow-up probes when answers are vague
- checkpoints for reflection and summary
- rules for when to go deeper
- rules for when to move on

This supports the case for an **elicitation engine** or interview state machine.

---

## 4. Discovery should be inclusive and end-to-end

GOV.UK repeatedly emphasizes:

- include users with different access needs
- research the whole journey, not just the screen
- understand support channels and assisted flows
- include all ways people interact with the service

This is especially important because many products fail when discovery is too digital-only or user-only.

**Implication for ETUS**

Discovery should explicitly surface:

- non-digital or offline steps
- support and operations interactions
- internal stakeholders and approvers
- accessibility and assisted-use scenarios
- cross-channel behavior

This strengthens the case for asking not just about the "primary user," but also:

- operator
- approver
- support team
- admin
- anti-user / misuse actor

---

## 5. Discovery should be continuous, not front-loaded

GOV.UK recommends researching in small batches throughout development, and Product Talk emphasizes a regular cadence of interviews.

This does not mean ETUS must force weekly interviews in all contexts, but it does mean the framework should treat discovery as a continuing capability, not a one-off phase that is "done forever."

**Implication for ETUS**

ETUS should support:

- initial discovery
- follow-up elicitation
- periodic interview refresh
- change-triggered rediscovery

In practice, this supports a stronger `/elicit` or rediscovery step when:

- assumptions remain high-risk
- priorities change
- a solution is failing
- stakeholders disagree

---

## 6. Discovery synthesis should happen immediately and collaboratively

IDEO recommends "download your learnings" right after interviews while details are still fresh.

Product Talk recommends interview snapshots that capture the key context, memorable quote, experience map, opportunities, and insights quickly after each interview.

This is a major finding for ETUS.

**Implication for ETUS**

The framework should not wait until a big summary document to synthesize.

It should create small, per-interview synthesis objects, for example:

- interview snapshot
- story snapshot
- opportunity note
- contradiction note

These should then feed:

- opportunity-pack
- coverage-matrix
- OST / prioritization

This would reduce loss of detail between raw conversation and later documents.

---

## Part 2 — What Great Brainstorm Looks Like

## 7. Brainstorm should only begin after the problem is framed well enough

The Double Diamond and Product Talk align strongly here:

- first understand and frame the problem
- then generate solutions

Teresa Torres's OST guidance is especially important: brainstorm should happen for a **chosen target opportunity**, not across the whole mess of the problem space.

**Implication for ETUS**

The current ETUS rule that brainstorm is blocked until minimum coverage exists is directionally correct.

But the unlock condition should become stronger:

- not just "some actors and a journey exist"
- but "we have enough evidence to define a specific opportunity"

Brainstorm should start only when ETUS can answer:

- what opportunity are we targeting?
- for whom?
- in what context?
- with what evidence?

---

## 8. "How Might We" is the strongest bridge between discovery and brainstorm

IDEO's `How Might We` method is one of the clearest bridges between insights and ideation:

- it reframes insights as possibility spaces
- it should not imply a solution
- it should be broad enough to allow options
- but narrow enough to stay actionable

**Implication for ETUS**

Discovery synthesis should end with 3-5 strong HMW prompts per target opportunity.

That means ETUS should not jump directly from:

- interview notes

to:

- candidate solutions

It should go through:

- themes
- insights
- HMWs
- then brainstorm

This would make brainstorm much more disciplined.

---

## 9. Good brainstorming separates divergence and convergence very clearly

IDEO's brainstorming rules and Design Sprint practice reinforce a clean separation:

- first diverge: quantity, build on ideas, defer judgment
- then converge: cluster, evaluate, gut check, vote, critique

Blending these modes too early kills idea generation.

**Implication for ETUS**

Brainstorm in ETUS should run in explicit stages:

1. Diverge
2. Cluster
3. Select
4. Stress test
5. Assumption test planning

The framework should avoid turning brainstorm into instant critique.

---

## 10. Strong brainstorming is facilitated by simple but strict rules

IDEO's seven brainstorm rules include principles such as:

- defer judgment
- encourage wild ideas
- build on others' ideas
- stay focused
- one conversation at a time
- be visual
- go for quantity

These are simple, but they matter because they shape the energy of the session.

**Implication for ETUS**

If ETUS offers brainstorm modes, it should explicitly switch the facilitation stance:

- during divergence, do not critique yet
- use "and" language instead of "but"
- keep the prompt visible
- push quantity first

This is especially important if ETUS ever uses parallel sub-agents or multiple brainstorm techniques.

---

## 11. The best brainstorms use concrete dynamics, not just "let's ideate"

The research points to several practical dynamics that work well:

### A. HMW + affinity mapping

From Google Design Sprint and IDEO:

- create HMW prompts
- collect notes
- cluster by theme
- vote/select target

### B. Crazy 8s

From the Google Sprint agenda:

- rapid sketching
- many options in very little time
- good for breaking solution fixation

### C. Gut Check

From IDEO:

- distill the core of an idea
- list constraints and barriers
- adapt ideas within real constraints
- discard weak ideas

### D. Five Whys

From IDEO:

- useful not as a brainstorm tool first, but as a pre-brainstorm deepening tool
- helps avoid solving the symptom instead of the cause

### E. Mash-Ups / analogies

From IDEO:

- useful when teams need novel directions
- combine desired qualities from other systems or brands

### F. Role play and error recovery

From Google voice sprint agendas:

- role-play candidate interactions
- explicitly discuss error recovery flows

This is a powerful finding for ETUS because it connects ideation to implementation realism much earlier.

---

## 12. Good brainstorms keep assumptions visible

Product Talk's OST flow is especially useful here:

- brainstorm several solutions
- choose around three to explore further
- break them into assumptions
- test the riskiest assumptions

This means brainstorm is not the end of discovery. It is the start of **assumption-based decision making**.

**Implication for ETUS**

Brainstorm output should never just be:

- "Direction A / B / C"

It should also include:

- why it might work
- what must be true for it to work
- what could make it fail
- what to test first

That suggests ETUS should connect brainstorm directly to:

- assumptions
- experiments
- solution-discovery

---

## 13. Psychological safety and inclusion materially affect brainstorm quality

Google Relay materials emphasize psychological safety and inclusion as facilitation concerns, especially for distributed collaboration.

This matters because brainstorm quality drops when:

- dominant voices take over
- critique starts too early
- quieter participants do not contribute
- remote participants lag behind

**Implication for ETUS**

If ETUS supports async or hybrid collaboration in the future, it should:

- separate solo ideation from group convergence
- preserve equal contribution time
- make critique happen after idea generation
- support async contribution windows

This is especially relevant if ETUS later grows a richer console or collaborative UI.

---

## Part 3 — What This Means For ETUS Specifically

## A. Discovery should become the true Core Interview Layer

ETUS should explicitly treat `ideate` + discovery as the main idea-extraction engine.

That means this layer should own:

- story-based interviews
- follow-up probes for vague answers
- reflection checkpoints
- stakeholder conflict detection
- anti-requirements
- evidence capture
- immediate synthesis

This is where the quality bar needs to be highest.

---

## B. Brainstorm should become a gated translation layer, not a generic creativity block

ETUS should treat brainstorm as:

- evidence-informed
- opportunity-scoped
- divergence first
- convergence second
- linked to assumptions and experiments

This is different from a general "let's brainstorm" mode.

The ideal ETUS brainstorm flow is:

1. Discovery stories
2. Themes
3. Insight statements
4. HMW prompts
5. Divergent generation
6. Clustering / bundling
7. Gut check
8. Select 3 directions
9. Surface assumptions
10. Recommend tests

---

## C. ETUS should add two missing micro-artifacts

### 1. Interview Snapshot

Per interview:

- who was interviewed
- context
- memorable quote
- story / experience map
- opportunities
- open questions
- contradictions

### 2. Brainstorm Packet

Per brainstorm session:

- target opportunity
- HMW prompts
- generated ideas
- clustered themes
- shortlisted ideas
- assumptions
- recommended next tests

These artifacts would reduce context loss between phases.

---

## D. ETUS should use different facilitation stances in discovery vs brainstorm

### Discovery stance

- curious
- specific
- evidence-seeking
- context-seeking
- patient
- grounded in past behavior

### Brainstorm stance

- expansive
- defer judgment first
- generative
- visual
- option-rich
- then analytical in convergence

Today these modes are conceptually present, but they are not yet sharply differentiated enough in workflow behavior.

---

## Recommended ETUS Changes Based On Web Research

## Priority 1 — Discovery mechanics

1. Add story-based interviewing as the default discovery method
2. Add probe templates:
   - "Walk me through the last time..."
   - "Can you give me a specific example?"
   - "What happened next?"
   - "Why was that important?"
3. Add reflection checkpoints every few substantive answers
4. Add an interview snapshot artifact
5. Add stronger synthesis cadence after each interview

## Priority 2 — Bridge to brainstorm

1. Add explicit theme clustering
2. Add insight statement generation
3. Add HMW generation before brainstorm
4. Only unlock brainstorm for a selected target opportunity

## Priority 3 — Brainstorm mechanics

1. Split brainstorm into divergence and convergence
2. Add support for:
   - HMW affinity mapping
   - Crazy 8s
   - Gut Check
   - Five Whys
   - Mash-Ups
   - role play + error recovery
3. Shortlist 3 directions
4. Attach assumptions to each direction

## Priority 4 — Continuity into decision making

1. Turn brainstorm output into solution-discovery input
2. Require assumption tests for higher-risk directions
3. Preserve rejected directions and why they were rejected

---

## Best-Practice Operating Model For ETUS

If ETUS wants to become excellent specifically at discovery and brainstorm, the operating model should look like this:

### Discovery

- Start from story-based interviewing
- Keep the user in real past behavior
- Probe for context, not opinions
- Include operators, support, approvals, edge actors
- Synthesize immediately after each interview
- Update opportunity space every few interviews

### Brainstorm

- Do not brainstorm from raw notes
- Convert insights into HMW prompts first
- Diverge widely, then converge deliberately
- Focus on one target opportunity at a time
- Use structured dynamics, not vague "ideation"
- End with assumptions and next tests, not just favorite ideas

---

## Final Conclusion

The web research strongly reinforces the following conclusion:

**Yes — discovery and brainstorm are the most important interview-heavy phases. But they are important for different reasons, and ETUS should optimize them differently.**

- Discovery should optimize for **truth and context**
- Brainstorm should optimize for **range, structure, and disciplined translation into testable directions**

If ETUS gets those two phases right, every downstream document becomes easier, more accurate, and more implementable.

If ETUS gets them wrong, no amount of later documentation rigor fully repairs the loss.

---

## Sources

- GOV.UK Service Manual — User research for government services: an introduction: https://www.gov.uk/service-manual/user-research/how-user-research-improves-service-design
- GOV.UK Service Standard — Understand users and their needs: https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs
- Nielsen Norman Group — Example Guide for a Semistructured Interview: https://media.nngroup.com/media/editor/2021/02/05/example_interview_guide.pdf
- Design Council — The Double Diamond: https://www.designcouncil.org.uk/our-resources/the-double-diamond/
- IDEO Design Kit — Brainstorm Rules: https://www.designkit.org/methods/brainstorm-rules.html
- IDEO Design Kit — How Might We: https://www.designkit.org/methods/how-might-we.html
- IDEO Design Kit — Download Your Learnings: https://www.designkit.org/methods/download-your-learnings.html
- IDEO Design Kit — Find Themes: https://www.designkit.org/methods/find-themes.html
- IDEO Design Kit — Five Whys: https://www.designkit.org/methods/the-five-whys.html
- IDEO Design Kit — Gut Check: https://www.designkit.org/methods/gut-check.html
- Product Talk — Opportunity Solution Trees: https://www.producttalk.org/opportunity-solution-trees/
- Product Talk — Story-Based Customer Interviews Uncover Much-Needed Context: https://www.producttalk.org/story-based-customer-interviews/
- Product Talk — User Interviews: https://www.producttalk.org/glossary-discovery-user-interviews/
- Product Talk — Interview Snapshot: https://www.producttalk.org/glossary-discovery-interview-snapshot/
- Google Design Sprint Kit — Product Sprint Deck / 3-Day Template: https://designsprintkit.withgoogle.com/assets/tools/Product%20Sprint%20Deck%20-%203-Day%20Template.pdf
- Google Design Sprint Kit — Voice Action Design Sprint Agenda: https://designsprintkit.withgoogle.com/assets/tools/Voice%20Action%20Design%20Sprint%20Agenda.pdf
- Google Relay — Facilitating Asynchronously: https://designsprintkit.withgoogle.com/relay2021/facilitating-asynchronously.html
- Google Relay — Safety for Authenticity: https://designsprintkit.withgoogle.com/relay2021/safety-for-authenticity.html
