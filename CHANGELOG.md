# Changelog

All notable changes to the `engenharia-de-requisitos` Claude Code skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

*No changes yet. New entries will accrue here under the appropriate Keep-a-Changelog headings (`### Added` / `### Changed` / `### Fixed` / `### Removed` / `### Deprecated` / `### Security`) before being rolled into the next tagged release.*

---

## [1.7.0] — 2026-06-10

Makes the on-disk structure (added in v1.6.0) **mandatory and automatic** instead of one optional trigger among many. The root cause this release fixes: when the skill was applied to a project, it would happily produce a loose `REQUISITOS_UNIFICADO.md` and **never build the `docs/` traceability spine**, and a project upgrading from a pre-`docs/` version was silently misclassified as GREENFIELD — its existing monolithic requirements doc ignored. The structure check is now the **first action** the skill takes on any project (§0), and the scaffolder gained a fourth detection verdict to recognize legacy monoliths.

### Added

- **`SKILL.md` §0 — "FIRST ACTION — structure-state check (MANDATORY, runs once per project, before anything else)"**. A new top-of-file section, placed *before* §1, that makes detecting/building the on-disk structure the **first thing the skill does** when applied to a project — analogous to elicitation preceding specification. It defines a 5-step protocol (auto-analyze the project for context → detect the structure state → act on the verdict → adapt the seeds → only then proceed) and a verdict→action table. The explicit principle: **the user never has to ask for the structure; its absence is the trigger to build it.** Closes the failure mode where older versions wrote a loose requirements doc and stopped.
- **`assets/scaffold-structure.sh` — `LEGACY-MONOLITH` detection (4th verdict)**. The detect step now also scans the repo root (CWD) and the docs root for a single loose requirements document (`requisito*.md`, `requirements.md`, `srs*.md`, `documento*requisito*.md`, `*requisitos*unificad*.md`, case-insensitive, excluding the structured `requirements/` subtree). When found with no spine, the target is classified **LEGACY-MONOLITH** instead of GREENFIELD, the candidate file(s) are reported, and migration guidance is printed. The scaffolder **never auto-splits** a monolith (prose decomposition into per-module RF/RNF needs judgment) — it creates the structure and hands the split to the operator. Verified: `bash -n` clean; smoke-tested that a loose `REQUISITOS_UNIFICADO.md` now yields LEGACY-MONOLITH while an empty dir still yields GREENFIELD (no false positives).
- **`references/10-estrutura-projeto.md` §8.1 — "Migrating a LEGACY-MONOLITH (upgrading from a pre-`docs/` skill version)"**. A step-by-step migration playbook: scaffold the spine → decompose the monolith into `RF/`+`RNF/` (preserving original `RF-NN` IDs), seed personas + glossary from it → keep the original as a linked consolidated overview (no duplicate-truth) → backfill `RF ↔ EP ↔ F` traceability.

### Changed

- **`SKILL.md` §0 — two first-run decisions wired into the protocol (new step 3, "infer → recommend → ask only if ambiguous")**: **(a)** `specs/` vs `--no-specs`, which **fixes the ADR tiering** (single-tier `planning/adrs/` vs two-tier with `specs/<feature>/adrs/`) — inferred from the §10 decision table, asked via `AskUserQuestion` when ambiguous (the scaffolder defaults to `--with-specs`, so `--no-specs` must be passed explicitly); **(b)** on an **existing** project only, an explicit `AskUserQuestion` offering to **backfill** the documentation the skill defines for work that already shipped (full now / only what the current task touches / structure-only-later), since backfill can be large and is the user's call. The verdict table (now step 4) annotates the per-verdict backfill offer; greenfield skips backfill. Cross-referenced from `references/10-estrutura-projeto.md` §10 (specs decision) and §9 Step 2.7 (backfill).
- **`SKILL.md` §1 (triggers)**: added a first-line trigger — *"Being applied to a project for the first time (or migrating one from an older skill version)"* — pointing to §0, so the structure step reads as the mandatory first action, not just one bullet among the elicitation/specification triggers. Updated the §5 Phase B scaffolder subsection with a banner cross-linking back to §0 (the *when*; §5 is the *how*). Updated `content_status.en-CA`.
- **`references/10-estrutura-projeto.md`**: standing rule 2 ("always detect before acting") now states it is the **first, automatic action every time the skill touches a project**, lists the LEGACY-MONOLITH path, and links to `SKILL.md §0`. §7 documents the new fourth verdict and the never-auto-split policy. §3 gained an explicit callout clarifying **one file per MODULE, not per requirement** — `RF/` filenames are named by the module's first requirement (`RF-01-<module>.md` holds RF-01..RF-04), so gaps in *filenames* are module boundaries, never missing requirements. The same callout is mirrored in the generic `assets/templates/requirements/README.md` so every scaffolded project carries it (closes a common "did it only create the prioritized RFs?" confusion).
- **`README.md`**: added a "First contact with a project (mandatory first action)" bullet to *When to invoke*; added `references/10-estrutura-projeto.md` + the `assets/` tree (scaffolder + generic templates) to the repository-structure listing; corrected the en-CA reference count `10 → 11 files`; updated the usage-pattern line to mention §0.
- **Priority scale — `Low` icon `⚪ → 🟢`**: the lowest priority tier now renders as a green circle instead of a white/empty one, across the whole corpus (`SKILL.md`, `references/05-convencoes-interpop.md` + `10-estrutura-projeto.md`, `examples/`, `assets/templates/`, and the `translations/pt-BR/` snapshot). The full scale is now 🔴 Immediate · 🟠 High · 🟡 Normal · 🟢 Low.
- **Version**: `SKILL.md` frontmatter, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` `1.6.0 → 1.7.0` (the three manifests stay aligned this release).

---

## [1.6.0] — 2026-06-09

The skill gains an **on-disk project-structure layer**: a canonical reference for the `requirements/` + `backlog/` + `specs/` + two-tier-ADR layout (everything under a single `docs/` root), a safety-first `detect → create → reorganize` scaffolder, and a generic, adaptive template tree (distinct from the Interpop-filled `examples/`). Two latent repo bugs surfaced while wiring CI for the release were fixed in passing.

### Added

- **`references/10-estrutura-projeto.md`** — new canonical reference for the **on-disk project structure** that materializes the traceability spine: `requirements/` (the *why/what*), `backlog/` (the *who/what/when*), `specs/` (the *how* — SDD), and the **two-tier ADR scheme**. Documents the purpose of each folder, the file anatomy of every artifact (RF, RNF, Epic, Feature), and — the part most projects get wrong — the **single continuous global ADR numbering across both tiers** (`planning/adrs/` for project-level decisions, `specs/<feature>/adrs/` for feature-level, with `INDEX.md` by layer + a living `tracker.md` ADR↔Task↔Test matrix, variant tags `-DB`/`-FE`/`-UI`, never-renumber / never-edit-a-decided-ADR rules). Includes "adopt in a new project" and "reorganize an existing project" playbooks + a SDD decision table. Mirrors the canonical *"Interpop"* reference implementation.
- **`assets/templates/`** — a **generic, placeholder-based template tree** (17 files) mirroring the target layout (`requirements/`, `backlog/`, `planning/adrs/`, `specs/_feature-template/`). Distinct from the Interpop-filled `examples/`: `examples/` is the *concrete reference* ("what done looks like"), `assets/templates/` is the *adaptive starting point* ("your skeleton"). Each file is marked `<!-- GENERIC TEMPLATE -->` and carries `<...>` placeholders + "adapt to your project" hints, while respecting all naming/ID/priority/traceability rules.
- **`assets/scaffold-structure.sh`** — companion scaffolder/reorganizer. Now runs a fixed **detect → create → reorganize** pipeline every invocation: **(1) detect** classifies the target (`GREENFIELD` / `HAS-STRUCTURE` / `LOOSE-FILES`) and lists any stray files; **(2) create** mirrors `assets/templates/` into the root (DRY — copies the generic files, no inline heredocs); **(3) reorganize** auto-runs when loose `RF-*`/`RNF-*`/`EP-*`/`F-*`/`sprint-*`/`ADR-*` files are detected, moving them via **`git mv`** (history-preserving; ambiguous files reported, not touched). Root **defaults to `docs/`** (single-root convention, warns otherwise). Safety-first: **dry-run by default**, **never overwrites**. Flags: `--root`, `--with-specs`/`--no-specs`, `--reorganize`/`--no-reorganize`, `--apply`. Validated: `bash -n` clean; smoke-tested for greenfield detect+create, idempotent re-apply (HAS-STRUCTURE), `--no-specs`, and LOOSE-FILES auto-reorganize via `git mv` (with dedup of the globstar double-match).

### Changed

- **`references/10-estrutura-projeto.md`**: added the **two standing rules** (single root named `docs/`; always detect before acting), the **two-template-layers** clarification (Interpop `examples/` vs generic `assets/templates/`), a new **§9 "Adaptation protocol"** (detect the host project's language/modules/roles/domain → adapt the seeds, or create the default when greenfield; hard rule: never commit placeholder files), and rewrote §7/§8 around the detect-driven scaffolder. Renumbered the SDD-decision and cross-reference sections (now §10/§11).
- **SKILL.md**: added an on-disk-structure trigger to §1 and an "On-disk project structure (folders, not just files) + scaffolder" subsection to §5 Phase B (Specification), updated to emphasize the `docs/` root, the generic-vs-Interpop template layers, and the Adaptation protocol. Updated `content_status.en-CA`.
- **Version alignment**: `SKILL.md` `1.5.0 → 1.6.0`, and `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` `1.3.0 → 1.6.0` (the two manifests had drifted behind `SKILL.md` since v1.4.0 — now realigned).

### Fixed

- **`.github/workflows/quality.yml`** — the 5 quality jobs were guarded on `github.repository == 'seekdevcore/sk-requirements-engineering'`, but the repo had been renamed (canonical is now `…-theskill`), so **every job was skipping repo-wide** — the quality gate was silently disabled. Switched to `github.repository_owner == 'seekdevcore'`, which survives the current rename and a future reclaim of the old name. Also added `--exclude-path assets/templates` to the lychee link-check (generic templates carry intentional, non-resolvable placeholder links).
- **`mcp-server/tests/smoke.py`** — the hardcoded `references count == 10` assertion now expects `11` (accounts for the new `10-estrutura-projeto.md`); `mcp-server/README.md` resource table updated to match.

---

## [1.5.0] — 2026-06-07

Infrastructure cleanup. **No content change** — same skill, same MCP server, same plugin marketplace; one less moving part in the distribution layer.

### Removed

- **Personal fork at `GabeMarques-Intetsu/sk-requirements-engineering-skill`** has been **permanently deleted**. The fork existed (since v1.0.0) as a discoverability proxy: it let the project owner pin a "personal" copy on their GitHub profile when the canonical upstream was hosted under the `seekdevcore` account. As of today, GitHub has indexed the owner's 23 commits on the upstream as a recognized contribution, so the upstream `seekdevcore/sk-requirements-engineering` is directly pinnable on the owner's profile via `Customize your pins → search → seekdevcore/...`. The fork no longer served any purpose, so it was deleted.
- The companion **`sync-upstream.yml` workflow that existed only on the fork** (introduced in v1.3.0 and documented in `CHANGELOG.md §1.3.0` / `§1.4.0`) was deleted along with the fork. There is no fork to keep in sync any longer. The upstream `quality.yml` and its `mcp-smoke` job (added in v1.4.0) remain intact.

### Changed

- **SKILL.md frontmatter**: `version: 1.4.0` → `1.5.0`.
- **Local git remotes** of contributors who had previously cloned the fork need to remove the `fork` remote (`git remote remove fork`). The single canonical remote is now `origin` pointing to `seekdevcore/sk-requirements-engineering`.

### What did NOT change

- Native skill content (`SKILL.md`, `references/`, `examples/`, `translations/pt-BR/`) — untouched.
- Plugin marketplace manifest (`.claude-plugin/marketplace.json`, `plugin.json`) — untouched.
- MCP server (`mcp-server/`) — untouched.
- Branch protection (`main-protection` ruleset with 6 rules + 5 required status checks) — intact.
- Releases v1.0.0..v1.4.0 — preserved on the upstream (they had also existed on the fork as mirrors, but those copies are gone with the fork).

### Why a minor bump (not a patch)

Semver-strict would classify "infra cleanup with zero API/content surface change" as a patch (1.4.1). The bump to 1.5.0 is a deliberate signal that **the distribution topology of the project changed visibly** — anyone tracking releases who had previously installed from the fork now needs to switch their remote / install URL to the upstream. Marking this as a minor release (rather than burying it as a patch) surfaces that change in the release feed and in dependency-update tooling.

### Historical references to the fork

Earlier CHANGELOG entries (`§1.3.0` "Added — Auto-sync (fork only)" and `§1.4.0` "Added — Claude Code plugin manifest") describe the fork as still existing. Those entries are kept verbatim as a historical record of what the project state was at the time of those releases — editing past changelog entries to retroactively pretend the fork never existed would violate the Keep-a-Changelog "do not rewrite history" principle.

---

## [1.4.0] — 2026-06-06

Cross-platform distribution: same corpus now reachable from Claude Code (native skill + plugin marketplace) and from any MCP client (Claude Desktop, Cursor, Cline, Continue, Zed, OpenAI Responses API, custom agents). **No content change** in `references/`, `examples/`, or `translations/pt-BR/`.

### Added

- **Claude Code plugin manifest** — `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json` make this repo installable via `/plugin marketplace add seekdevcore/sk-requirements-engineering` followed by `/plugin install engenharia-de-requisitos`. Mirrors the schema used by the `karpathy-skills` and `claude-plugins-official` marketplaces.
- **MCP server** — `mcp-server/` Python package built with FastMCP (`mcp[cli]>=1.2.0`), exposing the corpus to any MCP-compatible client (Claude Desktop, Cursor, Cline, Continue, Zed, OpenAI Responses API, custom LangChain/LlamaIndex agents). Resources: `requirements://skill`, `requirements://reference/{name}`, `requirements://example/{name}`, `requirements://catalog`. Tools: `list_references()`, `list_examples()`, `list_hard_rules()`, `validate_user_story(title, bdd?)` (INVEST + naming-convention check), `validate_acceptance_criterion(text)` (Interpop AC rule check). Layout: `mcp-server/src/requirements_engineering_mcp/server.py`, `pyproject.toml`, `.python-version` (3.12), and full per-client setup docs in `mcp-server/README.md`.
- **`mcp-smoke` CI job** — fifth job in `quality.yml` that installs `uv`, syncs `mcp-server/` dependencies, imports the server module, and asserts the corpus is discoverable (10 references + 5 examples found; all tools return non-empty strings; validators run without raising). Prevents regressions where the MCP server compiles but cannot locate the corpus.

### Changed

- **README §Installation** — opens with a 3-row comparison table (Native skill / Plugin marketplace / MCP server) explaining when to use which path. Plugin install (1-liner) and MCP server (with Resources + Tools matrix) added as new top-level sections.
- **README repository-structure** block updated to list `.claude-plugin/` and `mcp-server/`.
- **`.gitignore`** — adds `mcp-server/.venv/`, `mcp-server/.pytest_cache/`, `*.egg-info/`, `build/`, `dist/`. (`uv.lock` is intentionally tracked for reproducibility.)

---

## [1.3.0] — 2026-06-06

Operational maturity hardening after the v1.2.0 content milestone. **No content change** in `references/`, `examples/`, or `translations/pt-BR/` — only branding, community-health, CI, and branch-protection plumbing.

### Added

#### Branding & visual identity

- `assets/banner.png` — hero banner (1672×941, ~1.9 MB) with full English alt-text describing the pt-BR diagram for accessibility and SEO. Displayed at the top of `README.md` via `<p align="center"><img width="100%" ...>` so it renders as the GitHub repo hero.

#### Community-health

- `CONTRIBUTING.md` — 7-section operational guide: what is accepted (with priority), what is not, 6-step contribution process (issue-first for non-trivial, `kind/short-description` branch naming, hard-rules checklist, Conventional Commits + signed commits), recognition policy, license acknowledgement. Surfaces as the "Contributing" link in the GitHub repo header.
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1 augmented with explicit cross-references to *"SBC"* 002/2024 sections that already underpin `references/09-etica-sbc.md` (§1.1, §1.2, §1.3, §1.4, §3.1, §3.6). Includes §7 alignment-with-content note: the community producing this skill is held to the same ethics it teaches.
- `.github/PULL_REQUEST_TEMPLATE.md` — auto-loads on PR creation with hard-rules checklist (Rules 0, 1, 2, 7, 8, 9), language-preservation checklist (siglas, italic+quotes, cross-refs, *"SBC"* citations), quality bar (concrete examples, BDD step count, README/CHANGELOG sync), commit hygiene (signed, Conventional Commits, Co-Authored-By), and license acknowledgement.
- `.github/ISSUE_TEMPLATE/config.yml` — disables blank issues, surfaces 3 contact links (Discussions, source-instructor section, CoC).
- `.github/ISSUE_TEMPLATE/bug-or-fix.yml` — 🔴 typed form for typo, broken link, factual error, outdated citation, en-CA↔pt-BR inconsistency, hard-rules violation in example.
- `.github/ISSUE_TEMPLATE/content-proposal.yml` — 🟠 typed form for case study, `.feature` template variant, tooling scaffold, translation, anti-pattern submission. Requires motivation, scope, alignment with hard rules, stakeholder/source-ownership disclosure, license acknowledgement.
- `.github/ISSUE_TEMPLATE/question-or-clarification.yml` — 🟡 typed form for "this section is unclear" pointing to a specific file + section, with optional improvement proposal.

#### CI quality

- `.github/workflows/quality.yml` — 4-job parallel quality gate (markdown-lint via `DavidAnson/markdownlint-cli2-action@v17`, link-check via `lycheeverse/lychee-action@v2` with 14-day cache, yaml-schema via `yamllint`, actionlint via `raven-actions/actionlint@v2`). `concurrency` group cancels superseded runs; `permissions: contents read` enforces least-privilege.
- `.markdownlint.json` — 8 rules disabled or relaxed with inline `_<RULE>` comments explaining each decision (line-length irrelevant for content tables; allowed inline HTML for banner; emphasis-as-heading disabled for `**bold**` Brazilian-domain terms; bare URLs allowed for bibliographic citations; first-line H1 disabled for `<p>` banner; `MD024 siblings_only` for repeated `### Added` across CHANGELOG versions; `MD028` disabled for separated `>` blockquote paragraphs; `MD033` disabled for `<termo>/<nome>/<id>` placeholders in OpenProject backlog template; `MD051` disabled for anchor links with emoji prefixes; `MD060` disabled for compact `|---|---|` table style).
- `.lycheeignore` — 12 URL patterns intentionally skipped: Brazilian academic systems that rate-limit aggressively (*"Lattes"*, *"CNPq"*, *"ORCID"*, *"IFPB"*, *"SBC"*), the ACM Code of Ethics URL (Cloudflare 403 for non-browser User-Agents), the IEEE governance URL (418 "I'm a teapot" for bots), placeholder URLs in templates (`example.com`, `your-domain`, `seu-dominio`), sibling-project documentary paths (*"Interpop"* docs/specs), private-workspace URLs in worked examples (Figma file, Notion private workspaces).
- `.yamllint.yml` — extends default with `line-length max 200` (warning, not error), `document-start` disabled, `truthy check-keys` disabled (so GitHub Actions `on:` key is not flagged), 2-space indentation with consistent sequences. Ignores `translations/pt-BR/` and `node_modules/`.

#### Branch protection (upstream only)

- Ruleset `main-protection` (ID `17348015`) on `seekdevcore` upstream — `enforcement: active`, targeting default branch:
  - Restrict deletions.
  - Block force pushes (`non_fast_forward`).
  - Require signed commits.
  - Require linear history (no merge commits).
  - Require pull request before merging: 1 approval, `dismiss_stale_reviews_on_push: true`, `required_review_thread_resolution: true`, allowed merge methods `[merge, squash, rebase]`.
  - Require 4 status checks to pass: `markdown-lint`, `link-check`, `yaml-schema`, `actionlint`.

#### Auto-sync (fork only)

- `.github/workflows/sync-upstream.yml` — exists **only on the fork** (`GabeMarques-Intetsu/sk-requirements-engineering-skill`), not on the upstream. Runs every 30 minutes via cron + on-demand via `workflow_dispatch`. Uses `gh CLI` directly (no third-party Action) to minimize supply-chain surface. Keeps fork main in sync with upstream main automatically.

### Changed

- **Publisher display name rebranded `Seekdev` → `Seek`** in `README.md` Maintainer section. The GitHub handle remains `seekdevcore` (cannot be changed without renaming the account); only the human-facing label changed.
- **README hero**: replaced badges-only top with banner image + 4 badges + bilingual reader note explaining what remains in pt-BR by design (domain terms, real-project identifiers, *"IFPB"* course Gherkin, `.feature` template).
- **README repository-structure** section updated to list `assets/`, `.github/`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
- **README Contributing section** rewritten: removed "remaining en-CA translation" item (closed in v1.2.0); replaced with "Additional language translations under `translations/<bcp-47-tag>/`" to set the pattern for future i18n.
- **SKILL.md frontmatter** synced with v1.2.0 reality: `version: 1.1.0` → `1.2.0`; `content_status.en-CA: partial — entry point translated; references and examples in progress` → `complete — entry point, references/ (10 files), and examples/ (5 files) all translated`.
- **`quality.yml` jobs guarded** with `if: github.repository == 'seekdevcore/sk-requirements-engineering'` so the workflow does not run duplicated on the fork mirror (which received `.github/workflows/quality.yml` via `gh repo sync`). On the fork, all 4 jobs report `skipped` — no runner spawned, no notification fired.

### Fixed

- **Enforcement-channel email** in `CODE_OF_CONDUCT.md` §5 and `CONTRIBUTING.md` §4: `gabriel.santos.23@academico.ifpb.edu.br` → `gabriel.intetsu.dev@gmail.com`. The *"IFPB"* academic address is tied to a single institutional role and may rotate; the personal Gmail is the stable, long-lived inbox.
- **Broken intra-skill link** in `references/03-especificacao.md` §12: pointer to `references/06-estimativa.md` (a file that does not exist — legacy renumbering plan that never materialized). Removed the broken pointer; kept the live link to `references/05-estimativa.md`.
- **Relative-path link** in `.github/PULL_REQUEST_TEMPLATE.md`: `../../discussions` (which `lychee` cannot resolve from `file://` scheme during CI) → absolute `https://github.com/seekdevcore/sk-requirements-engineering/discussions` URL.
- **First CI run (commit `a21693f`)**: 4 link-check errors + 50+ markdown-lint violations. Resolved across 2 follow-up commits — auto-fixes for whitespace rules (MD031, MD032) applied across 16 files, 4 rules disabled with rationale (MD028, MD033, MD051, MD060), 2 link-check fixes (broken `06-estimativa` ref + PR-template relative URL), 2 false positives excluded (ACM 403 + IEEE 418).

### Workflow validation (end-to-end)

- **PR #1** (`chore(changelog): add [Unreleased] section per Keep a Changelog spec`) — first PR after branch protection went live. Validated: (1) push to feature branch (not main directly), (2) PR via `gh pr create`, (3) 4 required status checks passing, (4) cross-account approval (PR author `GabeMarques-Intetsu` → approver `seekdevcore` via `gh auth switch`), (5) squash merge with auto-delete-branch. Time: ~45s from open to merged.
- **PR #2** (`ci(quality): guard all 4 jobs to run only on the canonical upstream repo`) — re-validated the workflow and verified the guard itself by self-reference (the PR ran the workflow on the upstream where `github.repository` evaluates to the canonical value, so checks executed and passed).

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
