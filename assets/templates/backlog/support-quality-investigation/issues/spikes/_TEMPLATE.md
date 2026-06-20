<!-- GENERIC TEMPLATE — copy to SPK-NN-<slug>.md. A Spike is a TIME-BOXED investigation that produces knowledge
     (an ADR/finding), never shipped code. OpenProject: child of the "Spikes" Epic (under "Issues"). -->
# SPK-NN — <question to answer>

> **Type**: Spike (time-boxed investigation)
> **Time-box**: <e.g. 2 days — hard limit>
> **Status**: ⏳ Pending | 🚧 Investigating | ✅ Concluded
> **Sprint**: N

---

## Question / hypothesis

<the open question that blocks an estimate or a decision. One falsifiable question.>

## Traceability ↑ (what triggered it)

| Triggered by | ID | Where |
| --- | --- | --- |
| User Story / Feature | `USNN.M` / `F-NN` | [F-NN](../../../features/F-NN-....md) |
| Decision / ADR | `ADR-NNN` | [ADR](../../../../planning/adrs/ADR-NNN-....md) |
| Origin issue | `ISS-NN` | [ISS-NN](../ISS-NN-....md) |

## Findings ↓ (the deliverable — knowledge, not code)

| Outcome | Reference |
| --- | --- |
| ADR produced | `ADR-NNN` (link) |
| Finding / recommendation | <one-paragraph conclusion> |
| Unblocks | `<the US estimate / decision it enables>` |

> **Spike DoD**: question answered **within the time-box** → an `ADR-NNN` or finding note written → the blocked `US`/decision can now proceed → `git mv` to [`../../../done/`](../../../done/).
