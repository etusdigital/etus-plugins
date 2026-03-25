---
name: prioritization
description: >
  Use when prioritizing opportunities or features using ICE or RICE scoring with
  documented rationale and trade-offs. Also triggers on 'prioritize', 'ICE score',
  'RICE score', 'what comes first', 'priorização', 'ranking', or 'P0/P1/P2'.
model: opus
version: 1.0.0
argument-hint: "[context-path]"
compatibility: "Optional: external issue tracker adapter (for example, Linear) for backlog projection, Slack MCP (share ranking with stakeholders)"
---

## PURPOSE

Transform the OST into a decision: what enters now, what waits, and why. This document makes trade-offs explicit (impact vs effort vs confidence) and prevents "everything is a priority." It converts opportunities into P0/P1/P2 classification with documented rationale, enabling the team to open PRDs for the right items.

**Principle:** Sequencing is choosing.

## DEPENDENCY RESOLUTION

**Reference:** `.claude/skills/orchestrator/dependency-graph.yaml`

**BLOCKS** (must exist — auto-invoke if missing):
- `docs/ets/projects/{project-slug}/planning/ost.md` — Opportunities to prioritize come from the OST (O-# references).

**ENRICHES** (improves output — warn if missing):
- `docs/ets/projects/{project-slug}/discovery/baseline.md` — Baseline metrics inform impact assessment (baseline → target).
- `docs/ets/projects/{project-slug}/discovery/product-vision.md` — BO-# objectives inform priority alignment with strategic direction.

**Resolution protocol:**
1. Read `dependency-graph.yaml` → `prioritization.requires: [ost]`
2. Check: does `docs/ets/projects/{project-slug}/planning/ost.md` exist, is non-empty, and is not `<!-- STATUS: DRAFT -->`?
3. If ost missing → INFORM user → auto-invoke `ost` skill → wait → continue
4. If ost is DRAFT → WARN: "ost.md is DRAFT — prioritization may have weaker opportunity foundation" → proceed
5. Check if baseline.md exists → if yes, load baseline metrics to inform impact assessment → if no, WARN and proceed
6. Check if product-vision.md exists → if yes, load BO-# objectives to align priorities → if no, WARN and proceed

**Position in workflow:** After OST, before PRD. P0 items from this document become features in the PRD.

## ARTIFACT SAVE RULE

**MANDATORY:** This skill MUST write its artifact to disk before declaring complete.

1. Verify target directory exists → create with `mkdir -p` if needed
2. Write the complete document using the Write tool to the exact path specified in OUTPUT FORMAT
3. Displaying content in chat is NOT saving — the file MUST exist on the filesystem
4. After writing, display the CLOSING SUMMARY with the saved path
5. Only THEN propose the next step

**If the Write fails:** Report the error to the user. Do NOT proceed to the next skill.

## INTERACTION PROTOCOL

This skill follows the ETUS interaction standard. Your role is a thinking partner, not an interviewer — challenge inflated impact scores, push for evidence behind confidence ratings, probe whether effort estimates have been validated with the Tech Lead, and flag when everything is being marked P0. Prioritization work is about honest trade-offs — these patterns ensure the user makes deliberate choices, not wishful rankings.

1. **One question per message** — Ask one question, wait for the answer, then ask the next. Prioritization questions require the user to make judgment calls, so give them space. Use the AskUserQuestion tool when available for structured choices.

2. **3-4 suggestions for choices** — When the user needs to choose a direction (e.g., ICE vs RICE, how to handle ties, whether to include dependencies as a factor), present 3-4 concrete options with a brief description of each. Highlight your recommendation. Let the user pick before proceeding.

3. **Propose approaches before generating** — Before generating any content section, propose 2-3 approaches with tradeoffs. Example: "I see two methods for this prioritization: (A) ICE — simpler, faster, works well when reach is roughly equal across items; (B) RICE — adds Reach dimension, better when items have very different audience sizes. I recommend A because the OST opportunities target the same user segment."

4. **Present output section-by-section** — Don't generate the full document at once. Present each major section (Method selection, then each item's scoring one at a time, then ranking, then trade-offs), ask "Does this capture it well? Anything to adjust?" and only proceed after approval.

5. **Track outstanding questions** — If something can't be answered now, classify it:
   - **Resolve before PRD** — This blocks the next phase. Keep asking until resolved.
   - **Deferred to implementation** — Noted and carried forward.
   - **Deferred to [phase name]** — Noted and carried forward.

6. **Multiple handoff options** — At completion, present 3-4 next steps as options instead of a single fixed path.

7. **Resume existing work** — Before starting, check if the target artifact already exists at the expected path. If it does, ask the user: "I found an existing prioritization.md at [path]. Should I continue from where it left off, or start fresh?" If resuming, read the document, summarize the current state, and continue from outstanding gaps.

8. **Assess if full process is needed (right-size check)** — If the user's input already has clear scores with rationale and a proposed ranking, don't force the full interview. Confirm understanding briefly and offer to skip directly to document generation. Only run the full interactive process when there's genuine ambiguity to resolve.

9. **Thinking partner behaviors:**
   - When impact is rated 5 without strong evidence: "Impact 5 means this is the highest-impact item. What baseline metric moves, and by how much?"
   - When confidence is rated 5 without data: "Confidence 5 means strong evidence supports this. What's the evidence — data, user research, or precedent?"
   - When effort is rated without Tech Lead input: "Has this effort estimate been validated with the Tech Lead? A PM estimate alone should cap confidence at 3."
   - When everything is P0: "If everything is P0, nothing is P0. If you could only do ONE of these this cycle, which would it be?"
   - When dependencies are ignored: "O-[X] depends on [Y]. Even if O-[X] scores higher, can it be done first?"

## MEMORY PROTOCOL

This skill reads and writes persistent memory to maintain context across sessions.

**On start (before any interaction):**
1. Read `docs/ets/.memory/project-state.md` — know where the project is
2. Read `docs/ets/.memory/decisions.md` — don't re-question closed decisions
3. Read `docs/ets/.memory/preferences.md` — apply user/team preferences silently
4. Read `docs/ets/.memory/patterns.md` — apply discovered patterns
5. If any memory file doesn't exist, create it with the default template

**On finish (after saving artifact, before CLOSING SUMMARY):**
1. `project-state.md` is updated **automatically** by the PostToolUse hook — do NOT edit it manually.
2. If the user chose between approaches during this skill → run via Bash:
   `python3 .claude/hooks/memory-write.py decision "<decision>" "<rationale>" "<this-skill-name>" "<phase>" "<tag1,tag2>"`
3. If the user expressed a preference → run via Bash:
   `python3 .claude/hooks/memory-write.py preference "<preference>" "<this-skill-name>" "<category>"`
4. If a recurring pattern was identified → run via Bash:
   `python3 .claude/hooks/memory-write.py pattern "<pattern>" "<this-skill-name>" "<applies_to>"`

**The `.memory/*.md` files are read-only views** generated automatically from `memory.db`. Never edit them directly.

## PRESSURE TEST

Before generating content, challenge the prioritization quality with these questions (ask the most relevant 1-2, not all):

- **"If everything is P0, nothing is P0. What is THE MOST important?"** — Force a single top priority. If the user cannot choose, the prioritization is not ready.
- **"Is the impact based on data or on desire?"** — Impact scores must reference baseline metrics or evidence, not just "it feels important."
- **"Is the confidence calibrated? 5 = strong evidence, not 5 = seems good"** — Push for honest confidence ratings. Most items should be 2-4, not 5.
- **"Have we considered what happens if we do nothing?"** — The cost of inaction informs whether something is truly P0.

The goal is to sharpen the ranking's quality, not to block progress. If the ranking is well-justified, acknowledge it and move on quickly.

## ANTI-PATTERNS

These anti-patterns come from the team's real experience (KB). Flag them actively during the interview and generation:

1. **Everything is P0** — If all items are P0, the prioritization has failed. Push back: "We have [N] P0 items. That means all compete for the same capacity. Which 1-2 are truly non-negotiable?"

2. **Score as automatic decision** — The score is a tool, not the truth. Scores inform the ranking but don't dictate it. Dependencies, risks, and strategic alignment also matter. Flag if the user treats score as gospel: "The score suggests [X], but does that account for [dependency/risk]?"

3. **Prioritizing without dependencies** — An item that depends on another cannot come first. Always check: "Does this require something else to be built first?"

4. **Hiding constraints** — Capacity, legal requirements, integration dependencies, and team availability all affect what can actually be done. Push for disclosure: "Are there constraints (capacity, legal, integrations) that affect this ranking?"

5. **Table without justification** — A spreadsheet of numbers without written rationale is not a prioritization document. Every score needs 2-5 lines of justification.

6. **Effort estimated by PM alone** — Effort estimates must be validated with the Tech Lead. Flag if missing: "Who validated this effort estimate?"

## CONTEXT LOADING

Load context in this order of priority:

1. **$ARGUMENTS**: If the user passes `[context-path]`, read that file directly.
2. **Handoff Registry**: Check `docs/ets/projects/{project-slug}/state/reports/` for upstream planning artifacts.
3. **Document Scan**: Scan `docs/ets/projects/{project-slug}/planning/` for ost.md. Load O-# opportunities. Also scan `docs/ets/projects/{project-slug}/discovery/` for baseline.md and product-vision.md.
4. **User Interview**: If nothing found, begin the prioritization interviews interactively.

## INTERVIEW PROTOCOL

This interview follows a one-question-at-a-time rhythm. Ask each question alone in one message, wait for the user's answer, then decide whether to ask a follow-up or move forward.

### Block 1: Scope & Method

**Question 1** (ask alone, one message):
> "O que estamos priorizando? Oportunidades (O-#) da OST ou solucoes/hipoteses? Recomendacao: primeiro priorize oportunidades; depois detalhe hipoteses dentro do top P0."

Wait for the answer. Extract: unit of prioritization (opportunities, solutions, or hypotheses).

**Question 2** (ask alone, one message):
> "Qual metodo preferem? Apresento as opcoes: (A) ICE = (Impacto x Confianca) / Esforco — mais simples e rapido, funciona bem quando o alcance e similar entre itens; (B) RICE = (Reach x Impact x Confianca) / Esforco — melhor quando os itens tem audiencias muito diferentes. Recomendo [A or B] porque [rationale based on loaded context]. Qual preferem?"

Wait for the answer.

### Block 2: Item Scoring (one at a time)

For each O-# from the OST:

**Question 3** (ask alone, one message, for each item):
> "Para [O-# — titulo]: qual o impacto esperado? (1-5). Justifique com base em baseline — qual metrica muda, de quanto para quanto?"

Wait for the answer. If impact is 5 without strong evidence, challenge it.

**Question 4** (ask alone, one message):
> "Qual sua confianca nesse impacto? (1-5). Quais evidencias sustentam? (dados, discovery, historico)"

Wait for the answer. If confidence is 5, push for specific evidence.

**Question 5** (ask alone, one message):
> "Qual o esforco estimado? (1-5). Essa estimativa foi validada com o Tech Lead? Quais as principais complexidades?"

Wait for the answer. If not validated with Tech Lead, flag it.

After scoring, compute and present:
> "Score para O-[#]: ICE = ([I] x [C]) / [E] = [score]. Dependencias: [list]. Riscos: [list]. Prioridade sugerida: [P0/P1/P2] porque [rationale]."

Repeat Block 2 for each item.

### Block 3: Ranking & Trade-offs

**Question 6** (ask alone, one message):
> "Baseado nos scores, proponho este ranking: [P0/P1/P2 list]. Concorda? Quer ajustar algum item?"

Wait for the answer. If user adjusts, update and re-present.

**Question 7** (ask alone, one message):
> "O que ficou de fora e por que? Algum trade-off que precisa ser documentado? Quais riscos estamos aceitando?"

Wait for the answer.

## OUTPUT FORMAT

The generated `docs/ets/projects/{project-slug}/planning/prioritization.md` contains:

- **Header**: Title, version, date, owner, participants, method chosen, unit prioritized, links to OST/Discovery/Baseline
- **1. Contexto e objetivo**: Why prioritizing now, which decision to close (5-10 lines)
- **2. Regras do jogo** (method and scales):
  - Method formula: ICE or RICE
  - Scale definitions (1-5 for each dimension)
- **3. Lista de itens a priorizar**: Items from OST with O-# references
- **4. Avaliacao e score** (repeated block for each item):
  - Impacto (1-5) + justificativa (2-5 linhas, com baseline → target)
  - Confianca (1-5) + justificativa (quais evidencias)
  - Esforco (1-5) + justificativa (validado com Tech Lead)
  - Score calculado
  - Dependencias e riscos
  - Prioridade sugerida: P0/P1/P2 com racional
- **5. Ranking final**:
  - P0 (neste ciclo) — com 1 linha de justificativa cada
  - P1 (proximo ciclo)
  - P2 (backlog/avaliar depois)
- **6. Trade-offs e decisoes**:
  - O que ficou de fora e por que
  - Quais riscos estamos aceitando
  - Quais dependencias precisam ser resolvidas primeiro
- **7. Proximos artefatos** (o que isso destrava): PRDs, backlog, release

**SST Rule:** ICE/RICE scores, P0/P1/P2 ranking, and trade-off decisions ONLY in this document. No other document should redefine scores or the priority ranking.

## ID GENERATION

No new IDs — this document references O-# from OST and generates P0/P1/P2 classification.

Downstream traceability: `O-# (from ost.md) → P0 items → PRD-F-# features in prd.md`

## KNOWLEDGE POINTERS

- Read `knowledge/template.md` for the prioritization document template and structure.

## INPUT VALIDATION

**ost.md** (BLOCKS):
- Must contain at least 1 O-# opportunity with evidence
- Must have an Outcome section with measurable metrics

## OUTPUT VALIDATION

Before marking this document as COMPLETE:
- [ ] Contexto e objetivo states why prioritizing now and which decision to close
- [ ] Method chosen (ICE or RICE) with scale definitions
- [ ] At least 3 items scored with all dimensions (Impact, Confidence, Effort)
- [ ] Every Impact score has written justification with baseline reference when possible
- [ ] Every Confidence score has written justification citing evidence type
- [ ] Every Effort score indicates whether validated with Tech Lead
- [ ] Score calculated correctly for each item
- [ ] Ranking section has P0/P1/P2 classification with 1-line justification per item
- [ ] Trade-offs section documents what was deprioritized and why
- [ ] Dependencies documented for items with cross-cutting concerns
- [ ] Source Documents section present at top referencing ost.md

If any check fails → mark document as DRAFT with `<!-- STATUS: DRAFT -->` at top.

## CLOSING SUMMARY

After saving and validating, display:

```text
prioritization.md saved to `docs/ets/projects/{project-slug}/planning/prioritization.md`

Status: [COMPLETE | DRAFT]
Method: [ICE | RICE]
Items scored: [count]
P0: [count] | P1: [count] | P2: [count]
Trade-offs documented: [count]
```

Then present these options using AskUserQuestion (or as a numbered list if AskUserQuestion is unavailable):

1. **Proceed to PRD (Recommended)** — P0 items become PRD features (PRD-F-#)
2. **Refine scores** — Adjust specific items (e.g., after Tech Lead validation)
3. **Add more items** — If OST was updated with new opportunities
4. **Pause for now** — Save and return later (the document is already on disk)

Wait for the user to choose before taking any action. Do not auto-proceed to the next skill.

## WORKFLOW

### Step 1: Context Loading
- **Input:** `ost.md` (BLOCKS), optionally `baseline.md` (ENRICHES), `product-vision.md` (ENRICHES)
- **Action:** Extract O-# opportunities, baseline metrics, BO-# objectives. Summarize key points to the user to show you've absorbed the context.
- **Output:** Internal context object

### Step 2: Pressure Test
- **Input:** Step 1 context
- **Action:** Challenge the prioritization framing with 1-2 pressure test questions. Verify that there are genuinely multiple competing items (if only 1, suggest versao curta).
- **Output:** Validated/refined framing

### Step 3: Prioritization Interview (one question at a time)
- **Input:** Step 1-2 context + user responses (interactive)
- **Action:** Run the 3-block INTERVIEW PROTOCOL. Ask one question per message, wait for answers. For each item, ensure all scoring dimensions have justification. Flag anti-patterns actively.
- **Output:** Raw interview notes (internal)

### Step 4: Section-by-Section Document Generation
- **Input:** Interview notes from Step 3
- **Action:** Generate the document one major section at a time, using the template from `knowledge/template.md`. For each section:
  1. **Propose approach** — Before generating, briefly describe how you plan to frame this section
  2. **Generate the section** — Present it to the user
  3. **Ask for approval** — "Does this capture it well? Anything to adjust?"
  4. **Incorporate feedback** — If the user wants changes, revise and re-present
  5. **Move to next section** — Only after the user approves

  Section order:
  - Contexto e objetivo
  - Regras do jogo (method and scales)
  - Lista de itens a priorizar
  - Avaliacao — Item 1 (impact, confidence, effort, score, dependencies, priority)
  - Avaliacao — Item 2 (repeat)
  - ... (repeat for each item)
  - Ranking final (P0/P1/P2)
  - Trade-offs e decisoes
  - Proximos artefatos
- **Output:** Approved sections assembled into complete prioritization.md

### Step 5: Right-Size Check
- **Action:** Before saving, assess whether the document's depth matches the work's complexity:
  - If there's only 1 item to prioritize → offer "versao curta" with just the scoring and rationale
  - If there are >7 items and some lack justification → flag gaps for the user
  - Simple work deserves a short document. Don't pad sections to fill a template.
- **Output:** Document trimmed or flagged, ready for save

### Step 6: Pre-Finalization Check
- **Action:** Before saving, verify completeness by asking yourself:
  1. What would the PRD skill still have to invent if this prioritization is all they get?
  2. Are there P0 items without clear justification?
  3. Are there items without effort validation from Tech Lead?
  4. Is there a low-effort addition (e.g., one more dependency check, one clarification) that would significantly improve the PRD phase?
  If gaps are found, address them or flag them as outstanding questions before saving.
- **Output:** Document verified or gaps addressed

### Step 7: Save Artifact
- **Action:**
  1. Verify directory exists: `docs/ets/projects/{project-slug}/planning/` — create if missing
  2. Write the complete document to `docs/ets/projects/{project-slug}/planning/prioritization.md` using the Write tool
  3. The document is only saved when written to the filesystem — presenting content in chat is not the same as saving.
- **Output:** File written to disk at the specified path

### Step 8: Spec Review
- **Action:** After saving the artifact, dispatch the spec-reviewer agent to review the saved document with fresh context:
  1. Provide the spec-reviewer with: the saved file path (`docs/ets/projects/{project-slug}/planning/prioritization.md`) + paths to upstream documents (BLOCKS: `docs/ets/projects/{project-slug}/planning/ost.md`)
  2. The reviewer checks: completeness, scoring consistency, justification quality, anti-pattern compliance, SST compliance
  3. If **Approved** → proceed to user review gate
  4. If **Issues Found** → address the issues, re-save, re-dispatch reviewer (max 3 iterations)
  5. If still failing after 3 iterations → present issues to the user for guidance
- **Output:** Reviewed and approved document

### Step 9: User Review Gate
- **Action:** After the spec reviewer approves, ask the user to review the saved document:
  > "Document saved to `docs/ets/projects/{project-slug}/planning/prioritization.md`. The spec reviewer approved it. Please review and let me know if you want any changes before we proceed."
  Wait for the user's response. If they request changes, make them and re-run the spec review. Only proceed to validation after user approval.
- **Output:** User-approved document

### Step 10: Validation
- **Input:** Generated document
- **Action:** Run OUTPUT VALIDATION checklist
- **Output:** Document marked COMPLETE or DRAFT

### Step 11: Handoff Options
- **Action:** Present multiple next-step options (see CLOSING SUMMARY)

## ERROR HANDLING

| Error | Severity | Recovery | Fallback |
|-------|----------|----------|----------|
| BLOCKS dep missing (ost.md) | Critical | Auto-invoke ost skill — opportunities are needed to prioritize | Pause until ost is available |
| BLOCKS dep is DRAFT | Warning | Proceed with available context, noting opportunity quality may be lower | Add `<!-- ENRICHMENT_MISSING: ost is DRAFT -->` |
| ENRICHES dep missing (baseline.md) | Low | Proceed — impact can be estimated without precise baseline | Note that impact scores may need revision after baseline is defined |
| ENRICHES dep missing (product-vision.md) | Low | Proceed — strategic alignment can be assessed without formal vision | Note that priority alignment may need revision |
| User rates all items as P0 | High | Push back: "If everything is P0, nothing is P0. Force-rank the top 1-2." | Accept max 3 P0 items, flag the rest |
| Effort not validated with Tech Lead | Medium | Flag: "Effort estimate not validated — cap confidence at 3 for this item" | Add `<!-- EFFORT: PM estimate only -->` |
| Only 1 item to prioritize | Low | Offer versao curta — still document rationale and risks | Generate abbreviated document |
| Output validation fails | High | Address gaps, re-present sections to user | Mark as DRAFT |

## QUALITY LOOP

This skill supports iterative quality improvement when invoked by the orchestrator or user.

### Cycle

1. **Generate** — Produce initial document following WORKFLOW steps
2. **Self-Evaluate** — Score the output against OUTPUT VALIDATION checklist
   - Calculate: completeness % = (passing checks / total checks) x 100
   - If completeness >= 90% → mark COMPLETE, exit loop
   - If completeness < 90% → proceed to step 3
3. **Identify Issues** — List each failing check with specific gap description
4. **Improve** — Address each issue, regenerate affected sections only
5. **Re-Evaluate** — Score again against OUTPUT VALIDATION
   - If improved by < 5% from previous iteration → diminishing returns, mark DRAFT with notes
   - If completeness >= 90% → mark COMPLETE, exit loop
   - If max iterations (3) reached → mark DRAFT with iteration log
6. **Report** — Log to stdout: iteration count, score progression, remaining gaps if any

### Termination Conditions

| Condition | Action | Document Status |
|-----------|--------|-----------------|
| Completeness >= 90% | Exit loop | COMPLETE |
| Improvement < 5% between iterations | Exit loop (diminishing returns) | DRAFT + notes |
| Max 3 iterations reached | Exit loop | DRAFT + iteration log |

### Invocation

- **Automatic:** Orchestrator invokes Quality Loop for all high-dependency documents
- **Manual:** User can request `--quality-loop` on any skill invocation
- **Skip:** User can pass `--no-quality-loop` to disable (generates once, validates once)
