# Requirements Engineering — Claude Code Skill

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Skill: engenharia-de-requisitos](https://img.shields.io/badge/Skill-engenharia--de--requisitos-blue)](./SKILL.md)
[![Language: en-CA default](https://img.shields.io/badge/Language-en--CA%20(default)-success)](#language-status)
[![Translation: pt-BR available](https://img.shields.io/badge/Translation-pt--BR%20available-yellow)](#language-status)
[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational)](./CHANGELOG.md)

> **Skill for [Claude Code](https://claude.com/claude-code)** that loads canonical knowledge of **Requirements Engineering**, **Business Analysis**, and **Professional Ethics in Computing** into any Claude session — built from the full course material of IFPB (Instituto Federal da Paraíba) plus the canonical bibliography of the field (Sommerville, Pressman, Wiegers, Cohn, Robertson, Hull, Falbo, BABOK v3, SBC 002/2024).

---

## ⚡ Language status

| Language | Status | Current content |
|---|---|---|
| **en-CA** (default declared in frontmatter) | 🟡 Roadmap | Frontmatter and skill triggers exist in English; **full content translation is on the roadmap** |
| **pt-BR** | 🟢 Available | **All content is currently written in Brazilian Portuguese** (the original source — IFPB course taught in Portuguese) |

> If you are an English-speaking user: the skill **will activate** on English triggers (`requirements elicitation`, `acceptance criteria`, `BDD`, etc.), but the content delivered (references, examples, templates) is in **Portuguese**. Claude can translate inline if you ask, but the source files in this repo are pt-BR for now. **Pull requests welcome for en-CA translation.**

---

## 📦 Installation

### Option 1 — Clone directly into your global skills folder (recommended)

```bash
# 1. Clone the repo into Claude Code's global skills directory
cd ~/.claude/skills/
git clone git@github.com:seekdevcore/sk-requirements-engineering-skill.git engenharia-de-requisitos

# 2. Verify the skill loads
ls ~/.claude/skills/engenharia-de-requisitos/SKILL.md

# 3. Open a new Claude Code session and invoke
# (the skill auto-discovers on session start)
```

### Option 2 — Clone elsewhere and symlink

```bash
# 1. Clone wherever you keep your repos
git clone git@github.com:seekdevcore/sk-requirements-engineering-skill.git ~/repos/sk-requirements-engineering-skill

# 2. Create a symlink into Claude's skills folder
ln -s ~/repos/sk-requirements-engineering-skill ~/.claude/skills/engenharia-de-requisitos

# 3. Verify
readlink ~/.claude/skills/engenharia-de-requisitos
```

### Option 3 — HTTPS clone (if you don't have SSH keys configured)

```bash
git clone https://github.com/seekdevcore/sk-requirements-engineering-skill.git ~/.claude/skills/engenharia-de-requisitos
```

### Verifying installation

In a new Claude Code session, type:

```
List the skills I have installed.
```

You should see `engenharia-de-requisitos` in the list. Then invoke it explicitly:

```
> Skill: engenharia-de-requisitos
```

---

## 🎯 When to invoke this skill

Invoke when you (or Claude on your behalf) are doing:

- **Requirements discovery** — interviews, surveys, brainstorming, ethnography, document analysis, stories and scenarios
- **Specification** — building a hierarchical backlog (Epic → Feature [+ description + ACs] → User Story [+ BDD] → Task)
- **User Stories with BDD** — writing `Given / When / Then` that bridges requirement and executable test
- **Acceptance Criteria** — declarative testable rules per feature (with the `[...]` convention for sub-rules)
- **Estimation** — Story Points + Planning Poker (Fibonacci scale)
- **Validation** — Sommerville's 5 checks + Falbo's 7 dimensions + lo-fi/hi-fi prototypes
- **Change management + traceability** — keeping docs ↔ code ↔ test aligned
- **Business analysis** — BABOK v3, BPMN, AS-IS / TO-BE, MoSCoW, RICE
- **Professional ethics** — SBC 002/2024 Code applied to privacy, ML/AI, inclusion, system decommissioning

**Do not invoke for pure code implementation.** Requirements Engineering covers the stage **before** (discovering what to build) and **after** (validating that what was built is correct) — not the middle.

---

## 🗂 Repository structure

```
engenharia-de-requisitos/
├── SKILL.md                       ← entry point + usage protocol (map)
├── README.md                      ← this file
├── LICENSE                        ← CC BY-SA 4.0
├── CHANGELOG.md                   ← version history
├── references/                    ← canonical detail (loaded on demand)
│   ├── 01-fundamentos.md          (FR vs NFR, stakeholders, feasibility, spiral, MVP+A/B)
│   ├── 02-elicitacao.md           (6 techniques, 5W, scales, brainstorming)
│   ├── 03-especificacao.md        (Backlog, Epic→Feature→US→AC, INVEST, multiple root Epics)
│   ├── 04-bdd-criterios-aceitacao.md  (BDD pt-BR, Three Amigos, AC vs Gherkin, [...] convention)
│   ├── 05-estimativa.md           (Story Points, Planning Poker, velocity)
│   ├── 05-convencoes-interpop.md  (10 hard rules: source-of-truth document, naming, [...], etc.)
│   ├── 06-validacao.md            (5 checks + 7 dimensions + prototypes)
│   ├── 07-mudanca-rastreabilidade.md  (change management, RTM, enduring vs volatile requirements)
│   ├── 08-analista-negocios.md    (BABOK, AS-IS/TO-BE, MoSCoW, RICE, Kano)
│   └── 09-etica-sbc.md            (SBC 002/2024 Code applied to RE)
└── examples/
    ├── caso-controle-dopagem.md         (real CNPq case — ABCD/COB)
    ├── caso-interpop-moderacao.md       (Interpop project case — ban hierarchy)
    ├── template-backlog-openproject.md  (full worked backlog template)
    ├── template-documento-requisitos.md (IEEE 830 / Wiegers / Sommerville template)
    └── template-user-story.feature      (Gherkin pt-BR ready-to-copy)
```

**Usage pattern**: `SKILL.md` is a 10-section map with links to detail. You read `SKILL.md` to locate the answer; you read a `reference` only when you need full detail on that topic.

---

## 📚 Sources (corpus that fed the skill)

Built from the complete course material of **ERS — Requirements Engineering** at **IFPB Campus João Pessoa** (Prof. Juliana Dantas Ribeiro Viana de Medeiros), complemented by the canonical bibliography:

- **Sommerville, I.** *Software Engineering*, 10th ed. Pearson 2019 (Ch. 4 read integrally)
- **Pressman, R.** *Software Engineering: A Practitioner's Approach*, 9th ed. McGraw-Hill 2021
- **Wiegers, K. & Beatty, J.** *Software Requirements*, 3rd ed. Microsoft Press
- **Cohn, M.** *User Stories Applied*, 2004
- **Robertson, S. & Robertson, J.** *Mastering the Requirements Process* (VOLERE method)
- **Hull, E., Jackson, K., Dick, J.** *Requirements Engineering*, 4th ed. Springer
- **Falbo, R. A.** Lecture notes — UFES
- **IIBA.** *BABOK Guide* v3
- **SBC.** Resolution 002/2024 — Code of Ethics and Professional Conduct
- **Valente, M. T.** *Engenharia de Software Moderna* (engsoftmoderna.info, MVP + A/B testing)

IFPB lectures processed (in order):

- LECTURE 0 — Course presentation
- LECTURE 01 — Introduction to RE (real cases: $500M Citibank, Boeing 737 MAX, INSS, IPTU SP)
- LECTURE 02 — RE process + FR vs NFR
- LECTURE 03 — Real CNPq Doping Control case (full execution)
- LECTURE 04 — Elicitation via Interviews
- LECTURE 05 — Elicitation via Questionnaire + Brainstorming
- LECTURE 06 — Elicitation via Ethnography + Document Analysis
- LECTURE 07 — Specification: Initial backlog (OpenProject)
- LECTURE 08 — Specification: Acceptance Criteria
- LECTURE 09 — Specification: User Stories (BDD integrated)
- LECTURE 09.2 — Sizing estimation with User Story Points (Planning Poker)
- LECTURE 10 — Validation through interface prototypes

---

## 🤝 Contributing

Pull requests welcome — especially for:

1. **en-CA translation** of the `references/` and `examples/` content
2. Additional real-world examples (case studies)
3. New `.feature` templates
4. Tooling integration scaffolds (Linear, Jira, Notion, GitHub Issues)

When contributing, follow the same conventions documented in `references/05-convencoes-interpop.md` (10 hard rules: source-of-truth document, naming without infinitives, no technical terms in non-Task artifacts, grouped ACs with `[...]` convention, etc.).

---

## 📄 License

This skill content is licensed under **[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)**.

You are free to:
- **Share** — copy and redistribute in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — give appropriate credit and indicate if changes were made
- **ShareAlike** — distribute your contributions under the same license

See [`LICENSE`](./LICENSE) for the full legal code.

---

## 🏷 Maintainer

Published by [**Seekdev**](https://github.com/seekdevcore) (`seekdevcore` on GitHub).

Original author and curator: **Gabriel Marques** ([@GabeMarques-Intetsu](https://github.com/GabeMarques-Intetsu)).

---

---

# 🇧🇷 Versão em Português (pt-BR)

> **Skill para o [Claude Code](https://claude.com/claude-code)** que carrega conhecimento canônico de **Engenharia de Requisitos**, **Análise de Negócios** e **Ética Profissional em Computação** em qualquer sessão Claude — construída a partir do material didático completo do curso ERS do IFPB Campus João Pessoa, mais a bibliografia canônica da área (Sommerville, Pressman, Wiegers, Cohn, Robertson, Hull, Falbo, BABOK v3, SBC 002/2024).

## ⚡ Estado dos idiomas

| Idioma | Estado | Conteúdo atual |
|---|---|---|
| **en-CA** (padrão declarado no frontmatter) | 🟡 No roadmap | Frontmatter e gatilhos em inglês existem; **tradução do conteúdo completo está no roadmap** |
| **pt-BR** | 🟢 Disponível | **Todo o conteúdo atual está escrito em português brasileiro** (fonte original — curso IFPB ministrado em português) |

## 📦 Instalação

### Opção 1 — Clonar direto na pasta global de skills (recomendado)

```bash
cd ~/.claude/skills/
git clone git@github.com:seekdevcore/sk-requirements-engineering-skill.git engenharia-de-requisitos
ls ~/.claude/skills/engenharia-de-requisitos/SKILL.md
```

### Opção 2 — Clonar em outro lugar + symlink

```bash
git clone git@github.com:seekdevcore/sk-requirements-engineering-skill.git ~/repos/sk-requirements-engineering-skill
ln -s ~/repos/sk-requirements-engineering-skill ~/.claude/skills/engenharia-de-requisitos
```

### Opção 3 — Clone HTTPS

```bash
git clone https://github.com/seekdevcore/sk-requirements-engineering-skill.git ~/.claude/skills/engenharia-de-requisitos
```

Em uma nova sessão do Claude Code, invoque com:

```
> Skill: engenharia-de-requisitos
```

## 🎯 Quando invocar

Invoque quando você (ou seu Claude) estiver fazendo:

- **Descoberta de requisitos** — entrevistas, questionários, brainstorming, etnografia, análise de documentos, histórias e cenários
- **Especificação** — montar backlog hierárquico (Epic → Feature [+ descrição + CAs] → User Story [+ BDD] → Task)
- **User Stories com BDD** — escrever o `DADO / QUANDO / ENTÃO` que conecta requisito a teste executável
- **Critérios de Aceitação declarativos** — regras testáveis por feature (com convenção `[...]` para sub-regras)
- **Estimativa colaborativa** — Story Points + Planning Poker (Fibonacci modificada)
- **Validação** — Sommerville 5 conferências + Falbo 7 dimensões + protótipos lo-fi/hi-fi
- **Gestão de mudança + rastreabilidade** — manter docs ↔ código ↔ teste alinhados
- **Análise de negócios** — BABOK v3, BPMN, AS-IS / TO-BE, MoSCoW, RICE
- **Decisão ética** — Código SBC 002/2024 aplicado a privacidade, ML/IA, inclusão, descontinuação

Não invoque para implementação pura de código. ER é a fase **antes** (descobrir o quê) e **depois** (validar que é o certo) — não no meio.

## 📖 Vocabulário (pt-BR vs en)

| pt-BR | en |
|---|---|
| Requisito Funcional / Não Funcional | Functional / Non-functional Requirement (FR / NFR) |
| DADO / QUANDO / ENTÃO | Given / When / Then |
| Critério de Aceitação | Acceptance Criterion (AC) |
| História de Usuário | User Story |
| Backlog do produto / da sprint | Product / Sprint Backlog |
| Engenharia de Requisitos | Requirements Engineering (RE) |
| Regra de Negócio | Business Rule |

Cucumber, Behave, SpecFlow e Behat suportam Gherkin localizado nativamente (`# language: pt` no cabeçalho do `.feature`).

## 📄 Licença

Conteúdo licenciado sob **[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.pt_BR)**.

Você pode compartilhar e adaptar livremente (inclusive comercialmente), desde que: (a) dê crédito apropriado e indique mudanças; (b) distribua contribuições sob a mesma licença.

Veja [`LICENSE`](./LICENSE) para o texto legal completo.
