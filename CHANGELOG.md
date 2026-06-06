# Changelog

All notable changes to the `engenharia-de-requisitos` Claude Code skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] — 2026-06-06

### Changed — Full en-CA content translation completed

This release closes the translation roadmap announced in v1.1.0. **All `references/` (10 files) and `examples/` (5 files) now have en-CA content** alongside the previously translated entry point (SKILL.md, README.md, CHANGELOG.md). The original pt-BR source remains preserved at `translations/pt-BR/`.

#### What got translated (Packages 2–6)

| Package | Files | Lines processed |
|---|---|---|
| **2** | `references/01-fundamentos.md` + `02-elicitacao.md` + `03-especificacao.md` | ~1,266 |
| **3** | `references/04-bdd-criterios-aceitacao.md` + `05-convencoes-interpop.md` + `05-estimativa.md` | ~1,221 |
| **4** | `references/06-validacao.md` + `07-mudanca-rastreabilidade.md` + `08-analista-negocios.md` + `09-etica-sbc.md` | ~1,128 |
| **5** | `examples/caso-controle-dopagem.md` + `caso-interpop-moderacao.md` | ~817 |
| **6** | `examples/template-backlog-openproject.md` + `template-documento-requisitos.md` + `template-user-story.feature` | ~1,022 |

**Total**: ~5,454 additional lines processed across 13 files. Including the v1.1.0 entry point (~750 lines), **~6,200+ lines** of content now have en-CA renderings.

#### Translation principles applied (consistent across all 6 packages)

1. **Idiomatic en-CA** for explanations, rules, headers, field labels, analysis.
2. **Brazilian pt-BR siglas preserved verbatim** (`RF`, `RNF`, `G`, `CA`, `US`, `EP-NN`, `F-NN`, `USNN.M`, `TNN.M.K`, `TX-NN`, `G-NN`) for backward compatibility with real projects (*"Interpop"*, *"SIRA"*, *"Controle de Dopagem"*).
3. **Brazilian domain terms in *italic + quotes*** throughout: *"IFPB"*, *"Interpop"*, *"SIRA"*, *"ABCD"*, *"COB"*, *"WADA"*, *"STJD"*, *"CNPq"*, *"LGPD"*, *"BACEN"*, *"ANS"*, *"DATAPREV"*, *"CESAR"*, *"CAGEPA"*, *"EMBRAPII"*, *"SBC"*, *"Bolsa Atleta"*, *"Controle de Dopagem"*, *"Busca Editorial"*, *"Sistema de Reserva de Salas IFPB"*, *"Soft Power"*, *"Hostinger"*, *"Gabriel"* (project owner), *"Gabriel Marques"*, *"Profa. Juliana Dantas Ribeiro Viana de Medeiros"*, *"Profa. Thais Vasconcelos Batista"*, etc.
4. **Real-world worked examples preserved verbatim in pt-BR** when they reproduce identifiers from external systems:
   - Original *"IFPB"* / *"Controle de Dopagem"* item titles (`EPIC APLICAÇÃO WEB`, `FEATURE Bolsa Atleta recebidas`, `CA09 — O combobox FEDERAÇÃO...`) — they appear verbatim in Redmine cards, *"SVN"* commits, and academic papers.
   - Real *"Interpop"* artifacts (`EP-10 Busca Editorial`, `F-30 Busca de artigos por texto`, US BDD scenarios, Task descriptions with technical terms) — they are the actual cards in the *"Interpop"* OpenProject and the actual content of *"Busca Editorial"* `BACKLOG.md` v1.2.
   - *"SBC"* 002/2024 Code citations — non-official English renderings only; authoritative pt-BR remains at `translations/pt-BR/references/09-etica-sbc.md`.
   - *"Interpop Moderação"* commit `1e0241e` content (`Hierarquia de Banimento`, `can_be_banned_by`, mensagem `"Operação não permitida pela hierarquia editorial"`) — actual strings in the production code.
5. **`examples/template-user-story.feature` kept as pt-BR Gherkin template by design** (with `# language: pt`) because it reproduces the format used by real teams; explicit en-CA dialect option documented in the header comment (drop the `# language: pt` line, use `Feature:`/`Scenario:`/`Given/When/Then`).
6. **Cross-references between files preserved with pt-BR filenames** (`references/04-bdd-criterios-aceitacao.md`, `examples/caso-controle-dopagem.md`, etc.) to avoid breaking existing intra-skill links and external project references.

#### Frontmatter changes

- `version: 1.1.0` → `version: 1.2.0`
- `content_status.en-CA: partial — entry point translated; references and examples in progress` → `content_status.en-CA: complete — all references and examples translated; pt-BR copy preserved at translations/pt-BR/`
- `content_status.pt-BR: complete — full copy available at translations/pt-BR/` (unchanged)

#### What did NOT change

- All FR/NFR/G/CA/EP/F/US/T/TX numeric identifiers and item titles across the worked examples (`EP-10`, `F-30`, `US30.1`, `CA01..CA15`, `G-01`, `G-02`, etc.).
- All `references/` and `examples/` filenames (still in pt-BR) — preserves cross-references and external project links.
- The pt-BR Gherkin keywords in `template-user-story.feature` — by design.
- LICENSE (CC BY-SA 4.0).
- Frontmatter triggers (both English and Portuguese activation triggers retained).
- The `translations/pt-BR/` snapshot (it is the authoritative pt-BR for compliance and audit reference).

#### Six signed commits in this release sequence (after v1.1.0)

| Tag | Commit | Description |
|---|---|---|
| v1.1.0 | `d9316de` | Entry point en-CA + `translations/pt-BR/` (Package 1) |
| — | `46b108b` | Package 2 (references 01-03) |
| — | `5bc2939` | Package 3 (references 04, 05-conv, 05-estim) |
| — | `e1677aa` | Package 4 (references 06-09) |
| — | `51630d8` | Package 5 (examples cases) |
| **v1.2.0** | `d9e8ca9` | Package 6 (examples templates) + this CHANGELOG update |

### Rationale

The skill is now fully usable by English-speaking practitioners while remaining 100% loyal to the original *"IFPB"* course material, the *"Interpop"* / *"SIRA"* / *"Controle de Dopagem"* real projects, and the *"SBC"* 002/2024 Code authoritative wording — all preserved in `translations/pt-BR/` and selectively cited verbatim throughout the en-CA content where pedagogically necessary.

---

## [1.1.0] — 2026-06-06

### Changed — Language switch: en-CA promoted to default content language

The skill's frontmatter declared `language: en-CA` as the default since v1.0.0, but actual content remained in pt-BR. This release executes the promised promotion for the **entry point** (SKILL.md + README.md + CHANGELOG.md) and reorganizes the repository so both languages live side-by-side.

#### Repository reorganization

- **New directory `translations/pt-BR/`** — contains the full pt-BR copy of all files (SKILL.md, README.md, CHANGELOG.md, references/, examples/). The original Portuguese material is preserved verbatim, so existing pt-BR projects (*"Interpop"*, *"SIRA"*, *"Controle de Dopagem"*) can continue referencing it.
- **Root files now in en-CA** — `SKILL.md`, `README.md`, `CHANGELOG.md` were rewritten in Canadian English idiom.
- **`references/` and `examples/` filenames preserved in pt-BR** — these filenames are referenced by external projects in commit messages, OpenProject backlogs, and traceability matrices. Renaming would break years of cross-references for no real gain. Their **internal content** translation to en-CA is the next milestone (v1.2.0).

#### Translation principles applied

- **Idiomatic English terminology** for general concepts: *Engenharia de Requisitos* → *Requirements Engineering*; *Critério de Aceitação* → *Acceptance Criterion*; *DADO / QUANDO / ENTÃO* → *Given / When / Then*.
- **Brazilian acronyms preserved verbatim**: `RF`, `RNF`, `G`, `CA`, `US`, `EP`, `F`, `T`, `TX`, `EP-NN`, `F-NN`, `CA-NN`, `USNN.M`, `TNN.M.K`, `TX-NN`, `G-NN`. These are how real projects identify items; English-renumbered IDs would break traceability and existing OpenProject queries.
- **Brazilian domain terms preserved in *italic + quotes***: *"IFPB"*, *"Interpop"*, *"ABCD"*, *"COB"*, *"Bolsa Atleta"*, *"LGPD"*, *"SBC"*, *"CNPq"*, *"DATAPREV"*, *"CESAR"*, *"CAGEPA"*, *"EMBRAPII"*, *"Controle de Dopagem"*, *"Ministério do Trabalho"*, *"Prefeitura Municipal de João Pessoa"*, *"IPTU"*, *"ITBI"*, *"Taxa de Lixo"*, *"Plano Plurianual e Orçamentário"*, *"Cadastro Mercantil"*, *"Plano Nacional de Qualificação"*. These are proper nouns, institutional names, and regulatory frameworks whose meaning collapses if translated.
- **Author credit per CC BY-SA 4.0** preserved and reinforced in the new attribution language.

#### Frontmatter changes

- `version: 1.0.1` → `version: 1.1.0`
- `content_status.en-CA: roadmap` → `content_status.en-CA: partial — entry point translated; references and examples in progress`
- `content_status.pt-BR: available (current default content)` → `content_status.pt-BR: complete — full copy available at translations/pt-BR/`

#### README badge changes

- `Version: 1.0.0` → `Version: 1.1.0`
- `Translation: pt-BR available` retained
- New row in *Language status* table reflecting the en-CA partial / pt-BR complete reality

#### Rationale

The previous state (`language: en-CA` declared, but content in pt-BR) was misleading for English-speaking users. Discoverability and trigger activation worked in English, but every artifact opened in Portuguese — a poor experience.

The chosen middle ground:
1. **Entry point (SKILL.md, README.md, CHANGELOG.md) in en-CA** — these are read first; they need to match the declared language.
2. **`references/` and `examples/` filenames in pt-BR for now** — preserves backward compatibility with existing projects.
3. **Full pt-BR copy at `translations/pt-BR/`** — pt-BR readers (the original audience of the *"IFPB"* course) lose nothing.
4. **Internal content of `references/` and `examples/` translation in progress** — package-by-package, with user review between each.

This release is a non-breaking content-language change for the entry point; existing skill activation (English and Portuguese triggers in the frontmatter) is unaffected.

### Added

- `translations/pt-BR/SKILL.md`, `translations/pt-BR/README.md`, `translations/pt-BR/CHANGELOG.md` — verbatim pt-BR copies for the entry point.
- `translations/pt-BR/references/` and `translations/pt-BR/examples/` — verbatim pt-BR copies of the canonical detail and worked examples.
- README *Vocabulary (pt-BR ↔ en-CA glossary)* section explaining the term-vs-acronym strategy.
- README *Contributing* section now specifies translation principles (preserve domain terms in italic+quotes; preserve acronyms; preserve cross-reference filenames).

### Not changed (deliberate)

- All FR/NFR/G/CA/EP/F/US/T/TX numeric identifiers across all examples and templates.
- All file-to-file cross-references (intra-skill links remain valid).
- License (CC BY-SA 4.0).
- Frontmatter triggers (both English and Portuguese activation triggers retained).

---

## [1.0.1] — 2026-06-06

### Added — Source instructor attribution

- **README.md**: new sections "About the source instructor" (EN) and "Sobre a autora do material-fonte" (PT-BR) with the full academic and industrial credentials of **Prof. Dr. Juliana Dantas Ribeiro Viana de Medeiros** (IFPB), the creator and instructor of the course material that constitutes the primary corpus of this skill. Includes Lattes link, ORCID, doctoral thesis title (*"An approach to support the Requirements Specification in Agile Software Development"*, UFPE 2017 with sandwich period at Universidade Nova de Lisboa), active research lines, 20+ years of industrial experience, faculty positions, and academic citation format.
- **SKILL.md** §10 renamed to "Fonte primária e bibliografia canônica" with new §10.1 "Autora do material-fonte" giving formal credit and explaining why her credentials matter for the reliability of the skill's claims.
- **SKILL.md** §10.2: added Valente (2020) reference for MVP + A/B testing material added in §1.5.1 of `01-fundamentos.md`.

### Rationale

Per CC BY-SA 4.0 license requirements (Attribution), the source instructor of the primary corpus must be appropriately credited. This also provides academic and industrial provenance for users evaluating the trustworthiness of the skill's content.

---

## [1.0.0] — 2026-06-06

### Added — Initial public release

#### Core skill files
- `SKILL.md` — 10-section entry point with usage protocol, premise (requirement-as-leverage), bibliography, anti-patterns, and naming rules. Includes:
  - Regra 0 (source-of-truth document) — backlog never changes without document update first
  - Regra 9 (multiple root Epics) — no single "Epic-project" parent; root Epics are siblings
  - Regra 10 (FR/NFR/G also subject to all conventions — language, descriptions, traceability)
  - 13 anti-patterns (Connextra title in card, qualitative NFR, AC+BDD competing, etc.)

#### Reference documents (`references/`)
- `01-fundamentos.md` — FR vs NFR, stakeholders, feasibility study, requirements in any lifecycle model (Sommerville Figs 2.1–2.3), professional engineering analogy, canonical "tree-swing" cartoon, 7 real failure cases (Mariner, Hartford, Citibank, UEFA, INSS, IPTU SP, Boeing 737 MAX), MVP + A/B testing as modern complements (Valente 2020).
- `02-elicitacao.md` — Sommerville 5 difficulties + Christel & Kang + Kotonya; 6 techniques compared; full coverage of interviews (5W planning, question types, pyramid/funnel/diamond structures, recording).
- `03-especificacao.md` — Backlog hierarchy with multiple root Epics, document vs backlog artifact split (5.1.1 RF/RNF/G + 5.1.2 Epic/Feature/CA/US/Task), User Story history (1997 Chrysler C3 → 2004 Cohn), 3 Cs of Jeffries, INVEST checklist, Spike as backlog item type.
- `04-bdd-criterios-aceitacao.md` — Declarative AC style, BDD pt-BR, Three Amigos, Given/When/Then localized, `[...]` convention formalized (§2.5), `Funcionalidade:` Gherkin keyword false friend explained, anti-pattern §7.7 "Feature with BDD instead of description".
- `05-estimativa.md` — Story Points, modified Fibonacci, Planning Poker procedure, anchoring vs proportional comparison, Definition of Ready post-estimation.
- `05-convencoes-interpop.md` — **10 hard rules** (Regra 0 source-of-truth, no infinitives, no technical terms, pt-BR explicit, configs ≠ Features, Interpop priority scale, Feature has description + US has BDD, AC always grouped under `CA - <Tema>` + `[...]` convention, all artifacts have descriptions, multiple root Epics).
- `06-validacao.md` — Sommerville 5 checks + Falbo 7 dimensions, prototype fidelity levels (lo-fi/mid/hi-fi/functional), ML/AI validation extra layer (SBC 2.5).
- `07-mudanca-rastreabilidade.md` — Change management, RTM (Requirements Traceability Matrix), enduring vs volatile requirements.
- `08-analista-negocios.md` — BABOK v3, BPMN, AS-IS/TO-BE, MoSCoW, RICE, Kano.
- `09-etica-sbc.md` — Full SBC 002/2024 Code applied to requirements engineering decisions (privacy, ML/AI, inclusion, decommissioning).

#### Examples and templates (`examples/`)
- `caso-controle-dopagem.md` — Real CNPq 487777/2013-1 case (ABCD/COB); FR + NFR + business rules G + exceptions E; backlog with multiple root Epics (Aplicação Web + Mobile + Atividades de Apoio); Feature "Consulta GERAL de Atletas" worked end-to-end with 15 grouped ACs (4 with `[...]`), 3 sliced User Stories with BDD, Planning Poker estimation.
- `caso-interpop-moderacao.md` — Interpop ban hierarchy (dev/admin/editor/user); 9 ACs grouped in 3 themes; 6 ACs with `[...]` detailing; 5 User Stories with BDD; technical annex with `can_be_banned_by` exhaustive matrix.
- `template-backlog-openproject.md` — Full worked backlog template (Busca Editorial Interpop + Cadastro de Atletas) showing multiple root Epics, 4-level Epic nesting, AC grouping, `[...]` convention, BDD as US Description field content, smell test.
- `template-documento-requisitos.md` — Requirements document template (IEEE 830 + Sommerville + Wiegers) with worked Busca Editorial example, history-of-revisions section, smell test.
- `template-user-story.feature` — Gherkin pt-BR ready-to-copy `.feature` file with 4 scenarios + Scenario Outline + Python (pytest-bdd) and TypeScript (cucumber-playwright) step definition examples.

### Language status

- **en-CA**: declared as default in frontmatter; **content translation is on the roadmap**.
- **pt-BR**: all content currently written in Brazilian Portuguese (original source — IFPB course taught in Portuguese).

### Source corpus

Full IFPB course material (LECTURE 0 through LECTURE 10, including LECTURE 03 real case and LECTURE 09.2 estimation) processed integrally. Canonical bibliography:

- Sommerville 10e (Ch. 4 read integrally)
- Pressman 9e
- Wiegers & Beatty 3e
- Cohn — User Stories Applied (2004)
- Robertson & Robertson — VOLERE method
- Hull, Jackson & Dick — Requirements Engineering 4e
- Falbo (UFES) — lecture notes
- IIBA — BABOK Guide v3
- SBC — Resolution 002/2024 (Code of Ethics and Professional Conduct)
- Valente — *Engenharia de Software Moderna* (engsoftmoderna.info, MVP + A/B)

### License

Released under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

---

## Roadmap (post 1.0.0)

- **en-CA full content translation** of `references/` and `examples/`.
- Sommerville Chapters 11–14 (dependability, security, resilience) integration.
- More worked case studies (SaaS multi-tenant, fintech, government).
- Tooling integration scaffolds: Linear, Jira, Notion, GitHub Issues, Plane.
- Exportable PDF/Markdown checklists.
- `.feature` template variants per stack (pytest-bdd, behave, cucumber-js, cucumber-playwright, SpecFlow, Behat).
