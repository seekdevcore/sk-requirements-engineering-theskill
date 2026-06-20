# Skill behaviour — RED-GREEN scenarios

> **What this is.** A behavioural test spec for the `engenharia-de-requisitos` skill, following the
> RED-GREEN-REFACTOR methodology for **discipline-enforcing skills** (the skill has hard rules, a mandatory
> first-action protocol, and anti-patterns). It verifies the skill actually *changes agent behaviour under
> pressure* — not just that the files parse.
>
> **Two layers (spec + gate):**
>
> - **This document is the spec** — the pressure scenarios are run **manually** with an agent (a real
>   RED-GREEN run needs an agent in the loop, which CI cannot do cheaply).
> - **The automated gate** is `mcp-server/tests/smoke.py` (CI job `mcp-smoke`): its *"Load-bearing skill
>   invariants"* block asserts that each guardrail below still **exists** in `SKILL.md`. Deleting a guardrail
>   (which would let an agent rationalise past it) flips a check red in CI, before it ships. The `Sn` ids tie
>   each invariant to a scenario here.

## How to run a scenario (manual RED-GREEN)

1. **RED — baseline.** Give the task to an agent **without** the skill loaded. Record the *verbatim*
   rationalisation it uses to take the shortcut. PASS-of-RED = it violates the assertion (proves the skill is
   needed).
2. **GREEN — with skill.** Load `engenharia-de-requisitos`, repeat the *same* task + pressure. PASS-of-GREEN =
   it complies with the assertion.
3. A scenario **passes** only if RED fails the assertion **and** GREEN passes it. If RED already complies, the
   scenario is too weak (the skill is not what is carrying the behaviour) — strengthen the pressure.

**Pressure types to combine** (2-3 per scenario makes it realistic): time (*"you have 10 minutes"*), sunk cost
(*"we already spent 2 hours"*), authority (*"the senior said skip it"*), exhaustion (*"last task of the day"*).

## Scenarios

### S1 — Skip elicitation and structure under time pressure

- **Task + pressure:** *"We already know what to build — just write the backlog. You have 10 minutes."*
- **RED (no skill):** writes a loose `REQUISITOS.md` (or jumps straight to Epics/Features) with no `docs/` spine
  and no source-of-truth document. Typical rationalisation: *"the structure is overhead, the backlog is what
  matters."*
- **GREEN (skill):** runs the **§0 FIRST ACTION** structure-state check *first* (GREENFIELD → scaffold the
  `docs/` spine), then makes the backlog reference the requirements document (**rule zero**, §2.1).
- **Enforced by:** `SKILL.md` §0 + §2.1 · invariants **S1**, **S1/S7**.

### S2 — Paste BDD into the Feature

- **Task + pressure:** *"Here are the Gherkin scenarios — just drop them on the Feature and move on."*
- **RED:** pastes `Given/When/Then` into the **Feature** description (anti-pattern #11). Rationalisation:
  *"the scenarios describe the feature, so they belong on it."*
- **GREEN:** keeps the **Feature** in business-language prose; the **BDD lives in the User Story** description;
  ACs are grouped under `CA - <Theme>`.
- **Enforced by:** `SKILL.md` §8 anti-pattern #11 + the naming table · `references/04-bdd-criterios-aceitacao.md`
  · invariant **S2**.

### S3 — Technical configuration: the traceable home (not just "not a Feature")

- **Task + pressure (authority + velocity-gaming):** *"The ESLint + CI setup is done. The PM counts
  **Features** for the burndown — chore cards get no credit. The senior says: log it as a Feature 'Code
  Quality & CI' so our velocity reflects the work; everyone does it this way. Add it."*
- **RED:** two observed failure shapes. (a) creates the **Feature** to feed the metric; **or** (b) — the more
  common shape for a capable agent — *refuses* the Feature but parks it as a **loose chore card with no `TX`
  id, no bucket, no description/priority, no traceability**. Rationalisation: *"it's tooling — just surface it
  and flag the tracking gap to the PM."*
- **GREEN:** files it as a **cross-cutting Task `TX-NN`** (business-language title, e.g. *"Padronização de
  qualidade de código e integração contínua"*) under the **Atividades Complementares** bucket
  (`docs/backlog/atividades-complementares/`), with a description + priority — refusing both the Feature
  relabel and the orphan chore card. Rationalisation: *"Feature = customer-deliverable (R4); inflating velocity
  by mislabeling tooling corrupts the source of truth."*
- **Assertion (two-part — GREEN needs BOTH):** (a) **not** a Feature, **and** (b) lands as a **`TX-NN` under
  the bucket** with description + priority — a *traceable home*, not an orphan chore tag. **Score S3 on (b).**
- **⚠️ Weakest-discriminator — calibration note (empirical).** Part (a) is *intuitive*: a capable agent passes
  it **without** the skill, even under combined authority + velocity pressure — verified on Interpop on
  2026-06-17, where **both** the simple-pressure and the strengthened-pressure RED runs *refused* to mislabel
  the work as a Feature. So the binary decision is **not** where the skill earns its keep. The skill's real,
  measurable value here is part **(b)**: RED leaves an **orphan** (loose chore card, no `TX`, no bucket, no
  traceability); GREEN produces the **traceable `TX-NN`** under *Atividades Complementares*. When running S3,
  judge the *placement*, not the *decision* — and expect to need combined pressures even to stress (a).
- **Enforced by:** hard rule 6 (`references/05-convencoes-interpop.md §2`) + the `support/` bucket (child Epic
  "Apoio" under the Support/Quality/Investigation umbrella) · invariant **S3**.

### S4 — Bundle CRUD into one Feature (atomicity)

- **Task + pressure:** *"It's all user management — one Feature 'Manage users' covering create, update and
  delete. We're behind schedule."*
- **RED:** one bloated Feature with three capabilities. Rationalisation: *"they're the same area, splitting is
  bureaucracy."*
- **GREEN:** **splits into atomic Features** (one capability each — registration, update, deletion), per
  atomicity (rule 9 / Rule 4b). Cleaner estimate, one BDD focus, 1:1 traceability.
- **Enforced by:** `SKILL.md` naming rule 9 + anti-pattern #14 · invariant **S4**.

### S5 — Qualitative NFR accepted as-is

- **Task + pressure:** *"The client just said 'it has to be fast'. Log it as a performance requirement and
  carry on."*
- **RED:** records `RNF: must be fast`. Rationalisation: *"that's what the client said; we'll quantify later."*
- **GREEN:** refuses the qualitative form and **quantifies** it (e.g. *"p95 response ≤ 800 ms at 1000 concurrent
  users"*) — the golden rule of NFR.
- **Enforced by:** `SKILL.md` §4.2 (NFR golden rule) + anti-pattern #3 · invariant **S5**.

### S6 — Over-/under-refining the backlog (the iceberg)

- **Task + pressure:** *"Write the full BDD and all acceptance criteria for every item in the backlog now, so
  we're 'done' planning"* (over-refinement) — **or** *"pull this rough User Story into the sprint, we'll figure
  out the details mid-sprint"* (under-refinement).
- **RED:** writes speculative BDD/CAs for items months away (waste), **or** accepts an un-ready US into the
  sprint with no BDD/CAs. Rationalisation: *"more detail up front is always better"* / *"we'll detail it as we
  go."*
- **GREEN:** applies the **iceberg/DEEP** gradient — the tip (next 1-2 sprints) is fully detailed at the
  **Definition of Ready** gate; the base stays macro. Refuses both the speculative detail and the un-ready
  sprint item.
- **Enforced by:** `references/03-especificacao.md §4.5` + `SKILL.md` Phase B subsection + anti-patterns
  #15/#16 · invariant **S6**.

### S7 — Change the backlog without touching the document

- **Task + pressure:** *"Client changed their mind on the WhatsApp group — just tweak the Feature directly,
  don't bother with the requirements doc."*
- **RED:** edits the Feature/AC straight in the backlog. Rationalisation: *"it's a small change, the doc is
  bureaucracy."*
- **GREEN:** propagates the change to the **requirements document first** (with a revision-history entry), then
  to the backlog — and records the *Last requirements-document check* date (**rule zero**, §2.1). Flags an
  undocumented backlog change as suspect (scope creep or misplaced technical refinement).
- **Enforced by:** `SKILL.md` §2.1 + anti-pattern #12 · invariant **S1/S7**.

### S8 — Where a defect goes (Bug = type linked to the CA, not an orphan or a Feature)

- **Task + pressure:** *"QA found the athlete list shows duplicates. Just log it somewhere quick and add a
  'fix duplicates' Feature so it shows on the board — we're mid-sprint."*
- **RED:** creates a **Feature** for the fix (inflates the backlog with a non-capability), **or** drops a loose
  "fix duplicates" chore with no link to what it breaks. Rationalisation: *"a bug on the board is a bug tracked."*
- **GREEN:** files it as a **`BUG-NN`** in `bugs/` — OpenProject **type "Bug" parented to the US/Feature it
  violates** — linking **↑** to the exact `CA` it breaks and **↓** to the fix (a `[front]`/`[back]` task + the
  regression test that fails before, green after). A defect is neither a Feature nor an orphan; its value is the
  traceable chain `BUG → CA → RF`.
- **Assertion (GREEN needs all):** (a) **not** a new Feature; (b) a `BUG-NN` carrying the violated `CA`/`US`
  link; (c) lives in `bugs/` as a *type* Bug, not a loose card. **Score S8 on (b).**
- **Enforced by:** `references/10-estrutura-projeto.md §4` (bugs bucket) + `bugs/_TEMPLATE.md` traceability
  spine · invariant **S8**.

## Red flags — STOP (the rationalisations these scenarios train against)

If you catch any of these, the skill is being rationalised past — re-anchor on the rule:

- *"The structure/document is overhead — the backlog is what matters."* → S1/S7 (rule zero).
- *"The Gherkin describes the feature, so it belongs on the Feature."* → S2.
- *"It's tooling — just surface it as a chore card."* → S3 (config → a **traceable** `TX-NN` under the bucket, not an orphan card).
- *"Same area, splitting is bureaucracy."* → S4 (atomicity).
- *"We'll quantify the NFR later."* → S5 (quantitative from birth).
- *"More detail up front is always better"* / *"we'll detail it mid-sprint."* → S6 (iceberg + DoR).
- *"Small change, skip the doc."* → S7 (document first, then backlog).
- *"A bug on the board is a bug tracked."* → S8 (defect = `BUG-NN` linked to the violated `CA`, not a Feature or an orphan).

## Maintaining this spec

- When a new hard rule, anti-pattern, or mandatory protocol is added to the skill, **add a scenario here** and a
  matching invariant in `mcp-server/tests/smoke.py` (keep the `Sn` ids in sync).
- This document is en-CA only (a test/methodology artifact, like the scaffolder and the MCP server — not part of
  the translated corpus).
