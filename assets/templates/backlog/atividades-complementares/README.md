<!-- MANDATORY STRUCTURAL BUCKET (a directory, not an EP-NN file) — seeded by the scaffolder; skips if it exists.
     This directory IS a backlog bucket, child of backlog/ (sibling of epics/, features/, sprints/).
     On OpenProject export it COLLAPSES into a ROOT Epic ("Atividades Complementares" /
     Complementary Activities), depth 0, sibling of the feature-front Epics. This README is the Epic's
     body/vision; each TX-NN-*.md file beside it is exported as a TASK child of that Epic. -->
# Atividades Complementares (*Complementary Activities*) — bucket de backlog

> **O que é**: diretório-bucket, **filho de `backlog/`** (irmão de `epics/`, `features/`, `sprints/`).
> **No OpenProject**: colapsa num **Epic na raiz** do backlog (depth 0), **irmão de "Aplicação Web"**.
> **Prioridade global**: 🟡 Normal.

---

## Visão de produto (vira a *descrição* do Epic no export)

Casa de todo trabalho **técnico, de configuração e de infraestrutura que NÃO está ligado diretamente a uma Feature ou User Story** e que, por isso (Regra 6 do `SKILL.md` / Rule 4 de [`05-convencoes-interpop.md`](../../../../references/05-convencoes-interpop.md)), é uma **Task transversal `TX-NN`** — **não uma Feature**. Exemplos: variáveis de ambiente, lint/format (ESLint/Prettier), CI/CD, `docker-compose`, criação das pastas iniciais, observabilidade (Sentry/Prometheus), arquivos de configuração.

> **Por que existe**: configuração técnica não é entregável ao cliente → não é Feature. Mas precisa de um lar **visível e rastreável** para o time técnico — e esse lar é aqui, como `TX-01`, `TX-02`, …
>
> **O que NÃO entra aqui**: tarefa técnica que **suporta uma US específica** — essa é `TNN.M.K` **dentro daquela US**, não `TX`.

## Itens deste bucket (cada `TX-NN-*.md` ao lado vira Task filha do Epic no export)

- Um arquivo `TX-NN-<slug>.md` por task transversal.
- Cada um é exportado como uma **Task** filha do Epic "Atividades Complementares" no OpenProject.
- Este `README.md` **não** é exportado como item — ele é a **descrição** do Epic.

## Tasks transversais (`TX-NN`)

| ID | Tarefa técnica | Status |
| --- | --- | --- |
| `TX-01` | `<configuração / infra / ferramental>` | ⏳ Pending |

## ADRs relacionadas

`<decisões de infra/ferramental, se houver>`
