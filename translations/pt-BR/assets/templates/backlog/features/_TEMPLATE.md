<!-- GENERIC TEMPLATE — copy to F-NN-<slug>.md. Feature has a paragraph description; BDD lives in the User Story.
     On OpenProject export, the sections below expand into their own typed work-packages, all under this Feature:
       · each CA → a "Critério de Aceitação" (child of the Feature; a grouping CA may nest CA→CA)
       · each US → a "User story" (child of the Feature; LINKS to the CAs it satisfies)
       · each Task → a "Task" child of its US, tagged [front]/[back] by layer.
     A defect against a CA is a separate BUG-NN (type "Bug") parented here — see ../bugs/. -->

# F-NN — <nome de negócio>

> **Tipo**: Feature
> **Epic pai**: [EP-NN ...](../epics/EP-NN-....md)
> **Sprint de execução**: [Sprint N](../sprints/sprint-N-....md)
> **Status**: 📝 Proposto | 🚧 Em andamento | ✅ Done
> **Prioridade**: 🔴 Imediato

---

## Descrição (visão de produto)

<parágrafo em linguagem de negócio. Feature NUNCA tem BDD — BDD vive na User Story.>

## Requisitos atendidos (rastreabilidade ↑)

| ID | Requisito | Relação |
| --- | --- | --- |
| [RF-NNN](../../requirements/RF/RF-NNN-....md) | <enunciado> | Realiza diretamente |

## Critérios de Aceitação (CAs)

| ID | Critério | Como verificar | Status |
| --- | --- | --- | --- |
| **CA01** | <estado verificável em booleano> | <teste> | ⏳ |

## User Stories

### US-NN.1 — <título curto>

> **Como** <persona>
> **Quero** <ação>
> **Para** <valor>.

- **Prioridade**: 🔴 · **Estimativa**: <SP> · **Sprint**: N · **Status**: ⏳
- **CAs cobertos**: CA01..CANN · **Persona**: [<persona>](../../requirements/personas-and-scenarios.md)

#### Cenários BDD (Gherkin)

```gherkin
Funcionalidade: <nome>
  Cenário: <caminho feliz>
    Dado que <contexto>
    Quando <ação>
    Então <resultado observável>
```

## Tasks (único nível com termo técnico)

> Prefixe a Task por camada — `[front]` / `[back]` / `[infra]` — como no OpenProject (vira a tag de camada).

| ID | Task | Camada | Commit | Status |
| --- | --- | --- | --- | --- |
| T-NN.1.1 | `[back]` <descrição técnica> | Backend | — | ⏳ |

## Defeitos conhecidos (rastreabilidade ↓)

| Bug | Viola | Status |
| --- | --- | --- |
| [BUG-NN](../bugs/BUG-NN-....md) | CANN | 🆕 Open |
