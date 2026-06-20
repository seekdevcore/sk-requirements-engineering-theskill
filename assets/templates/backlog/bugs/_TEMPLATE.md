<!-- GENERIC TEMPLATE — copy to BUG-NN-<slug>.md. A Bug is a DEFECT against an existing CA/US.
     OpenProject: work-package of TYPE "Bug", PARENTED to the US/Feature it violates (inherits that Feature's
     Epic). Never invents an Epic of its own. -->
# BUG-NN — <short symptom in business language>

> **Type**: Bug (defect)
> **Severity**: 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
> **Layer**: Frontend | Backend | Infra | Fullstack   (drives the `[front]`/`[back]` tag on the fix Task)
> **Status**: 🆕 Open | 🚧 Fixing | 🩹 Fixed | ✅ Verified | 📦 Closed
> **Sprint**: N · **Reported**: DD/MM/YYYY

---

## Defect (observed × expected)

- **Observed**: <what goes wrong>
- **Expected**: <the correct behaviour per the violated CA>

## Steps to reproduce

1. <step>
2. <step>
3. <faulty result>

## Traceability ↑ (what this defect VIOLATES)

| Violates | ID | Where |
| --- | --- | --- |
| Acceptance Criterion | `CANN` | [F-NN](../features/F-NN-....md) |
| User Story | `USNN.M` | [F-NN](../features/F-NN-....md) |
| Source requirement | `RF-NNN` | [RF-NNN](../../requirements/RF/RF-NNN-....md) |

## Origin ← (where it came from)

- Triaged from: [`ISS-NN`](../support-quality-investigation/issues/ISS-NN-....md) *(if it came from triage; else: direct report)*.

## Resolution ↓ (traceability of the fix)

| Artifact | Reference |
| --- | --- |
| Fix Task | `T-NN.M.K` · `[front]`/`[back]` |
| Commit / PR | `<sha>` / `#PR` |
| Regression test | [`<feature>.feature` / suite](../../tests/...) — **fails before, green after** |

> **Bug DoD**: reproduce → fix → **regression test that was red is now green** → update the violated `CA` status → `git mv BUG-NN-*.md ../done/`.
