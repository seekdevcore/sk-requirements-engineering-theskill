<!-- CHILD-EPIC BUCKET — seeded by the scaffolder; skips if it exists. en-CA folder: `qa/`.
     On OpenProject export → child Epic "Q&A" under the "Atividades de Apoio, Qualidade e Investigação" umbrella.
     Each QA-NN-*.md beside this README exports as a child of the "Q&A" Epic. -->
# Q&A — Quality Assurance (*Q&A*) — child-Epic bucket

> **What it is**: child-bucket of [`../`](../) (the Support/Quality/Investigation umbrella).
> **On OpenProject**: child Epic **"Q&A"** under the umbrella root Epic.
> **Global priority**: 🟡 Normal.

---

## Product vision (becomes the *description* of the "Q&A" Epic on export)

Home of **cross-cutting quality work** — the activities that verify the product meets its quality bar but are **not bound to a single Feature**. **Quality here includes testing.** What belongs:

- **Test design / execution / automation** (e.g. the Gherkin `.feature` files + step-defs, the test pyramid, E2E suites).
- **Code review** campaigns and review checklists.
- **Quality gates** (coverage thresholds, lint/format gates, CI gates).
- **Hardening** passes (a11y audit, performance hardening, security review hand-off).

> **Q&A vs. feature-bound test work**: a test that covers **one** Feature/US is a `TNN.M.K` **inside that US** (parented to the Feature). Only **cross-cutting** quality work (global test strategy, a CI coverage gate, a project-wide a11y audit) lives here as `QA-NN`.

## Items in this bucket (each `QA-NN-*.md` → a child of the "Q&A" Epic)

| ID | Quality activity | Category | Status |
| --- | --- | --- | --- |
| `QA-01` | `<test plan / review / gate / hardening>` | test/review/gate | ⏳ Pending |

## Traceability

A `QA-NN` links **↑** to the **RNF** (quality attribute) and/or **Feature/Epic** it verifies, and **↓** to the **artifacts** it produces (feature files, suites, CI gates) and any **`BUG-NN`** it raises. This `README.md` is **not** exported as an item.

## Related ADRs

`<testing/quality tooling decisions, if any>`
