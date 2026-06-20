<!-- GENERIC TEMPLATE — copy to QA-NN-<slug>.md. A QA item is CROSS-CUTTING quality work (tests, review, gate,
     hardening) not bound to one Feature. OpenProject: a child of the "Q&A" Epic. Feature-bound test work is a
     TNN.M.K inside the US instead. -->
# QA-NN — <quality activity>

> **Type**: Q&A (quality activity)
> **Category**: test design | test execution | code review | quality gate | hardening
> **Layer**: Frontend | Backend | Cross
> **Status**: ⏳ Pending | 🚧 In progress | ✅ Done
> **Sprint**: N

---

## Quality objective

<what quality bar this verifies, in one line. Quality includes testing.>

## Traceability ↑ (what it verifies)

| Verifies | ID | Where |
| --- | --- | --- |
| Non-functional req. | `RNF-<slug>` | [RNF](../../../requirements/RNF/RNF-....md) |
| Feature/Epic covered | `F-NN` / `EP-NN` | [F-NN](../../features/F-NN-....md) |

## Activity & artifacts ↓ (what it produces)

| Artifact | Reference |
| --- | --- |
| Test artifact | `<feature file / suite path>` |
| Quality gate | `<CI gate / coverage threshold>` |
| Defects raised | `<BUG-NN …>` (link each) |

> A `QA-NN` that finds a defect raises a [`BUG-NN`](../../bugs/_TEMPLATE.md) and links it under "Defects raised".
