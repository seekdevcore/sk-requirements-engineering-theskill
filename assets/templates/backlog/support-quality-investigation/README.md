<!-- MANDATORY STRUCTURAL BUCKET (a directory, not an EP-NN file) — seeded by the scaffolder; skips if it exists.
     en-CA folder name: `support-quality-investigation/`. On OpenProject export it COLLAPSES into a ROOT Epic
     named (pt-BR) "Atividades de Apoio, Qualidade e Investigação", depth 0, sibling of the feature-front Epics
     (e.g. "Aplicação Web"). This README is that Epic's body/vision. Its three child directories each export as a
     CHILD Epic of this umbrella: support/ → "Apoio", qa/ → "Q&A", issues/ → "Issues" (with issues/spikes/ →
     "Spikes" under it). The adapter `_BUCKETS` maps each en-CA folder to its pt-BR Epic title. -->
# Support, Quality & Investigation (*Atividades de Apoio, Qualidade e Investigação*) — backlog umbrella bucket

> **What it is**: an umbrella directory-bucket, **child of `backlog/`** (sibling of `epics/`, `features/`, `sprints/`).
> **On OpenProject**: a **ROOT Epic** "Atividades de Apoio, Qualidade e Investigação" with **three child Epics**.
> **Global priority**: 🟡 Normal (an individual item may rise).

---

## Product vision (becomes the Epic *description* on export)

Single home for the **cross-cutting work that serves the whole project and belongs to no single Feature**: technical support, quality assurance, and the triage/investigation funnel. Feature-bound work never lives here — it is parented to the Feature it serves (the *type says what it is; the parent says whom it serves*).

## Child Epics (each subdirectory → a child Epic on export)

| Folder (en-CA) | Child Epic (pt-BR) | Houses | ID |
| --- | --- | --- | --- |
| [`support/`](support/) | **Apoio** | cross-cutting technical / config / infra tasks (not tied to a US) | `TX-NN` |
| [`qa/`](qa/) | **Q&A** | quality assurance — **tests**, code review, quality gates, hardening | `QA-NN` |
| [`issues/`](issues/) | **Issues** | triage inbox (raw items → reclassified & moved) | `ISS-NN` |
| [`issues/spikes/`](issues/spikes/) | **Spikes** *(child of Issues)* | time-boxed investigations producing an ADR/finding | `SPK-NN` |

> **Bugs do NOT live here.** A `BUG-NN` is a work-package of **type "Bug"** parented to the US/Feature it violates (it inherits that Feature's Epic). See [`../bugs/README.md`](../bugs/README.md).

## Traceability

Every item under this umbrella keeps the bidirectional spine: it links **↑** to what it serves (an RNF, a Feature, a decision) and **↓** to what it produces (a test, an ADR, a reclassified `BUG/SPK/TX`). This `README.md` is **not** exported as an item — it is the umbrella Epic's description.

## Related ADRs

`<cross-cutting decisions about tooling/quality/infra, if any → ../../planning/adrs/>`
