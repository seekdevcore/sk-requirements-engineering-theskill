<!-- CHILD-EPIC BUCKET — seeded by the scaffolder; skips if it exists. en-CA folder: `issues/spikes/`.
     On OpenProject export → child Epic "Spikes" UNDER the "Issues" child Epic (which is under the umbrella).
     Each SPK-NN-*.md beside this README exports as a child of the "Spikes" Epic. -->
# Spikes (*Spikes*) — child-Epic bucket (under Issues)

> **What it is**: child-bucket of [`../`](../) (Issues), grandchild of the umbrella.
> **On OpenProject**: child Epic **"Spikes"** under the **"Issues"** Epic.
> **Global priority**: 🟡 Normal · **always time-boxed**.

---

## Product vision (becomes the *description* of the "Spikes" Epic on export)

Home of **time-boxed investigations** — a `SPK-NN` answers a *question* ("which index strategy holds p95 ≤ 300 ms?", "is library X viable?") **before** a US can be estimated or a design decided. A Spike produces **knowledge, not a feature**: its deliverable is an **ADR**, a finding note, or an estimate — never shipped code.

> **Spike vs. Bug**: a Spike investigates an **open question**; a Bug fixes a **known defect**. A spike that uncovers a defect raises a `BUG-NN`.

## Items in this bucket (each `SPK-NN-*.md` → a child of the "Spikes" Epic)

| ID | Question to answer | Time-box | Outcome | Status |
| --- | --- | --- | --- | --- |
| `SPK-01` | `<the question>` | `<e.g. 2 days>` | ADR/finding | ⏳ Pending |

## Traceability

A `SPK-NN` links **↑** to what triggered it (the `USNN.M` / `F-NN` / decision / `ISS-NN` that needs the answer) and **↓** to its result (the `ADR-NNN` it produces, or the estimate/decision it unblocks). This `README.md` is **not** exported as an item.

## Related ADRs

`<the ADR(s) this spike produced → ../../../../planning/adrs/ or ../../../../specs/<feature>/adrs/>`
