<!-- GENERIC TEMPLATE — copy to F-NN-<slug>.md. Feature has a paragraph description; BDD lives in the User Story.
     On OpenProject export, the sections below expand into their own typed work-packages, all under this Feature:
       · each CA → a "Critério de Aceitação" (child of the Feature; a grouping CA may nest CA→CA)
       · each US → a "User story" (child of the Feature; LINKS to the CAs it satisfies)
       · each Task → a "Task" child of its US, tagged [front]/[back] by layer.
     A defect against a CA is a separate BUG-NN (type "Bug") parented here — see ../bugs/. -->

# F-NN — <business name>

> **Type**: Feature
> **Parent Epic**: [EP-NN ...](../epics/EP-NN-....md)
> **Execution sprint**: [Sprint N](../sprints/sprint-N-....md)
> **Status**: 📝 Proposed | 🚧 In progress | ✅ Done
> **Priority**: 🔴 Immediate

---

## Description (product vision)

<paragraph in business language. A Feature NEVER has BDD — BDD lives in the User Story.>

## Requirements met (traceability ↑)

| ID | Requirement | Relation |
| --- | --- | --- |
| [RF-NNN](../../requirements/RF/RF-NNN-....md) | <statement> | Directly realizes |

## Acceptance Criteria (CAs)

| ID | Criterion | How to verify | Status |
| --- | --- | --- | --- |
| **CA01** | <verifiable boolean state> | <test> | ⏳ |

## User Stories

### US-NN.1 — <short title>

> **As a** <persona>
> **I want** <action>
> **So that** <value>.

- **Priority**: 🔴 · **Estimate**: <SP> · **Sprint**: N · **Status**: ⏳
- **CAs covered**: CA01..CANN · **Persona**: [<persona>](../../requirements/personas-and-scenarios.md)

#### BDD scenarios (Gherkin)

```gherkin
Feature: <name>
  Scenario: <happy path>
    Given <context>
    When <action>
    Then <observable result>
```

## Tasks (the only level with technical terms)

> Prefix the Task by layer — `[front]` / `[back]` / `[infra]` — as in OpenProject (becomes the layer tag).

| ID | Task | Layer | Commit | Status |
| --- | --- | --- | --- | --- |
| T-NN.1.1 | `[back]` <technical description> | Backend | — | ⏳ |

## Known defects (traceability ↓)

| Bug | Violates | Status |
| --- | --- | --- |
| [BUG-NN](../bugs/BUG-NN-....md) | CANN | 🆕 Open |
