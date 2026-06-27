<!-- MANDATORY STRUCTURAL BUCKET (a directory, not an EP-NN file) — seeded by the scaffolder; skips if it exists.
     This directory IS a backlog bucket, child of backlog/ (sibling of epics/, features/, sprints/).
     On OpenProject export it COLLAPSES into a ROOT Epic ("Melhorias" / Improvements), depth 0,
     sibling of the feature-front Epics (e.g. "Aplicação Web"). This README is the Epic's body/vision;
     each *.md file beside it is exported as a CHILD of that Epic. -->
# Melhorias (*Improvements*) — backlog bucket

> **What it is**: a bucket directory, **child of `backlog/`** (sibling of `epics/`, `features/`, `sprints/`).
> **In OpenProject**: collapses into a **root Epic** of the backlog (depth 0), **sibling of "Aplicação Web"**.
> **Global priority**: 🟢 Low (unless a specific improvement is bumped up in priority).

---

## Product vision (becomes the Epic's *description* on export)

Home of **product improvements** — refinements, optimizations and small enhancements to things that **already exist** and that are **not a new capability**. This includes: usability tweaks, perceived performance, visual polish, copy/accessibility improvements, and evolution ideas that emerge from real use and have not yet become a formal requirement.

> **Improvement vs. new Feature**: if it delivers a **new capability** to the customer → it is a **Feature** (under the right domain Epic). If it **improves something that already exists** without being a new capability → it is an **Improvement**, and lives here.

## Items in this bucket (each `*.md` beside it becomes a child of the Epic on export)

- One `.md` file per improvement (e.g. `F-NN-<slug>.md` or `US-<slug>.md`).
- Each file is exported as a **child** of the "Melhorias" Epic in OpenProject (Feature/User story according to the ID).
- This `README.md` is **not** exported as an item — it is the **description** of the Epic.

## Traceability

| ID | Improvement | Type | Source |
| --- | --- | --- | --- |
| `<F/US>` | `<improvement description>` | Feature/US | real use / feedback |

## Related ADRs

`<if an improvement carries a design decision, link the ADR>`
