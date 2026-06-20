<!-- CHILD-EPIC BUCKET — seeded by the scaffolder; skips if it exists. en-CA folder: `issues/`.
     On OpenProject export → child Epic "Issues" under the "Atividades de Apoio, Qualidade e Investigação" umbrella.
     Each ISS-NN-*.md beside this README exports as a child of the "Issues" Epic. issues/spikes/ → child Epic
     "Spikes" under "Issues". -->
# Issues — triage inbox (*Issues*) — child-Epic bucket

> **What it is**: child-bucket of [`../`](../) (the Support/Quality/Investigation umbrella).
> **On OpenProject**: child Epic **"Issues"** under the umbrella root Epic.
> **Global priority**: 🟡 Normal.

---

## Product vision (becomes the *description* of the "Issues" Epic on export)

The **triage inbox** — where anything raw enters before it is classified. An `ISS-NN` is **transient by design**: on triage it is reclassified into the right artifact and **moved** (`git mv`) to its real home. **To triage is to investigate** — analysing an incoming report *is* the investigation step; deeper, time-boxed investigations become a **Spike** ([`spikes/`](spikes/), the child Epic).

```
raw report  →  ISS-NN (inbox)  →  triage  →  BUG-NN (bugs/)        ← defect
                                          →  SPK-NN (issues/spikes/) ← needs investigation
                                          →  TX-NN  (../support/)    ← technical/config
                                          →  Melhoria (../../melhorias/) ← enhancement
                                          →  duplicate / won't-fix   ← closed with rationale
```

## Items in this bucket (each `ISS-NN-*.md` → a child of the "Issues" Epic)

| ID | Raw report | Triage verdict | Became | Status |
| --- | --- | --- | --- | --- |
| `ISS-01` | `<what was observed/requested>` | Bug/Spike/TX/Melhoria/dup | `<target id>` | 🆕 New |

## Traceability

An `ISS-NN` is the **origin** node: it links **↓** to whatever it became (`BUG-NN` / `SPK-NN` / `TX-NN` / Melhoria), so the chain *report → triage → work* is never lost. The reclassified item links back **↑** to its `ISS-NN`. This `README.md` is **not** exported as an item.

## Related ADRs

`<triage-policy decisions, if any>`
