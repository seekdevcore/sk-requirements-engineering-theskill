<!-- MANDATORY STRUCTURAL BUCKET (a directory, not an EP-NN file) — seeded by the scaffolder; skips if it exists.
     This directory IS a backlog bucket, child of backlog/ (sibling of epics/, features/, sprints/).
     On OpenProject export it COLLAPSES into a ROOT Epic ("Melhorias" / Improvements), depth 0,
     sibling of the feature-front Epics (e.g. "Aplicação Web"). This README is the Epic's body/vision;
     each *.md file beside it is exported as a CHILD of that Epic. -->
# Melhorias (*Improvements*) — bucket de backlog

> **O que é**: diretório-bucket, **filho de `backlog/`** (irmão de `epics/`, `features/`, `sprints/`).
> **No OpenProject**: colapsa num **Epic na raiz** do backlog (depth 0), **irmão de "Aplicação Web"**.
> **Prioridade global**: 🟢 Baixa (a menos que uma melhoria específica suba de prioridade).

---

## Visão de produto (vira a *descrição* do Epic no export)

Casa das **melhorias do produto** — refinamentos, otimizações e pequenos aprimoramentos de coisas **que já existem** e que **não são uma capacidade nova**. Aqui entram: ajustes de usabilidade, performance percebida, polimento visual, melhorias de texto/acessibilidade, e ideias de evolução que surgem do uso real e ainda não viraram requisito formal.

> **Melhoria vs. Feature nova**: se entrega uma **capacidade nova** ao cliente → é **Feature** (sob o Epic de domínio certo). Se **melhora algo que já existe** sem ser capacidade nova → é **Melhoria**, e mora aqui.

## Itens deste bucket (cada `*.md` ao lado vira filho do Epic no export)

- Um arquivo `.md` por melhoria (ex.: `F-NN-<slug>.md` ou `US-<slug>.md`).
- Cada arquivo é exportado como **filho** do Epic "Melhorias" no OpenProject (Feature/User story conforme o ID).
- Este `README.md` **não** é exportado como item — ele é a **descrição** do Epic.

## Rastreabilidade

| ID | Melhoria | Tipo | Origem |
| --- | --- | --- | --- |
| `<F/US>` | `<descrição da melhoria>` | Feature/US | uso real / feedback |

## ADRs relacionadas

`<se uma melhoria carregar uma decisão de design, linke a ADR>`
