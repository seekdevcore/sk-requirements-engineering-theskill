<!-- GENERIC TEMPLATE — adapt to your project. See references/10-estrutura-projeto.md §"Adaptation protocol". -->
# Backlog — <NOME DO PROJETO>

> **Pasta-fonte do "QUEM faz O QUÊ, QUANDO".** O **porquê** vive em `../requirements/`. O **como** em `../specs/` + ADRs.
>
> Last requirements-document check: DD/MM/AAAA — no changes
> (atualize toda vez que conferir os requisitos antes de mexer no backlog — SKILL §2.1)

## Estrutura

```
backlog/
├── README.md                  este arquivo
├── glossary.md               vocabulário de domínio (toda US/CA/ADR deve usar estes termos)
├── epics/                     EP-NN-<slug>.md  — Aplicação→Módulo→Componente (MÁX. 3 níveis de Epic) → Features
├── features/                  F-NN-<slug>.md   — descrição + CAs + USs (com BDD) + Tasks
├── improvements/                 ← bucket OBRIGATÓRIO → Epic-raiz "Melhorias" (Improvements) no export
│   ├── README.md              o que é + descrição do Epic
│   └── <F/US>-<slug>.md        cada melhoria do produto (vira filho do Epic)
├── bugs/                      ← bucket de DEFEITOS → type "Bug" parented à US/Feature violada (NÃO é Epic)
│   ├── README.md              por que bug é type, não Epic
│   └── BUG-NN-<slug>.md        cada defeito (linka ao CA que viola)
├── support-quality-investigation/  ← bucket UMBRELLA → Epic-raiz "Atividades de Apoio, Qualidade e Investigação"
│   ├── README.md              descrição do Epic umbrella + 3 Epics filhos
│   ├── support/               → Epic-filho "Apoio"  — TX-NN (técnico/config/infra; era atividades-complementares)
│   ├── qa/                    → Epic-filho "Q&A"    — QA-NN (testes · reviews · gates)
│   └── issues/                → Epic-filho "Issues" — ISS-NN (triagem)
│       └── spikes/            → Epic-filho "Spikes" — SPK-NN (investigação time-boxed)
├── sprints/                   sprint-N-<slug>.md — execução temporal (mapping US/Task)
└── done/                      itens fechados (MOVIDOS via git mv: Feature/Bug/QA/ISS/SPK)
```

> **Regra de profundidade — MÁX. 3 níveis de Epic.** O front (`Aplicação Web`/`Mobile`) é o Epic raiz (nível 1); abaixo dele vem o **Módulo** (nível 2) e o **Componente** (nível 3) — e então a **Feature**. Depois do Epic-módulo há **só mais um** Epic (o componente) antes da Feature. Não aninhe um 4º nível de Epic (ex.: `Aplicação › Módulo › Gestão de X › Consulta de X › Feature` está fundo demais — colapse para `Aplicação › Módulo › Componente › Feature`).
>
> **Nomes en-CA, Epics pt-BR.** As pastas seguem o padrão en-CA (`support/`, `qa/`, `issues/`, `spikes/`) como `epics/`/`features/`; o adapter (`_BUCKETS`) restaura o nome pt-BR do Epic no export ("Apoio", "Q&A", "Issues", "Spikes", "Atividades de Apoio, Qualidade e Investigação").
>
> **Buckets estruturais** (diretórios, não arquivos `EP-NN`): **`improvements/`** = aprimoramentos do que já existe (→ Epic-raiz). **`support-quality-investigation/`** = umbrella transversal (→ Epic-raiz com 3 Epics filhos). **`bugs/`** é diferente: cada `BUG-NN` é um work-package **type "Bug" parented à US/Feature que viola** (herda o Epic dela), **não** um Epic próprio — assim o defeito fica a um link do `CA`. Regra-mãe: *o type diz o que é; o parent diz a quem serve.*

## Naming (regra dura)

| Nível | Pode no título | NÃO pode no título |
| --- | --- | --- |
| Epic | Substantivo + adjetivo | Infinitivo, termo técnico |
| Feature | Substantivo + adjetivo | Infinitivo, sigla técnica |
| CA | Estado verificável | Vago ("Performance OK") |
| US | "Como [persona], quero [ação], para [valor]" | Mistura técnico-negócio |
| Task | **PODE** termo técnico | (único nível onde técnico é OK) |

## IDs canônicos (imutáveis após criação)

| Tipo | Formato | Exemplo |
| --- | --- | --- |
| Epic | `EP-NN` | `EP-10` |
| Feature | `F-NN` | `F-30` |
| Critério de Aceitação | `CANN` (no Feature pai) | `CA01` |
| User Story | `USNN.M` | `US30.1` |
| Task US-bound | `TNN.M.K` | `T30.1.4b` |
| Task transversal (Apoio) | `TX-NN` | `TX-18` |
| Defeito (Bug) | `BUG-NN` | `BUG-04` |
| Atividade de qualidade (Q&A) | `QA-NN` | `QA-07` |
| Issue de triagem | `ISS-NN` | `ISS-12` |
| Spike (investigação) | `SPK-NN` | `SPK-02` |
| Sprint | `sprint-N-slug` | `sprint-4-<slug>` |

## Prioridade

🔴 Imediato (bloqueia MVP/security) · 🟠 Alta (release atual) · 🟡 Normal (próxima sprint) · 🟢 Baixa.

## Definition of Done de Feature

1. Todos os CAs verificados por teste (ou checklist manual se UX puro).
2. Toda US tem BDD que roda verde.
3. Toda Task `done` com commit hash.
4. Code-review aprovado.
5. Cobertura ≥ gate do Sprint.
6. Documentação cruzada atualizada (RF/RNF citados; Sprint cita Feature; Feature em `done/`).
7. Mergeada via PR (sem `--force-push`, sem `--no-verify`).

## Como fechar uma Feature

1. Confirmar CAs/USs/Tasks `✅ Done`.
2. Atualizar commit hashes no `features/F-NN-*.md`.
3. Atualizar Epic pai.
4. Atualizar Sprint.
5. Atualizar `requirements/RF-*` (`## Realizado por`).
6. `git mv features/F-NN-*.md done/`.
7. Commit `chore(backlog): F-NN done — close + archive`.

## Cross-references

- [Requisitos](../requirements/README.md) · [Specs](../specs/) · [ADRs do projeto](../planning/adrs/)
