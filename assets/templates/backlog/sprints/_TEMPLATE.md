<!-- GENERIC TEMPLATE — copy to sprint-N-<slug>.md.
     PRINCIPLE: do NOT rewrite the Epic/Feature/US — REFERENCE the existing docs (traceability lives at the source).
     TWO status axes (one row carries both). The EMOJI is the stable token; the word is BILINGUAL — write it in the
     person's/team's language (EN or pt-BR):
       • Status        = sprint work progress + who:  ⏳ To do/A fazer · 🔨 Doing/Fazendo · ✅ Done/Feito · ⤳ Skipped/Adiado
       • Status Final  = GitHub-derived PR state (as in the project's root README):  ✅ Merged/Mergeada · 🔄 In review/Em revisão · 📭 PR open/PR aberta · — (no PR/sem PR)
     BLOCKS = one per person (the block title names WHO does it), mirroring the SIRA root-README roadmap.
     Anything dropped to a later sprint goes to the "Adiados (skipped)" section with a reason — and its Status becomes ⤳ Skipped. -->
# Sprint N — <meta curta>

> **Período**: DD/MM — DD/MM · **Meta**: <objetivo único da sprint>
> **Time**: <pessoas> · **Gate de cobertura**: <ex.: 40%>

## Referências (não reescrever — apenas linkar)

> O que entra nesta sprint **já está especificado** no backlog/requisitos. Aqui só **referenciamos** os documentos de origem — a rastreabilidade vive neles, não se copia o conteúdo do Epic/Feature/US para cá.

| Origem | Documento |
| --- | --- |
| Requisitos (RF/RNF) | [requirements/](../../requirements/) |
| Epic(s) em escopo | [EP-NN](../epics/EP-NN-....md) |
| Feature(s) em escopo | [F-NN](../features/F-NN-....md) · [F-NN](../features/F-NN-....md) |

## Legenda dos dois status (bilíngue — use a língua da pessoa/time)

> O **emoji é o token estável**; a palavra ao lado é **bilíngue** (EN / pt-BR) — escreva no idioma de quem preenche. Misturar idiomas entre blocos é OK (cada pessoa no seu).

- **Status** — progresso na sprint (e implícito *quem*, pelo bloco): **⏳ To do / A fazer** · **🔨 Doing / Fazendo** · **✅ Done / Feito** · **⤳ Skipped / Adiado** (ver [§ Adiados](#adiados-para-outra-sprint-skipped))
- **Status Final** — estado do PR no GitHub (como no README raiz do projeto): **✅ Merged / Mergeada** · **🔄 In review / Em revisão** · **📭 PR open / PR aberta** · **— (no PR / sem PR)**

## Blocos — quem faz o quê (espelha o README raiz do projeto)

> Um **bloco por pessoa**; o título do bloco diz **quem**. Cada linha **referencia** a US no documento da Feature (não reescreve a US). A coluna **PR** vem logo após **Status Final**.

### Bloco 1 — <tema do bloco> · *<Pessoa EN>*  <!-- exemplo: pessoa de língua inglesa -->

| US | Descrição | Status | Status Final | PR |
| --- | --- | --- | --- | --- |
| [US-NN.M](../features/F-NN-....md) | <ref curta — linka a US, não reescreve> | 🔨 Doing | — | — |
| [US-NN.M](../features/F-NN-....md) | <…> | ✅ Done | ✅ Merged | [#NNN](https://github.com/<org>/<repo>/pull/NNN) |

**Conclusão:** X / Y user stories concluídas.

### Bloco 2 — <tema do bloco> · *<Pessoa pt-BR>*  <!-- exemplo: pessoa de língua portuguesa -->

| US | Descrição | Status | Status Final | PR |
| --- | --- | --- | --- | --- |
| [US-NN.M](../features/F-NN-....md) | <…> | ⏳ A fazer | 🔄 Em revisão | [#NNN](https://github.com/<org>/<repo>/pull/NNN) |

**Conclusão:** X / Y user stories concluídas.

## Adiados para outra sprint (skipped)

> Toda US que **não couber** nesta sprint (falta de tempo, dependência, repriorização, qualquer motivo) fica aqui — com **motivo** e **destino**. No bloco acima, o **Status** dela passa a **⤳ Skipped**. Assim ninguém precisa caçar no histórico por que algo não entrou.

| US | Bloco / Responsável | Motivo do adiamento | Vai para |
| --- | --- | --- | --- |
| [US-NN.M](../features/F-NN-....md) | Bloco N · *<Pessoa>* | <falta de tempo / bloqueada por US-XX / repriorizada / …> | Sprint N+1 |

## Retrospectiva (preencher no fim da sprint)

- **Entregue**: <US com Status ✅ Done/Feito · Status Final ✅ Merged/Mergeada>
- **Adiado (skipped)**: <US + motivo — ver § Adiados>
- **Aprendizados**: <o que melhorar na próxima>
