# Contributing to `engenharia-de-requisitos`

Thanks for considering a contribution. This document explains **what** is welcome, **how** to propose changes, and the **conventions** every PR must respect.

> If you are looking only for a quick overview, the [README.md §🤝 Contributing](./README.md#-contributing) has the summary. This file is the operational detail.

---

## 1. What we accept

| Category | Examples | Priority |
|---|---|---|
| **New worked examples** | Case study from a real project in fintech, govtech, healthtech, SaaS multi-tenant, education, logistics, or any domain not yet covered in `examples/` | 🟠 High |
| **`.feature` template variants** | Stack-specific Gherkin templates (pytest-bdd, behave, cucumber-js, cucumber-playwright, SpecFlow, Behat, JBehave) | 🟠 High |
| **Tooling integration scaffolds** | Backlog templates for Linear / Jira / Notion / GitHub Issues / Plane / Shortcut that mirror the OpenProject hierarchy | 🟡 Normal |
| **Additional language translations** | Full or partial translation under `translations/<bcp-47-tag>/` (es, fr, de, it, ja, etc.) | 🟡 Normal |
| **Reference improvements** | Corrections of typos, factual errors, broken links, outdated citations in `references/` or `examples/` | 🔴 Immediate |
| **Anti-pattern submissions** | A new anti-pattern observed in the wild, with a concrete ❌/✅ example | 🟠 High |

## 2. What we do NOT accept

- **Implementation code** unrelated to RE/BA/Ethics (e.g., a Django CRUD example). This skill is content, not a code template.
- **Promotional content** for paid tools without disclosure (an Atlassian-vs-Linear comparison sponsored by either is out of scope).
- **Renaming pt-BR siglas** to English (`RF` → `FR`, `CA` → `AC`, `EP-NN` → `EP-NN`) — these are stable identifiers used by real projects; renumbering breaks years of OpenProject and Git traceability. See [README §Vocabulary](./README.md#-vocabulary-pt-br--en-ca-glossary).
- **Removal of pt-BR domain terms** preserved in *italic + quotes* (*"IFPB"*, *"Interpop"*, *"ABCD"*, *"COB"*, *"WADA"*, *"STJD"*, *"LGPD"*, *"SBC"*, *"CNPq"*, etc.). These are proper nouns whose meaning collapses if translated.

## 3. Process — 6 steps

### 3.1 Open an issue first (for non-trivial changes)

If your contribution adds a new file (case study, template variant, translation directory) or restructures any existing one, **open an issue first** describing the intent. Lets us catch direction conflicts before you invest writing.

Trivial fixes (typo, broken link, citation update) — skip the issue, go straight to PR.

### 3.2 Fork + branch

```bash
gh repo fork seekdevcore/sk-requirements-engineering-skill --clone --remote
cd sk-requirements-engineering-skill
git checkout -b <kind>/<short-description>
```

Branch naming convention:
- `feat/<thing>` — new content (`feat/case-study-fintech`, `feat/translation-es`)
- `fix/<thing>` — corrections (`fix/typo-references-04`, `fix/broken-link-readme`)
- `docs/<thing>` — meta-documentation (`docs/contributing-update`)
- `refactor/<thing>` — restructure existing without changing meaning

### 3.3 Make your change

For **new content**, follow the structural patterns:
- New case study → mirror [`examples/caso-interpop-moderacao.md`](./examples/caso-interpop-moderacao.md) structure (Context → Stakeholders → AS-IS/TO-BE → Feature → ACs grouped by theme → User Stories with BDD → Validation → Traceability → Ethical layer → Lessons).
- New `.feature` template → mirror [`examples/template-user-story.feature`](./examples/template-user-story.feature) (header comment with `@US`/`@F`/`@EP`/`@CAs`/`@SP`/`@Doc-Req`; ≥4 scenarios covering happy path + error + edge + outline).
- New translation → create `translations/<bcp-47-tag>/` with the full file tree mirrored from root.
- Reference improvement → keep the en-CA tone idiomatic; do not rewrite the structure unless explicitly fixing something broken.

### 3.4 Follow the hard rules (non-negotiable)

Every contribution must respect the **10 hard rules** documented in [`references/05-convencoes-interpop.md §2`](./references/05-convencoes-interpop.md):

- 🔴 **Source-of-truth document principle** (Rule 0)
- 🔴 **No infinitive verbs in Epic/Feature/US/RF/RNF/G titles** (Rule 1)
- 🔴 **No technical terms in Epic/Feature/US/CA/RF/RNF/G** (Rule 2)
- 🔴 **All artifacts have business-language descriptions** (Rule 8)
- 🔴 **Multiple root Epics, no single project-Epic** (Rule 9)
- 🔴 **`[...]` convention for ACs with sub-rules** (Rule 7)

Failure to respect these will surface in review and block merge.

### 3.5 Commit, sign, push

Conventional Commits format with **signed commits**:

```bash
git config commit.gpgsign true   # one-time if not already set

git add <files>
git commit -S -m "feat(examples): add fintech case study (PIX onboarding)

Real-project case based on a 2025 BACEN regulation rollout. Walks
through stakeholder identification, AS-IS/TO-BE analysis, 12 ACs
grouped by theme with 3 [...] details, 4 sliced User Stories with
BDD in pt-BR, full traceability commit-to-AC, and the SBC 002/2024
ethical layer applied to PIX privacy requirements.

Co-Authored-By: ... <...>"

git push -u origin <branch>
```

We use Conventional Commits scopes mapped to the directory:
- `feat(references)`, `feat(examples)`, `feat(translations)`, `feat(i18n)`
- `fix(references)`, `fix(typo)`, `fix(link)`
- `docs(readme)`, `docs(changelog)`, `docs(contributing)`

### 3.6 Open the PR

```bash
gh pr create --base main --fill
```

Use the PR template that opens automatically. The maintainer reviews within ~7 days; expect at least one round of review comments.

## 4. Code of Conduct

Participation in this project is governed by the [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) — Contributor Covenant 2.1 augmented with the *"SBC"* 002/2024 Code of Ethics references. Reports of violations go to gabriel.intetsu.dev@gmail.com.

## 5. License of contributions

By submitting a PR, you agree that your contribution will be licensed under [**Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**](./LICENSE) — the same license as the rest of the skill.

In practice this means:
- You retain copyright of your contribution.
- You grant everyone the right to share and adapt under the same license.
- You must indicate the source instructor of the primary corpus (Prof. Dr. *"Juliana Dantas Ribeiro Viana de Medeiros"* — see [README §About the source instructor](./README.md#-about-the-source-instructor)) when redistributing.

If you cannot agree to CC BY-SA 4.0 (e.g., your employer requires a different license), please discuss in an issue first.

## 6. Recognition

All contributors are listed in the GitHub contributors page automatically. Significant contributions (new case studies, translations, major refactors) are also acknowledged explicitly in the [CHANGELOG.md](./CHANGELOG.md) entry of the release that includes them.

## 7. Questions?

- General questions about the skill: open a [Discussion](https://github.com/seekdevcore/sk-requirements-engineering-skill/discussions).
- Specific contribution proposal: open an [Issue](https://github.com/seekdevcore/sk-requirements-engineering-skill/issues/new/choose).
- Direct contact (maintainer): [@GabeMarques-Intetsu](https://github.com/GabeMarques-Intetsu).
