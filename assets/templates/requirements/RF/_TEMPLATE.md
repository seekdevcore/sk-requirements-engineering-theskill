<!-- GENERIC TEMPLATE — copy to RF-NNN-<module>.md and fill for one real module of the system. -->
# RF-NNN — <business title, no infinitive verb, no technical term>

> **Type**: Functional Requirement
> **Priority**: 🔴 Immediate | 🟠 High | 🟡 Normal | 🟢 Low
> **Status**: 📝 Proposed | 🚧 Partial | ✅ Done | 🗄️ Deprecated

---

## Business statement (no technical term)

> **<One sentence: the system lets [persona] [do something] [with what perceived value/limit]>.**

<!-- 5W1H completeness (ref03 §2.1.1) — the statement + the body of this RF must let you answer all SIX:
     · Who  → the persona              · What → the function/service (the sentence above)
     · Where → the module/screen       · When → the trigger/deadline/frequency
     · Why  → the ## Rationale          · How  → the BUSINESS flow/rule (detailed in the AC/BDD)
     "How" is BUSINESS (the user's step-by-step), NEVER the technical how (endpoint/table → ADR/Task, rule 2). -->

## Rationale (why this requirement exists)

<real user/business pain; product impact; target KPI if any>

## Realized by (traceability ↓)

| Epic | Feature(s) | Status |
| --- | --- | --- |
| [EP-NN ...](../../backlog/epics/EP-NN-....md) | [F-NN ...](../../backlog/features/F-NN-....md) | ⏳ |

## Non-Functional Requirements that constrain this RF

| RNF | Imposed limit |
| --- | --- |
| [RNF-perf](../RNF/RNF-perf.md) | <e.g. p95 ≤ 300ms> |

## Constraints and out-of-scope

- <what is NOT included>
