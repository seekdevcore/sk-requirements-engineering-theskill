<!-- GENERIC TEMPLATE — adapt to your project. See references/10-estrutura-projeto.md §"Adaptation protocol". -->
# Backlog — <PROJECT NAME>

> **Source folder for "WHO does WHAT, WHEN".** The **why** lives in `../requirements/`. The **how** in `../specs/` + ADRs.
>
> Last requirements-document check: DD/MM/YYYY — no changes
> (update every time you check the requirements before touching the backlog — SKILL §2.1)

## Structure

```
backlog/
├── README.md                  this file
├── glossary.md               domain vocabulary (every US/CA/ADR must use these terms)
├── epics/                     EP-NN-<slug>.md  — Application→Module→Component (MAX. 3 Epic levels) → Features
├── features/                  F-NN-<slug>.md   — description + CAs + USs (with BDD) + Tasks
├── improvements/                 ← MANDATORY bucket → root Epic "Melhorias" (Improvements) on export
│   ├── README.md              what it is + Epic description
│   └── <F/US>-<slug>.md        each product improvement (becomes a child of the Epic)
├── bugs/                      ← DEFECTS bucket → type "Bug" parented to the violated US/Feature (NOT an Epic)
│   ├── README.md              why a bug is a type, not an Epic
│   └── BUG-NN-<slug>.md        each defect (links to the CA it violates)
├── support-quality-investigation/  ← UMBRELLA bucket → root Epic "Atividades de Apoio, Qualidade e Investigação"
│   ├── README.md              umbrella Epic description + 3 child Epics
│   ├── support/               → child Epic "Apoio"  — TX-NN (technical/config/infra; was atividades-complementares)
│   ├── qa/                    → child Epic "Q&A"    — QA-NN (tests · reviews · gates)
│   └── issues/                → child Epic "Issues" — ISS-NN (triage)
│       └── spikes/            → child Epic "Spikes" — SPK-NN (time-boxed investigation)
├── sprints/                   sprint-N-<slug>.md — temporal execution (US/Task mapping)
└── done/README.md             GENERATED done view (Status-driven; items are NOT moved) — `assets/gen-done-view.sh`
```

> **Depth rule — MAX. 3 Epic levels.** The front (`Web Application`/`Mobile`) is the root Epic (level 1); below it comes the **Module** (level 2) and the **Component** (level 3) — and then the **Feature**. After the module Epic there is **only one more** Epic (the component) before the Feature. Do not nest a 4th Epic level (e.g. `Application › Module › X Management › X Lookup › Feature` is too deep — collapse to `Application › Module › Component › Feature`).
>
> **en-CA names, pt-BR Epics.** The folders follow the en-CA pattern (`support/`, `qa/`, `issues/`, `spikes/`) like `epics/`/`features/`; the adapter (`_BUCKETS`) restores the Epic's pt-BR name on export ("Apoio", "Q&A", "Issues", "Spikes", "Atividades de Apoio, Qualidade e Investigação").
>
> **Structural buckets** (directories, not `EP-NN` files): **`improvements/`** = improvements to what already exists (→ root Epic). **`support-quality-investigation/`** = cross-cutting umbrella (→ root Epic with 3 child Epics). **`bugs/`** is different: each `BUG-NN` is a work-package **type "Bug" parented to the US/Feature it violates** (inherits its Epic), **not** an Epic of its own — so the defect stays one link away from the `CA`. Mother rule: *the type says what it is; the parent says whom it serves.*

## Naming (hard rule)

| Level | Allowed in the title | NOT allowed in the title |
| --- | --- | --- |
| Epic | Noun + adjective | Infinitive, technical term |
| Feature | Noun + adjective | Infinitive, technical acronym |
| CA | Verifiable state | Vague ("Performance OK") |
| US | "As a [persona], I want [action], so that [value]" | Mixing technical and business |
| Task | **MAY** use technical terms | (the only level where technical is OK) |

## Canonical IDs (immutable after creation)

| Type | Format | Example |
| --- | --- | --- |
| Epic | `EP-NN` | `EP-10` |
| Feature | `F-NN` | `F-30` |
| Acceptance Criterion | `CANN` (in the parent Feature) | `CA01` |
| User Story | `USNN.M` | `US30.1` |
| US-bound Task | `TNN.M.K` | `T30.1.4b` |
| Cross-cutting Task (Support) | `TX-NN` | `TX-18` |
| Defect (Bug) | `BUG-NN` | `BUG-04` |
| Quality activity (Q&A) | `QA-NN` | `QA-07` |
| Triage issue | `ISS-NN` | `ISS-12` |
| Spike (investigation) | `SPK-NN` | `SPK-02` |
| Sprint | `sprint-N-slug` | `sprint-4-<slug>` |

## Priority

🔴 Immediate (blocks MVP/security) · 🟠 High (current release) · 🟡 Normal (next sprint) · 🟢 Low.

## Feature Definition of Done

1. All CAs verified by test (or manual checklist if pure UX).
2. Every US has BDD that runs green.
3. Every Task `done` with commit hash.
4. Code-review approved.
5. Coverage ≥ Sprint gate.
6. Cross-referenced documentation updated (RF/RNF cited; Sprint cites Feature).
7. Merged via PR (no `--force-push`, no `--no-verify`).
8. **Status set to `✅ Done`** and the **done view regenerated** (the item appears in `done/README.md`).

## How to close any item (no move — Status + generated view)

1. Confirm CAs/USs/Tasks `✅ Done`.
2. Update commit hashes in the item file (`features/F-NN-*.md`, `bugs/BUG-NN-*.md`, …).
3. Update the parent Epic / the Sprint / `requirements/RF-*` (`## Realized by`) cross-refs.
4. Set the item's **`Status` to `✅ Done`** (single value, in place — the file does **not** move).
5. Regenerate the done view: `bash <skill>/assets/gen-done-view.sh --root docs --apply`.
6. Commit `chore(backlog): F-NN done — status + done view`.

> **Create a new item** with `bash <skill>/assets/new-item.sh <kind> <slug> --title "…" --apply` (kinds: spike · bug · issue · qa · tx · epic · feature · rf · rnf · pm · runbook · adr · sprint) — it allocates the next free ID and instantiates the template.

## Cross-references

- [Requirements](../requirements/README.md) · [Specs](../specs/) · [Project ADRs](../planning/adrs/)
