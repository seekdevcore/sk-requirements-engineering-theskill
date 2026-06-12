<!-- MANDATORY ROOT EPIC — seeded by the scaffolder (skips if it already exists).
     The home for cross-cutting TX. Rename the ID to your project's EP-NN scheme if needed. -->
# EP — Atividades Complementares (*Complementary Activities*)

> **Tipo**: Epic (root, **obrigatório**) · **Status**: 🚧 Em andamento (contínuo)
> **Prioridade global**: 🟡 Normal
> **Papel**: front-irmão dos Epics de funcionalidade (não tem Epic-pai)

---

## Visão de produto

Casa de todo trabalho **técnico, de configuração e de infraestrutura que NÃO está ligado diretamente a uma Feature ou User Story** e que, por isso (Regra 4 de [`05-convencoes-interpop.md`](../../../references/05-convencoes-interpop.md)), é uma **Cross-cutting Task `TX-NN`** — **não uma Feature**. Exemplos: variáveis de ambiente, lint/format (ESLint/Prettier), CI/CD, `docker-compose`, criação das pastas iniciais, observabilidade (Sentry/Prometheus), arquivos de configuração.

> **Por que existe**: configuração técnica não é entregável ao cliente → não é Feature. Mas precisa de um lar **visível e rastreável** para o time técnico — e esse lar é aqui, como `TX-01`, `TX-02`, …
>
> **O que NÃO entra aqui**: tarefa técnica que **suporta uma US específica** — essa é `TNN.M.K` **dentro daquela US**, não `TX`.

## Tasks transversais sob este Epic (`TX-NN`)

| ID | Tarefa técnica | Status |
| --- | --- | --- |
| `TX-01` | `<configuração / infra / ferramental>` | ⏳ Pending |

## ADRs relacionadas

`<decisões de infra/ferramental, se houver>`
