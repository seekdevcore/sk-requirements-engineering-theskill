# 12 — Interop SDD (OpenSpec · Spec Kit) — *espelho pt-BR pendente*

> ⚠️ **Sem tradução pt-BR completa ainda.** Referência adicionada na v1.9.0 (adaptador na v1.10.0); o snapshot
> pt-BR ainda não a espelha. A versão **autoritativa** (en-CA) está na raiz:
> [`../../../references/12-sdd-interop.md`](../../../references/12-sdd-interop.md).

**Resumo:** ponte **opcional** entre esta skill (camada de **qualidade** do requisito) e um framework de
execução SDD (**OpenSpec** — <https://github.com/Fission-AI/OpenSpec> · **GitHub Spec Kit** —
<https://github.com/github/spec-kit>). A fonte de verdade fica em `docs/requirements/`; o framework é uma
**projeção** gerada dela, preservando as tags `[RF-NN]`. Par **gerar ↔ verificar**:
`assets/project-to-sdd.sh <F-NN> --target openspec|speckit` gera a projeção; o validador MCP
`check_projection_drift` confirma que nada divergiu (missing / duplicated / orphan / ca_without_scenario /
ears_weakened; advisory, nunca bloqueia; EN + pt-BR).
