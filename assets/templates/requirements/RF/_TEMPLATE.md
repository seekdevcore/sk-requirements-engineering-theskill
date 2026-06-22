<!-- GENERIC TEMPLATE — copy to RF-NNN-<modulo>.md and fill for one real module of the system. -->
# RF-NNN — <título de negócio, sem infinitivo, sem termo técnico>

> **Tipo**: Requisito Funcional
> **Prioridade**: 🔴 Imediato | 🟠 Alta | 🟡 Normal | 🟢 Baixa
> **Status**: 📝 Proposto | 🚧 Parcial | ✅ Realizado | 🗄️ Deprecated

---

## Enunciado de negócio (sem termo técnico)

> **<Uma frase: o sistema permite que [persona] [faça algo] [com qual valor/limite percebido]>.**

<!-- Completude 5W1H (ref03 §2.1.1) — o enunciado + o corpo deste RF devem deixar responder as SEIS:
     · Quem  → a persona               · O quê → a função/serviço (a frase acima)
     · Onde  → o módulo/tela           · Quando → o gatilho/prazo/frequência
     · Por quê → a ## Justificativa     · Como  → o fluxo/regra de NEGÓCIO (detalhado nos CA/BDD)
     "Como" é de NEGÓCIO (passo a passo do usuário), NUNCA o como técnico (endpoint/tabela → ADR/Task, regra 2). -->


## Justificativa (por que este requisito existe)

<dor real do usuário/negócio; impacto de produto; KPI alvo se houver>

## Realizado por (rastreabilidade ↓)

| Epic | Feature(s) | Status |
| --- | --- | --- |
| [EP-NN ...](../../backlog/epics/EP-NN-....md) | [F-NN ...](../../backlog/features/F-NN-....md) | ⏳ |

## Requisitos Não-Funcionais que limitam este RF

| RNF | Limite imposto |
| --- | --- |
| [RNF-perf](../RNF/RNF-perf.md) | <ex.: p95 ≤ 300ms> |

## Restrições e fora-de-escopo

- <o que NÃO está incluído>
