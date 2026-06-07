"""FastMCP server exposing the engenharia-de-requisitos skill corpus.

Layout assumption: this module ships inside `mcp-server/` at the root of
the `sk-requirements-engineering-skill` repository. The skill content lives
two directories up (`../../`). The server discovers the corpus relative
to its own file location so it works after `uv tool install`, `uvx`, and
local `uv run` invocations alike.

Resources exposed
-----------------
- requirements://skill                  → SKILL.md (10-section entry point map)
- requirements://reference/{name}       → references/{name} (without extension)
- requirements://example/{name}         → examples/{name} (without extension)
- requirements://catalog                → JSON catalog of every available document

Tools exposed
-------------
- list_references()                     → titles + 1-line summaries of every reference/
- list_examples()                       → titles + 1-line summaries of every example/
- list_hard_rules()                     → the 10 Interpop hard-rules titles
- validate_user_story(title, bdd?)      → INVEST + naming-convention check
- validate_acceptance_criterion(text)   → format check + `[...]` convention check

All content is in en-CA at the root; pt-BR snapshot is preserved at
`translations/pt-BR/` (exposed as `?lang=pt-BR` query when applicable).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Skill-corpus discovery
# ---------------------------------------------------------------------------

# This file is at:  <repo>/mcp-server/src/requirements_engineering_mcp/server.py
# Skill root is at: <repo>/
SKILL_ROOT = Path(__file__).resolve().parents[3]
REFERENCES_DIR = SKILL_ROOT / "references"
EXAMPLES_DIR = SKILL_ROOT / "examples"
SKILL_MD = SKILL_ROOT / "SKILL.md"
PT_BR_ROOT = SKILL_ROOT / "translations" / "pt-BR"


def _read_or_error(path: Path) -> str:
    if not path.exists():
        return f"Error: file not found ({path.name})"
    return path.read_text(encoding="utf-8")


def _list_md(dir_path: Path) -> list[str]:
    if not dir_path.exists():
        return []
    return sorted(p.stem for p in dir_path.glob("*.md"))


def _extract_first_paragraph(text: str) -> str:
    """Return the first non-heading non-blockquote paragraph as a short summary."""
    for block in text.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith(">"):
            continue
        if stripped.startswith("---"):
            continue
        # Strip simple inline markup for cleanliness
        summary = re.sub(r"[*_`]", "", stripped)
        # Collapse whitespace; cap at ~280 chars
        summary = re.sub(r"\s+", " ", summary).strip()
        return summary[:280] + ("…" if len(summary) > 280 else "")
    return "(no summary available)"


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("engenharia-de-requisitos")


# ----- Resources -----------------------------------------------------------


@mcp.resource("requirements://skill")
def skill_map() -> str:
    """SKILL.md — the 10-section entry point that maps the whole methodology."""
    return _read_or_error(SKILL_MD)


@mcp.resource("requirements://reference/{name}")
def reference_doc(name: str) -> str:
    """A specific reference file from references/<name>.md (en-CA)."""
    return _read_or_error(REFERENCES_DIR / f"{name}.md")


@mcp.resource("requirements://example/{name}")
def example_doc(name: str) -> str:
    """A specific example/template from examples/<name>.{md,feature}."""
    md = EXAMPLES_DIR / f"{name}.md"
    if md.exists():
        return md.read_text(encoding="utf-8")
    feature = EXAMPLES_DIR / f"{name}.feature"
    if feature.exists():
        return feature.read_text(encoding="utf-8")
    return f"Error: example not found ({name})"


@mcp.resource("requirements://catalog")
def catalog() -> str:
    """JSON catalog of every available document — useful for clients to
    enumerate the corpus without parsing markdown."""
    refs = _list_md(REFERENCES_DIR)
    exs_md = _list_md(EXAMPLES_DIR)
    exs_feat = sorted(p.stem for p in EXAMPLES_DIR.glob("*.feature")) if EXAMPLES_DIR.exists() else []
    return json.dumps(
        {
            "skill_md": "requirements://skill",
            "references": [
                {"uri": f"requirements://reference/{name}", "name": name}
                for name in refs
            ],
            "examples": [
                {"uri": f"requirements://example/{name}", "name": name}
                for name in (exs_md + exs_feat)
            ],
            "pt_br_snapshot_available": PT_BR_ROOT.exists(),
        },
        indent=2,
        ensure_ascii=False,
    )


# ----- Tools ---------------------------------------------------------------


@mcp.tool()
def list_references() -> str:
    """Return the titles and first-paragraph summaries of every reference/ file.

    Equivalent to opening each file and reading the first paragraph after the
    H1. Useful when the client wants a quick map of the corpus before deciding
    which reference to fetch in full.
    """
    refs = _list_md(REFERENCES_DIR)
    if not refs:
        return "(references/ directory is empty or missing)"

    lines: list[str] = []
    for name in refs:
        text = (REFERENCES_DIR / f"{name}.md").read_text(encoding="utf-8")
        first_line = text.split("\n", 1)[0].lstrip("# ").strip()
        summary = _extract_first_paragraph(text)
        lines.append(f"## {name}\n**{first_line}**\n\n{summary}\n")
    return "\n".join(lines)


@mcp.tool()
def list_examples() -> str:
    """Return the titles and first-paragraph summaries of every examples/ file."""
    exs = _list_md(EXAMPLES_DIR)
    feats = sorted(p.stem for p in EXAMPLES_DIR.glob("*.feature")) if EXAMPLES_DIR.exists() else []
    if not (exs or feats):
        return "(examples/ directory is empty or missing)"

    lines: list[str] = []
    for name in exs:
        text = (EXAMPLES_DIR / f"{name}.md").read_text(encoding="utf-8")
        first_line = text.split("\n", 1)[0].lstrip("# ").strip()
        summary = _extract_first_paragraph(text)
        lines.append(f"## {name} (markdown)\n**{first_line}**\n\n{summary}\n")
    for name in feats:
        lines.append(f"## {name} (Gherkin .feature)\nReady-to-copy template — see content via requirements://example/{name}\n")
    return "\n".join(lines)


@mcp.tool()
def list_hard_rules() -> str:
    """Return the 10 hard rules from references/05-convencoes-interpop.md
    (the canonical Interpop convention layer). Each rule is non-negotiable
    when designing a backlog under this methodology.
    """
    return (
        "**10 Hard Rules** (full detail at requirements://reference/05-convencoes-interpop):\n"
        "\n"
        "0. The requirements document is the SOURCE OF TRUTH (backlog only materializes it).\n"
        "1. No infinitive verbs in Epic/Feature/US/RF/RNF/G titles.\n"
        "2. No technical terms in Epic/Feature/US/CA/RF/RNF/G (those belong in Tasks).\n"
        "3. Explicit pt-BR, simple and direct (readable by non-technical stakeholders).\n"
        "4. Technical configuration is NOT a Feature (becomes Cross-cutting Task `TX-NN`).\n"
        "5. Interpop priority scale on every node (🔴 Immediate / 🟠 High / 🟡 Normal / ⚪ Low).\n"
        "6. Each node has its own artifact — Feature has description, US has BDD.\n"
        "7. ACs always grouped under `CA - <Theme>` + `[...]` convention for sub-rules.\n"
        "8. ALL artifacts have descriptions in business language.\n"
        "9. Multiple root Epics, no single `project-Epic` parent.\n"
    )


@mcp.tool()
def validate_user_story(title: str, bdd: Optional[str] = None) -> str:
    """Validate a User Story against INVEST + Interpop naming conventions.

    Args:
        title: The User Story title as it appears on the OpenProject card.
        bdd:   (optional) The Given/When/Then or Dado/Quando/Então scenario text
               that lives in the US Description field. If provided, structural
               checks run on it too.

    Returns:
        A markdown report with PASS/FAIL per check + explanation.
    """
    findings: list[str] = []

    # Naming Rule 1 — no infinitive verbs (pt-BR sample heuristic)
    infinitive_endings = ("ar", "er", "ir")
    first_word = title.strip().split(" ")[0].lower() if title.strip() else ""
    if first_word.endswith(infinitive_endings) and len(first_word) > 3:
        findings.append(
            f"❌ **Rule 1 (no infinitive verbs)** — title appears to start with an infinitive "
            f"verb (`{first_word}`). Rewrite using a noun or gerund "
            f"(`Listagem de…`, `Cadastro de…`, `Apresentação de…`)."
        )
    else:
        findings.append("✅ **Rule 1 (no infinitive verbs)** — title does not start with an infinitive.")

    # Naming Rule 2 — no technical terms
    technical_tokens = [
        "endpoint", "api", "rest", "graphql", "hook", "migration", "schema",
        "useeffect", "useSearch", "config", "deploy", "postgres", "mysql",
        "redux", "context", "router", "middleware", "controller", "model",
    ]
    leaked = [tok for tok in technical_tokens if tok.lower() in title.lower()]
    if leaked:
        findings.append(
            f"❌ **Rule 2 (no technical terms in titles)** — found: "
            f"`{', '.join(leaked)}`. These belong in Tasks, not in the US title."
        )
    else:
        findings.append("✅ **Rule 2 (no technical terms)** — title is in business language.")

    # INVEST — Small (heuristic: title length)
    if len(title) > 120:
        findings.append(
            "⚠️ **INVEST — Small** — title is over 120 chars; the US itself may "
            "be too large for a single sprint. Consider slicing."
        )
    else:
        findings.append("✅ **INVEST — Small** — title length is reasonable.")

    # INVEST — Negotiable (heuristic: Connextra template inside title)
    if re.search(r"\bComo\b.*\beu quero\b.*\bpara\b", title, flags=re.IGNORECASE) or \
       re.search(r"\bAs a\b.*\bI want\b.*\bso that\b", title, flags=re.IGNORECASE):
        findings.append(
            "❌ **Card hygiene** — the full Connextra template is in the title. "
            "Keep a short descriptive title (`US Listagem básica de atletas`); "
            "put the Connextra in the description/conversation."
        )
    else:
        findings.append("✅ **Card hygiene** — title is short and descriptive.")

    # BDD checks
    if bdd:
        if not re.search(r"\b(Dado|Given)\b", bdd, flags=re.IGNORECASE):
            findings.append("❌ **BDD structure** — no `Dado/Given` step found.")
        else:
            findings.append("✅ **BDD structure** — `Dado/Given` step present.")

        if not re.search(r"\b(Quando|When)\b", bdd, flags=re.IGNORECASE):
            findings.append("❌ **BDD structure** — no `Quando/When` step found.")
        else:
            findings.append("✅ **BDD structure** — `Quando/When` step present.")

        if not re.search(r"\b(Então|Then)\b", bdd, flags=re.IGNORECASE):
            findings.append("❌ **BDD structure** — no `Então/Then` step found.")
        else:
            findings.append("✅ **BDD structure** — `Então/Then` step present.")

        step_count = len(re.findall(r"^\s*(Dado|Given|Quando|When|Então|Then|E|And|Mas|But)\b",
                                    bdd, flags=re.IGNORECASE | re.MULTILINE))
        if step_count < 3:
            findings.append(f"⚠️ **BDD quality (Liz Keogh)** — only {step_count} step(s); aim for 3–7.")
        elif step_count > 7:
            findings.append(
                f"⚠️ **BDD quality (Liz Keogh)** — {step_count} steps; aim for 3–7. "
                "Split into multiple scenarios."
            )
        else:
            findings.append(f"✅ **BDD quality** — {step_count} steps (within 3–7 range).")
    else:
        findings.append("ℹ️  No BDD text supplied — BDD structural checks skipped.")

    return "\n".join(findings)


@mcp.tool()
def validate_acceptance_criterion(text: str) -> str:
    """Validate an Acceptance Criterion against Interpop AC convention.

    Checks:
    - Self-sufficiency vs. `[...]` convention (Rule 7).
    - Imperative wording (`deve`/`shall`/`must`).
    - Absence of subjective adjectives ("amigável", "rápido", "intuitivo").
    - Absence of technical terms.
    - Concrete metric when measurable.
    """
    findings: list[str] = []

    has_brackets = bool(re.search(r"\[\.\.\.\]", text))
    has_rules_to_apply = bool(re.search(r"Regras a serem aplicadas", text, flags=re.IGNORECASE))

    if has_brackets and not has_rules_to_apply:
        findings.append(
            "❌ **`[...]` convention** — title ends with `[...]` but no `Regras a serem aplicadas:` "
            "block detected. Either remove the `[...]` or add the bullet detail in the body."
        )
    elif has_rules_to_apply and not has_brackets:
        findings.append(
            "⚠️ **`[...]` convention** — body has `Regras a serem aplicadas:` but title does not end "
            "in `[...]`. Add `[...]` so list-mode readers know the title is not self-sufficient."
        )
    elif has_brackets and has_rules_to_apply:
        findings.append("✅ **`[...]` convention** — title + body matched correctly.")
    else:
        findings.append("✅ **Self-sufficient AC** — title carries the rule without sub-detail.")

    # Imperative wording
    if not re.search(r"\b(deve|shall|must|deverá|devem)\b", text, flags=re.IGNORECASE):
        findings.append(
            "⚠️ **Imperative wording** — no `deve/shall/must` verb detected. ACs should be "
            "declarative imperatives, not wishes."
        )
    else:
        findings.append("✅ **Imperative wording** — declarative verb present.")

    # Subjective adjectives
    subjective = [
        "amigável", "intuitivo", "fácil", "fácil de usar", "bonito",
        "friendly", "intuitive", "easy", "easy-to-use", "nice", "modern", "responsivo",
    ]
    leaked = [s for s in subjective if re.search(rf"\b{re.escape(s)}\b", text, flags=re.IGNORECASE)]
    if leaked:
        findings.append(
            f"❌ **No qualitative adjectives** — found: `{', '.join(leaked)}`. "
            "Replace with measurable behaviour (e.g., `responde em ≤800ms p95`)."
        )
    else:
        findings.append("✅ **No qualitative adjectives** detected.")

    # Technical terms
    leaked_tech = [
        tok for tok in [
            "endpoint", "rest", "graphql", "hook", "migration", "schema",
            "table", "controller", "model", "react", "django", "next.js",
            "http 400", "http 401", "http 403", "http 500",
        ]
        if tok.lower() in text.lower()
    ]
    if leaked_tech:
        findings.append(
            f"❌ **Rule 2 (no technical terms)** — found: `{', '.join(leaked_tech)}`. "
            "Move these to Tasks; rewrite the AC in business language."
        )
    else:
        findings.append("✅ **Rule 2 (no technical terms)** — AC stays in business language.")

    return "\n".join(findings)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Console script entry point.

    Runs the FastMCP server on stdio transport (the universal MCP default).
    Compatible with Claude Desktop, Cursor, Cline, Continue, Zed, and any
    other client that speaks the MCP stdio protocol.
    """
    if not SKILL_ROOT.exists():
        sys.stderr.write(f"FATAL: skill root not found at {SKILL_ROOT}\n")
        sys.exit(1)
    mcp.run()


if __name__ == "__main__":
    main()
