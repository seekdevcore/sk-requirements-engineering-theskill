<!-- The imperative spine of the skill: every "the skill says do X" reframed as a reflex trigger. -->
# 14 — Triggers (the skill ACTS, not just advises)

> A skill is knowledge an agent *reads* — it does not execute itself. That is why spikes, issues, and bugs
> that the skill *says* to create were never created by default, and why the mandatory §0 check was skipped.
> This reference turns the skill's whole guidance into **reflex triggers**: `WHEN <observable condition in the
> work> → THEN <action> [via <tool>]`. When you observe the condition, you **act immediately** — you do not
> ask permission for the deterministic ones, and you *do* ask for the genuine user decisions (marked
> `AskUserQuestion`).
>
> **The tools that make the action one step** (the generative layer — [`SKILL.md §5`](../SKILL.md)):
> `new-item.sh <kind>` allocates the next free id + instantiates the right template (kinds: spike · bug · issue ·
> qa · tx · epic · feature · rf · rnf · pm · runbook · adr · sprint) · `gen-done-view.sh` regenerates the
> Status-driven done ledger · `scaffold-structure.sh` builds/migrates the structure · the MCP tools
> `create_item`/`generate_done_view`/`close_item` (imperative) and `validate_user_story`/`validate_acceptance_criterion`/`validate_ears`/`check_projection_drift` (advisory).

## The two standing triggers (behind everything)

| # | WHEN | THEN | via |
|---|---|---|---|
| **T0** | the skill first touches ANY project/folder (before creating or editing a single requirement) | run the structure-state check as the **automatic first action** → classify GREENFIELD/HAS-STRUCTURE/LOOSE-FILES/LEGACY-MONOLITH and act on the verdict | `scaffold-structure.sh` ([SKILL §0](../SKILL.md)) |
| **T-zero** | about to add/alter/remove **anything** in the backlog | first verify the requirements **document** changed (rule zero); a backlog change with no documented origin is scope-creep → record it in the document first | manual ([SKILL §2.1](../SKILL.md)) |

## §0 — Structure (the first-run decisions)

| # | WHEN | THEN | via |
|---|---|---|---|
| 1 | you have not yet read the project | auto-analyze existing docs/README/source/roles/entities/stack before asking anything | manual (§0.1) |
| 2 | the `specs/` vs `--no-specs` (ADR tiering) choice is genuinely ambiguous | ask the user (clear signals → state the default and proceed) | **`AskUserQuestion`** (§0.3a) |
| 3 | an existing project shipped code/features without RE docs | ask whether to backfill — offer scope full / task-scoped / structure-only (recommend task-scoped) | **`AskUserQuestion`** (§0.3b) |
| 4 | verdict is LEGACY-MONOLITH (one loose requirements doc, no spine) | scaffold, then split it per module into `rf`/`rnf` + personas + glossary, keep the monolith as a linked overview | `scaffold-structure.sh` + `new-item.sh rf/rnf` (§0.4) |
| 5 | a seed file still contains `<...>`/`RF-NNN`/`EP-NN` | adapt it to this project's reality — never commit placeholders | manual (§0.5) |

## Elicitation & analysis

| # | WHEN | THEN | via |
|---|---|---|---|
| 6 | starting any project, before elicitation | run the 3-question feasibility study; any "no" → question proceeding | manual ([01 §6](01-fundamentos.md)) |
| 7 | eliciting | always combine **2+** techniques; forgotten stakeholder = forgotten requirement | manual ([02 §3](02-elicitacao.md)) |
| 8 | an elicitation smell appears (all "must be fast", only "end user", no NFR/domain rule, screens in the first meeting) | go back to Phase A (re-elicit) | manual ([02 §11](02-elicitacao.md)) |
| 9 | mapping a business process (multi-system / org change / >R$500k / regulation) | run AS-IS → TO-BE → GAP; each gap → a requirement (software **or** process/policy) | `new-item.sh rf/rnf` ([08 §3](08-analista-negocios.md)) |
| 10 | a rule comes from the domain/regulation, not a user | record it as a business rule `G-NN` and put a domain specialist in the review | manual ([01 §4](01-fundamentos.md)) |

## Specification & creation (the generative reflexes)

| # | WHEN | THEN | via |
|---|---|---|---|
| 11 | discovered findings must be documented | materialize the hierarchy Epic → Feature → US → CA | `new-item.sh epic/feature` + `rf/rnf` |
| 12 | you **cannot estimate** a story (missing understanding, `?`/`100` in Planning Poker, unknown feasibility) | create a **time-boxed spike** (`?`→ also talk to the PO; `100`→ slice the disguised epic) | **`new-item.sh spike`** ([03 §5](03-especificacao.md), [05-estimativa §4](05-estimativa.md)) |
| 13 | a defect violates a specific `CA` | create a **`BUG-NN`** ("Bug" type parented to the violated US/Feature), linked ↑ to CA/US/RF | **`new-item.sh bug`** |
| 14 | a raw report / incoming item arrives | create an **`ISS-NN`** in the triage inbox → triage into bug/spike/tx/improvement/incident | **`new-item.sh issue`** |
| 15 | a cross-cutting tests/reviews/quality-gate activity is needed | file a **`QA-NN`** under the Q&A child Epic | **`new-item.sh qa`** |
| 16 | technical config/infra work serves the whole project (ESLint, env, CI, docker) — **not** a Feature | file a **`TX-NN`** under support/ (naming rule 4/6) | **`new-item.sh tx`** |
| 17 | a design decision (the "how") is taken | record an **ADR** in the correct tier under the one global sequence; changing a decision → a NEW ADR that supersedes (never edit/renumber) | **`new-item.sh adr`** ([10 §5](10-estrutura-projeto.md)) |
| 18 | planning a sprint's execution | materialize a thin, link-first **sprint** doc (per-person blocks; US that slip → "Adiados" + ⤳ Skipped) | **`new-item.sh sprint`** |
| 19 | authoring a Feature | business-language description + ACs; **never** BDD in a Feature (BDD lives in the US) | `validate_acceptance_criterion` (§5 / [04 §7.7](04-bdd-criterios-aceitacao.md)) |
| 20 | authoring a User Story | BDD (Given/When/Then) in its Description; ACs inherited; short descriptive title (Connextra stays in the body) | `validate_user_story` |
| 21 | an AC needs sub-rules to be testable | end the title with `[...]`, open the body with `Rules to be applied:` | `validate_acceptance_criterion` ([04 §2.5](04-bdd-criterios-aceitacao.md)) |
| 22 | a candidate Feature bundles ≥2 capabilities (register + update) | split into atomic one-thing Features | `new-item.sh feature` (rule 9) |
| 23 | a title uses an infinitive verb or a technical term | rewrite as noun/gerund, business language (tech terms only in Tasks) | manual (rules 1–2) |
| 24 | creating any node | declare a priority 🔴/🟠/🟡/🟢 and a stable eternal id (never renumber) | `new-item.sh` (allocates the id) |

## Estimation & the refinement gradient (iceberg)

| # | WHEN | THEN | via |
|---|---|---|---|
| 25 | an item is at the backlog **tip** (next 1–2 sprints) | fully refine it: complete BDD + grouped CAs + edge cases + binding RNF — meet **Definition of Ready** | `validate_user_story` ([03 §4.5](03-especificacao.md)) |
| 26 | an item is at the **base** (months away) | keep it macro (1–2 sentences); **no** speculative BDD/CAs | manual ([03 §4.5](03-especificacao.md)) |
| 27 | a US is about to enter a sprint **without** DoR (no BDD/CAs/points) | do NOT pull it in — return to refinement | `validate_user_story` ([05-estimativa §11](05-estimativa.md)) |

## Validation

| # | WHEN | THEN | via |
|---|---|---|---|
| 28 | a requirement is **qualitative** ("must be fast/easy/secure") | quantify it into a measurable NFR **immediately** (never "later") | `validate_acceptance_criterion` (§4.2) |
| 29 | a requirement must be unambiguous / edge-case / regulated / for an AI implementer | phrase it in **EARS** (one `SHALL`/`DEVE` per statement) — keep business language for early/lay-stakeholder work | `validate_ears` ([11](11-ears.md)) |
| 30 | accepting any requirement/feature into the backlog | run **Falbo's 7 + 5W1H**; a genuinely unanswerable question → incomplete → return to the stakeholder | `validate_user_story`/`validate_acceptance_criterion` (§9) |
| 31 | writing CA and BDD | author **both** (invariant × interaction) — never only one | both `validate_*` ([04 §1](04-bdd-criterios-aceitacao.md)) |
| 32 | a requirement is being written with no identified stakeholder/owner | stop — a requirement without an owner is unvalidated | manual (anti-pattern 5) |

## Change, traceability & the "after" loop

| # | WHEN | THEN | via |
|---|---|---|---|
| 33 | a requirement change is proposed | run the formal change process (problem → impact+cost → implement); update the **document first**, then backlog/design/code, sync the RTM in the **same PR** | manual ([07 §3](07-mudanca-rastreabilidade.md)) |
| 34 | a production **incident** occurs (a dependability RNF/CA failed) | write a **postmortem** linked ↑ to the RNF/CA, ← to the origin ISS/alert, ↓ to corrective BUG/TX (through the doc first) | **`new-item.sh pm`** ([13 §11](13-confiabilidade-seguranca.md)) |
| 35 | a resilience/availability RNF (`RTO`/`RPO`/`AVAIL`) must be operationalized | author a **runbook** linked ↑ to that RNF | **`new-item.sh runbook`** ([13 §6](13-confiabilidade-seguranca.md)) |
| 36 | an item's Status becomes **✅ Done** | set Status **in place** (never `git mv`) + regenerate the read-only done ledger | **`gen-done-view.sh`** / `close_item` |
| 37 | a dependability attribute is qualitative | quantify it: pick `POFOD`/`ROCOF`/`MTTF`/`AVAIL`/`RTO`/`RPO` + target + measurement | `new-item.sh rnf` ([13 §3](13-confiabilidade-seguranca.md)) |
| 38 | authoring postmortem/runbook prose (timeline, 5-whys, steps) | delegate the craft to the `documentation-engineer` agent / `postmortem-writing` · `incident-runbook-templates` skills — the skill owns only the home + links | delegate ([13 §11](13-confiabilidade-seguranca.md)) |

## Ethics (the layer below all others)

| # | WHEN | THEN | via |
|---|---|---|---|
| 39 | any substantive feature is reviewed | run the ethical checkpoint (privacy/LGPD, harm, ML re-evaluation); fold ethics issues into **acceptance criteria**, not a side doc | manual ([09 §3](09-etica-sbc.md)) |
| 40 | a requirement collects personal data | add NFRs: minimization, retention+deletion, consent, portability, audit logging | `new-item.sh rnf` ([09 §2.5](09-etica-sbc.md)) |
| 41 | the system automates a critical decision about people (ML/AI) | add NFRs (periodic risk re-eval, drift, explainability, contestation, bias audit) — or do not deploy | `new-item.sh rnf` ([09 §2.7](09-etica-sbc.md)) |
| 42 | misuse or harm is foreseen/unavoidable | invoke the professional veto — it may be best **not to build** it; record the decision | manual ([09 §2.9](09-etica-sbc.md)) |

## Integrations (project outward; source of truth stays in `docs/`)

| # | WHEN | THEN | via |
|---|---|---|---|
| 43 | the team tracks the backlog in **OpenProject** | project only `docs/backlog/`; pull to snapshot, dry-run push, then `--apply` (round-trip) | export adapter ([openproject.md](integrations/openproject.md)) |
| 44 | the project runs **OpenSpec / Spec Kit** | project a Feature down (keep `[RF-NN]` tags + verbatim Gherkin); reconcile changes back to the RF | `project-to-sdd.sh` ([sdd-interop.md](integrations/sdd-interop.md)) |
| 45 | checking docs ↔ framework sync | run drift detection (advisory; run against the **full** projection, not one feature) | `check_projection_drift` |

---

*This table is the **exhaustive** distillation; every row traces to a rule/section cited inline. It does not
replace the reference that owns each rule — it makes the rule **fire**. When in doubt whether a deterministic
trigger applies, it does: act (create the artifact, run the check) rather than defer.*
