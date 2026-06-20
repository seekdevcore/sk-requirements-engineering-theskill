<!-- STRUCTURAL BUCKET — seeded by the scaffolder; skips if it exists. en-CA folder: `bugs/`.
     UNLIKE the other buckets, bugs do NOT collapse into an Epic of their own. Each BUG-NN-*.md exports as a
     work-package of TYPE "Bug", PARENTED to the US/Feature it violates (it inherits that Feature's Epic). This
     README is documentation only — it is NOT exported as an Epic description. -->
# Bugs (*Defeitos*) — defect bucket (type, not Epic)

> **What it is**: a directory-bucket, **child of `backlog/`** (sibling of `epics/`, `features/`, `melhorias/`).
> **On OpenProject**: each item is a work-package of **type "Bug"** — **parented to the US/Feature it violates**, NOT grouped under a "Bugs" Epic. This keeps the defect one link away from the `CA` it breaks.
> **Priority is per-bug** (severity), not a single bucket priority.

---

## Why bugs are a *type*, not an Epic

A bug is a **defect against an existing acceptance criterion**. Its value as a backlog item is the **traceability** `BUG → CA → US → RF` — so it must live next to the requirement it violates, inheriting that Feature's Epic. Grouping all bugs under one "Bugs" Epic would sever that link. The OpenProject **"Bug" type** lets every defect be filtered together **without** detaching it from its Feature.

## Items in this bucket (each `BUG-NN-*.md` → a "Bug" work-package parented to the violated US/Feature)

| ID | Symptom | Severity | Layer | Violates | Status |
| --- | --- | --- | --- | --- | --- |
| `BUG-01` | `<short symptom>` | 🟠 High | Backend | `CANN` of `F-NN` | 🆕 Open |

## Traceability (the whole point)

Every `BUG-NN` links **↑** to the `CA`/`US`/`RF` it violates, **← origin** to the `ISS-NN` it was triaged from (if any), and **↓** to its fix (Task `[front]`/`[back]` · commit/PR · **regression test that failed before**). Closed bugs are `git mv`-d to [`../done/`](../done/).

## Related ADRs

`<if a fix carries a design decision, link the ADR>`
