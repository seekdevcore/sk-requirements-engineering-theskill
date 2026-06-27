<!-- GENERIC TEMPLATE — copy to RNF-<slug>.md (perf, security, a11y, lgpd, availability, ...). Metrics MUST be quantitative. -->
# RNF-<slug> — <Performance | Security | Accessibility | Privacy | Availability | ...>

> **Type**: Non-Functional Requirement (cross-cutting)
> **Priority**: 🟠 High (release gate)
> **Status**: 📝 Proposed | 🚧 Partial | ✅ Verified

---

## Statement

<business sentence for the quality attribute>

### Mandatory metrics (ALWAYS quantitative)

| Metric | Target | When/how to measure |
| --- | --- | --- |
| <e.g. server response p95> | <e.g. ≤ 300ms at <scale>> | <e.g. load test> |

## Realized by (traceability ↓)

| Epic / Feature | How it meets the requirement |
| --- | --- |
| [EP-NN → F-NN](../../backlog/features/F-NN-....md) | <which ACs> |

## How to verify (CI gates)

| Gate | Status |
| --- | --- |
| <e.g. build fails if bundle > <limit>> | ⏳ |

## Constraints

- <baseline test hardware, target scale, etc.>
