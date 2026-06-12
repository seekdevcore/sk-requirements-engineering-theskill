# Integrações — índice

> **Uma pasta, três lares.** Cada integração desta skill com uma ferramenta externa vive em **três lugares** por função (a taxonomia da skill é por função, não por feature). Este índice amarra os três para você achar todas as partes de qualquer integração de relance.
>
> - **Doc** (o *quê/porquê/como*) → aqui, `references/integrations/<nome>.md` — acessível pelo MCP como `requirements://reference/<nome>`.
> - **Adaptador** (o *executável*) → `../../../assets/integrations/<nome>.sh` (ou equivalente; o código é neutro de idioma e vive na raiz).
> - **Validador** (a *checagem consultiva*, quando aplicável) → o servidor MCP, `../../../mcp-server/`.

## Integrações disponíveis

| Integração | Doc | Adaptador | Validador |
|---|---|---|---|
| **SDD — OpenSpec · GitHub Spec Kit** (projeta a espinha `docs/` num loop de execução Spec-Driven Development, preservando as tags `[RF-NN]`) | [`sdd-interop.md`](sdd-interop.md) | [`../../../assets/integrations/project-to-sdd.sh`](../../../assets/integrations/project-to-sdd.sh) | `check_projection_drift` ([`../../../mcp-server/`](../../../mcp-server/README.md)) |
| **OpenProject — backlog ↔ work packages (round-trip via API REST)** (pull + push de Epics/Features/User Stories do `docs/backlog/` direto na API v3 do OpenProject; o `.xlsm` Excel é fallback Windows-only) | [`openproject.md`](openproject.md) | [`../../../assets/integrations/openproject-api.py`](../../../assets/integrations/openproject-api.py) (primário) · [`../../../assets/integrations/project-to-openproject.py`](../../../assets/integrations/project-to-openproject.py) (fallback Excel) | — (round-trip via o prefixo `<nosso-id>` no Subject) |

## Planejadas

| Integração | Status |
|---|---|
| *(nenhuma no momento)* | proponha uma pelos passos de "como adicionar" abaixo |

## Como adicionar uma nova integração

1. **Doc** → adicione `references/integrations/<nome>.md` (o crosswalk, a receita de projeção/sync, a regra de ida-e-volta). É auto-exposto pelo MCP como `requirements://reference/<nome>` (o servidor escaneia `references/` recursivamente, excluindo este `README.md`).
2. **Adaptador** → adicione `assets/integrations/<nome>.sh` (ou o script na linguagem certa) — dry-run por padrão, nunca sobrescreve, `set -Eeuo pipefail`.
3. **Validador** (opcional) → adicione um `@mcp.tool()` consultivo ao `mcp-server/` que nunca bloqueia, só reporta drift.
4. **Índice** → adicione uma linha na tabela acima.

> **A fonte da verdade fica em `docs/`.** Toda integração *projeta a partir* da espinha `docs/requirements/` + `docs/backlog/` para o formato da ferramenta externa — nunca o contrário. O identificador `[RF-NN]` é o que carrega a rastreabilidade através da fronteira; preserve-o.
