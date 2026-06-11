# 10 — Estrutura de projeto on-disk — *espelho pt-BR pendente*

> ⚠️ **Sem tradução pt-BR completa ainda.** Referência adicionada após a v1.0.x; o snapshot pt-BR ainda não a
> espelha. A versão **autoritativa** (en-CA) está na raiz do repositório:
> [`../../../references/10-estrutura-projeto.md`](../../../references/10-estrutura-projeto.md).

**Resumo (use a versão en-CA para o detalhe):** a estrutura física sob um único `docs/` —
`docs/requirements/` (o *porquê/o quê*) + `docs/backlog/` (o *quem/o quê/quando*) + ADRs em dois tiers
(`planning/adrs/` + `specs/<feature>/adrs/`, numeração global) — materializa a espinha de rastreabilidade. O
scaffolder `assets/scaffold-structure.sh` roda **detect → create → reorganize** e classifica o alvo em
**GREENFIELD / HAS-STRUCTURE / LOOSE-FILES / LEGACY-MONOLITH** (§8.1 = migração de monolito legado). É a base
do **§0 first-run obrigatório** do `SKILL.md` en-CA.
