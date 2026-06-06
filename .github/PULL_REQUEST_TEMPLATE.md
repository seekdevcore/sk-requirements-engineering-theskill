<!--
Thanks for your contribution. Fill in the sections below and check the
applicable boxes. Items that do not apply may stay unchecked or be removed.
-->

## What is this PR?

<!-- 1–3 sentences in plain English (or pt-BR) describing the change. -->

## Type

- [ ] 🟠 New worked example (case study) — `examples/<file>.md`
- [ ] 🟠 New `.feature` template variant — `examples/<file>.feature`
- [ ] 🟡 Tooling-integration scaffold (Linear / Jira / Notion / Plane / etc.)
- [ ] 🟡 New or updated translation — `translations/<bcp-47-tag>/`
- [ ] 🔴 Fix — typo / broken link / factual correction / outdated citation
- [ ] 🟠 New anti-pattern submission with ❌/✅ example
- [ ] 🟡 Documentation / meta (README, CONTRIBUTING, CHANGELOG, etc.)
- [ ] Other (please describe):

## Origin

- [ ] Linked to issue **#____**
- [ ] No issue — trivial fix (typo, broken link)
- [ ] No issue — discussed via [Discussions](https://github.com/seekdevcore/sk-requirements-engineering-skill/discussions)

## Hard-rules checklist (per `references/05-convencoes-interpop.md`)

If your PR touches Epic / Feature / User Story / AC / FR / NFR / business-rule (G) artifacts in any file, confirm:

- [ ] **Rule 0** — Source-of-truth document principle respected (any backlog change has matching requirements-document update)
- [ ] **Rule 1** — No infinitive verbs in titles (use noun / gerund)
- [ ] **Rule 2** — No technical terms in Epic / Feature / US / CA / RF / RNF / G (those belong in Tasks)
- [ ] **Rule 7** — ACs grouped under `CA - <Theme>` + `[...]` convention for sub-rules
- [ ] **Rule 8** — All artifacts have business-language descriptions
- [ ] **Rule 9** — Multiple root Epics where appropriate (no single "Project-Epic" parent)

## Language & convention preservation

- [ ] Brazilian **pt-BR siglas preserved verbatim** (`RF`, `RNF`, `G`, `CA`, `US`, `EP-NN`, `F-NN`, `USNN.M`, `TNN.M.K`, `TX-NN`, `G-NN`) — not renamed to English equivalents
- [ ] Brazilian **domain terms in *italic + quotes*** when newly introduced (e.g., *"IFPB"*, *"Interpop"*, *"LGPD"*, *"SBC"*, *"CNPq"*)
- [ ] **Cross-references** to other reference files use existing pt-BR filenames (no rename)
- [ ] If touching `references/09-etica-sbc.md`: *"SBC"* 002/2024 Code citations remain non-official English renderings; authoritative pt-BR copy at `translations/pt-BR/references/09-etica-sbc.md` is untouched (or updated in parallel)

## Quality

- [ ] Examples are **concrete** (real values like `"kpop"`, `"R$ 100"` — not placeholders like `"a value"`)
- [ ] BDD scenarios are **3–7 steps**, focus on ONE behaviour, domain-language (not UI selectors)
- [ ] If new files added, the [`README.md`](../README.md) repository-structure listing was updated
- [ ] If feature-relevant, the [`CHANGELOG.md`](../CHANGELOG.md) has an entry under `## [Unreleased]` (or the next-version section)

## Commit hygiene

- [ ] Commits follow **Conventional Commits** format (`feat(scope): …`, `fix(scope): …`, `docs(scope): …`)
- [ ] Commits are **signed** (`git commit -S`)
- [ ] Co-Authored-By trailer present if AI assistance was used

## License acknowledgement

- [ ] I agree my contribution is licensed under **CC BY-SA 4.0** (the same as the rest of this skill).
- [ ] If my contribution derives from another source, I cited it and confirmed the source license is compatible with CC BY-SA 4.0.

## Anything else for the reviewer?

<!-- Context, edge cases, trade-offs, screenshots, open questions, etc. -->
