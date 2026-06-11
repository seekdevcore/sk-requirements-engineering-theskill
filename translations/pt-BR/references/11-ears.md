# 11 — EARS (camada opcional de precisão) — *espelho pt-BR pendente*

> ⚠️ **Sem tradução pt-BR completa ainda.** Referência adicionada na v1.8.0; o snapshot pt-BR ainda não a
> espelha. A versão **autoritativa** (en-CA, já bilíngue EN+pt-BR no corpo) está na raiz:
> [`../../../references/11-ears.md`](../../../references/11-ears.md).

**Resumo:** EARS (*Easy Approach to Requirements Syntax*) é uma **camada OPCIONAL de precisão** que coexiste
com o `RF` em linguagem de negócio + BDD (não substitui). Cinco padrões, em pt-BR:
`O SISTEMA DEVE …` (ubíquo) · `QUANDO <gatilho> O SISTEMA DEVE …` · `ENQUANTO <estado> …` ·
`SE <condição> ENTÃO O SISTEMA DEVE …` · `ONDE <recurso> …`. Um `DEVE` por sentença → um grupo `CANN` → um ou
mais `Cenário`. EARS vive no **corpo** do RF / na CA, nunca no título de negócio. Validador MCP: `validate_ears`.
