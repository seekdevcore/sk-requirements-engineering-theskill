<!-- GENERIC TEMPLATE — copy to ISS-NN-<slug>.md. An Issue is a RAW triage-inbox item. It is TRANSIENT: on triage
     it is reclassified and the resulting BUG/SPK/TX/Melhoria is created, then this file is moved (git mv) to
     ../done/ (or kept as the triage record linking down to what it became). OpenProject: child of the "Issues" Epic. -->
# ISS-NN — <raw report, as reported>

> **Type**: Issue (triage inbox)
> **Status**: 🆕 New | 🔍 Triaging | 🏷️ Classified | 📦 Closed
> **Reporter**: <name> · **Reported**: DD/MM/YYYY

---

## Raw report

<exactly what was observed/requested, in the reporter's words. Do NOT pre-classify here.>

## Triage

- **Verdict**: Bug | Spike | TX (support) | Melhoria | **Incident (→ PM in `docs/postmortems/`)** | Duplicate | Won't-fix
- **Rationale**: <one line on why>

## Outcome ↓ (what it became — keep the chain)

| Became | ID | Where |
| --- | --- | --- |
| `<Bug/Spike/TX/Melhoria>` | `<BUG-NN / SPK-NN / TX-NN / F-US>` | [target](../../bugs/) |

> **Triage = investigation.** A shallow triage classifies on the spot; a deeper, time-boxed investigation becomes a [`SPK-NN`](spikes/_TEMPLATE.md). Once classified, this `ISS-NN` is `git mv`-d to [`../../done/`](../../done/) (it stays as the audit record; the created item links **↑** back to this `ISS-NN`).
