# Translations

> **en-CA is the DEFAULT and the universal FALLBACK.** The authoritative content lives at the repository **root** in **en-CA English** — `SKILL.md`, `references/`, `assets/` (templates · scaffolder · integrations), `examples/`, and the MCP validators. `translations/<lang>/` carries **only the localized deviations** for a language.

## Resolution rule (applies to EVERYTHING — SKILL, references, templates, examples, integrations, validators)

To resolve any file for a language `<lang>`:

1. If `translations/<lang>/<path>` exists → **use it**.
2. Otherwise → **fall back to the en-CA file at the root** (`<path>`).

A translation may therefore be **partial**: whatever it does not override resolves to en-CA. There is **no obligation to mirror every file** — a missing file is not a gap, it is a deliberate fallback to the default. This holds for *everything in the project*, integrations included (the Python adapters and the scaffolder are language-neutral code with en-CA comments; they simply have no translation and so always resolve to the root).

## Available translations

| Lang | Coverage |
|---|---|
| **en-CA** (root) | authoritative source — **everything** |
| **pt-BR** (`translations/pt-BR/`) | `SKILL.md` · `references/` (01–13 + `integrations/`) · `examples/` · `assets/templates/` (the 10 language-bearing templates; all other templates fall back to en-CA) |

## Adding a language

1. Create `translations/<lang>/` and mirror **only** the files whose wording must change, keeping the **same relative paths** as the root.
2. Leave everything else out — it falls back to en-CA automatically.
3. Brazilian domain proper nouns kept in *italics+quotes* (e.g. *"Interpop"*, *"IFPB"*, *"Controle de Dopagem"*) and the skill's IDs/acronyms (`RF`, `RNF`, `CA`, `US`, `EP`, `F`, `T`, `TX`, `BUG`, `QA`, `ISS`, `SPK`, `PM`, `RB`, `G`) are **language-neutral by design** — keep them identical across languages.

> Register the new language in `SKILL.md` → `available_translations`.
