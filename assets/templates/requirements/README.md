<!-- GENERIC TEMPLATE — adapt to your project. See references/10-estrutura-projeto.md §"Adaptation protocol". -->
# Requirements — <PROJECT NAME>

> **Source folder for the "WHAT".** Answers "what need does the system address?", without going into the "how"
> (that is `../specs/` + ADRs). The backlog only materializes what lives here — this folder is the source of truth.

## Traceability hierarchy

```
Requirement (RF/RNF)      ← THIS folder
  ↓ realized by
Epic (EP-NN)              ← ../backlog/epics/
  ↓ decomposed into
Feature (F-NN)            ← ../backlog/features/
  ↓ accepted when
Acceptance Criterion      ← inside the Feature file
  ↓ illustrated by
User Story + BDD          ← inside the Feature file
  ↓ implemented by
Task (T / TX)             ← inside the Feature file
  ↓ delivered in / materialized in
Sprint → Commit (SHA)
```

**Hard rule**: bidirectional traceability — each file cites its parent and children via a relative link.

## Structure

```
requirements/
├── README.md                 this file
├── personas-and-scenarios.md    project personas; every US references one
├── RF/   RF-NNN-<module>.md   Functional Requirements (1 file per system module)
└── RNF/  RNF-<slug>.md        Non-Functional Requirements (cross-cutting; ALWAYS quantitative)
```

> **Adapt to the project**: create one `RF-NNN-<module>.md` per real module/app of the system
> (e.g. one per bounded context, Django app, package, or domain area).

> ⚠️ **1 file per MODULE, not 1 per requirement** (a common confusion — read before assuming something is missing).
> Each file in `RF/` documents an **entire module** (one Epic), named after its **first** requirement:
> `RF-01-<module>.md` contains RF-01..RF-04; `RF-05-<module>.md` contains RF-05..RF-08; and so on.
> The individual requirements live as `### RF-NN` sections **inside** the file. So a folder that
> shows `RF-01, RF-05, RF-09…` is **not** missing RF-02/03/04 — those are sections of the first file.
> The "jumps" in the **file names** are module boundaries (contiguous ranges), never missing
> requirements. *(If you prefer 1 file per requirement, that is a valid variant — but the convention and the
> scaffolder assume 1-file-per-module.)*

## Conventions

- **Business language**. No infinitive verb in the title; no technical term (jargon belongs in ADRs/specs).
- **Immutable IDs**: `RF-NNN`, `RNF-<slug>`. Deprecated → `RF-NNN-deprecated.md` (never vanishes).
- **Priority**: 🔴 Immediate · 🟠 High · 🟡 Normal · 🟢 Low.
- **RNF is always quantitative** — "fast" is a wish; "p95 ≤ 300ms" is a requirement.
- Each file has a `## Realized by` (Epics/Features that execute it).

## How to add a requirement

1. Does the module's `RF-NNN` exist? Yes → new section. No → `RF-NNN-new-module.md` (next free number).
2. Statement in business language.
3. Explicit priority.
4. `## Realized by` (empty if there is no Epic yet).
5. When a new Epic cites this requirement, edit it here — bidirectional is mandatory.

## Canonical skill

[`engenharia-de-requisitos`](https://github.com/seekdevcore/sk-requirements-engineering-theskill) — *"IFPB"* ERS + Sommerville/Pressman/Wiegers/Cohn/BABOK v3 + SBC 002/2024 Ethics.

## Cross-references

- [Backlog](../backlog/README.md) · [Specs](../specs/) · [Project ADRs](../planning/adrs/)
