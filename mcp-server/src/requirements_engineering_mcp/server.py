"""FastMCP server exposing the engenharia-de-requisitos skill corpus.

Layout assumption: this module ships inside `mcp-server/` at the root of
the `sk-requirements-engineering` repository. The skill content lives
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
- list_hard_rules()                     → the Interpop hard-rules titles
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

import subprocess

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


def _list_refs() -> list[str]:
    """Reference doc stems, scanned recursively under references/ (so
    references/integrations/*.md is exposed too), excluding README indexes."""
    if not REFERENCES_DIR.exists():
        return []
    return sorted(p.stem for p in REFERENCES_DIR.rglob("*.md") if p.name != "README.md")


def _ref_path(name: str) -> Path:
    """Resolve a reference by stem anywhere under references/ (excl. README index)."""
    for p in REFERENCES_DIR.rglob(f"{name}.md"):
        if p.name != "README.md":
            return p
    return REFERENCES_DIR / f"{name}.md"  # fallback (404s in _read_or_error)


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
    """A specific reference file from references/<name>.md (en-CA), resolved
    recursively so references/integrations/<name>.md works too."""
    return _read_or_error(_ref_path(name))


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
    refs = _list_refs()
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
    refs = _list_refs()
    if not refs:
        return "(references/ directory is empty or missing)"

    lines: list[str] = []
    for name in refs:
        text = _ref_path(name).read_text(encoding="utf-8")
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
    """Return the hard rules from references/05-convencoes-interpop.md
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

    # EARS hint (optional precision layer — reference 11)
    if not re.search(r"\b(shall|deve|when|while|if|where|quando|enquanto|se|onde)\b", text, flags=re.IGNORECASE):
        findings.append(
            "💡 **EARS (optional)** — for an unambiguous, AI-parseable phrasing, consider EARS in the "
            "requirement body (`WHEN/QUANDO … THE SYSTEM SHALL/O SISTEMA DEVE …`). Run `validate_ears(text)`."
        )

    return "\n".join(findings)


@mcp.tool()
def validate_ears(text: str) -> str:
    """Validate an EARS statement (reference 11 — optional precision layer).

    EARS (Easy Approach to Requirements Syntax) phrases a requirement as one of five
    templates around a single obligation keyword `SHALL` (EN) / `DEVE` (pt-BR):
      - Ubiquitous:      THE SYSTEM SHALL / O SISTEMA DEVE ...
      - Event-driven:    WHEN/QUANDO <trigger> THE SYSTEM SHALL/O SISTEMA DEVE ...
      - State-driven:    WHILE/ENQUANTO <state> ...
      - Unwanted:        IF/SE <condition> THEN/ENTÃO ...
      - Optional:        WHERE/ONDE <feature> ...

    Advisory only — EARS is opt-in and coexists with business-language `RF` + BDD.
    Checks: exactly one obligation keyword, no weak modals, no subjective adjectives,
    an EARS structural keyword is present, and EARS keywords do not leak into a title.
    """
    findings: list[str] = []
    lowered = text.lower()

    # 1) Exactly one obligation keyword (SHALL / DEVE)
    obligations = re.findall(r"\b(shall|deve|deverá|devem)\b", text, flags=re.IGNORECASE)
    if len(obligations) == 0:
        findings.append(
            "❌ **Obligation keyword** — no `SHALL`/`DEVE` found. An EARS statement needs exactly "
            "one obligation keyword (`THE SYSTEM SHALL …` / `O SISTEMA DEVE …`)."
        )
    elif len(obligations) > 1:
        findings.append(
            f"❌ **One behaviour per statement** — found {len(obligations)} obligation keywords "
            f"(`{', '.join(o.lower() for o in obligations)}`). Two `SHALL`/`DEVE` = two requirements; split them."
        )
    else:
        findings.append("✅ **Obligation keyword** — exactly one `SHALL`/`DEVE`.")

    # 2) Weak modals instead of SHALL/DEVE
    weak = [w for w in ["should", "must", "will", "deveria", "poderá", "pode", "irá", "vai"]
            if re.search(rf"\b{re.escape(w)}\b", text, flags=re.IGNORECASE)]
    if weak:
        findings.append(
            f"⚠️ **Weak modal** — found `{', '.join(weak)}`. EARS uses the obligation `SHALL`/`DEVE`, "
            "never `should/must/will` / `deveria/pode/irá`."
        )
    else:
        findings.append("✅ **No weak modals**.")

    # 3) Subjective / non-measurable response
    subjective = [
        "amigável", "intuitivo", "fácil", "bonito", "rápido", "rapidamente",
        "friendly", "intuitive", "easy", "nice", "fast", "modern", "responsivo",
    ]
    leaked = [s for s in subjective if re.search(rf"\b{re.escape(s)}\b", lowered)]
    if leaked:
        findings.append(
            f"❌ **Measurable response** — found subjective term(s): `{', '.join(leaked)}`. "
            "The response after `SHALL`/`DEVE` must be an observable, measurable outcome."
        )
    else:
        findings.append("✅ **Measurable response** — no subjective adjectives.")

    # 4) An EARS structural keyword is present (else it may just be prose)
    structural = re.search(
        r"\b(when|while|if|then|where|the system|quando|enquanto|se|então|onde|o sistema)\b",
        text, flags=re.IGNORECASE,
    )
    if structural:
        findings.append("✅ **EARS structure** — a recognized keyword is present.")
    else:
        findings.append(
            "⚠️ **EARS structure** — no `WHEN/WHILE/IF/WHERE/THE SYSTEM` (or `QUANDO/ENQUANTO/SE/ONDE/"
            "O SISTEMA`) keyword detected. If this is event/state/error behaviour, add the trigger clause."
        )

    # 5) EARS keywords must not land in a business title (heuristic: a short single line in a title-like form)
    if re.match(r"^\s*(RF|RNF)[- ]?\d", text, flags=re.IGNORECASE) and structural and len(text.splitlines()) == 1:
        findings.append(
            "ℹ️ **Reminder** — EARS belongs in the requirement **body**, never in the business-language "
            "title (naming rule 2). Keep the catalog title jargon-free."
        )

    return "\n".join(findings)


# ---------------------------------------------------------------------------
# check_projection_drift — advisory drift report between docs/requirements and
# its SDD projection (OpenSpec / Spec Kit). See references/integrations/sdd-interop.md §5.
# ---------------------------------------------------------------------------

_RF_RE = re.compile(r"\b(RF|RNF)-?(\d{1,3})\b", re.IGNORECASE)
# CANN / CA-NN / CANN.M (sub optional). Normalized to the skill's `CANN` (no hyphen).
_CA_RE = re.compile(r"\bCA-?(\d{1,3})(?:\.(\d{1,3}))?\b", re.IGNORECASE)
# Weak modals signalling lost EARS phrasing. NOTE: pt-BR `DEVE` is the EARS
# OBLIGATION (see _SHALL_RE), NOT weak — deliberately excluded; pt-BR weakness
# is `deveria/pode/poderá/irá/vai`.
_WEAK_MODAL_RE = re.compile(
    r"\b(should|must|will|is able to|deveria|poder[áa]|pode|ir[áa]|vai)\b", re.IGNORECASE
)
_SHALL_RE = re.compile(r"\b(SHALL|DEVE)\b")
_SPEC_GLOBS = ("spec.md", "*.spec.md", "specs/**/*.md", "**/spec.md")


def _norm_rf(kind: str, number: str) -> str:
    """Normalize 'rf21' / 'RF-21' -> 'RF-21'."""
    return f"{kind.upper()}-{int(number):02d}"


def _norm_ca(nn: str, m: Optional[str]) -> str:
    """Normalize to the skill's `CANN` convention (no hyphen): 'CA-02.1' -> 'CA02.1'."""
    base = f"CA{int(nn):02d}"
    return f"{base}.{int(m)}" if m else base


def _collect_ids_from_text(text: str) -> tuple[set[str], set[str]]:
    rf = {_norm_rf(k, n) for k, n in _RF_RE.findall(text)}
    ca = {_norm_ca(nn, m or None) for nn, m in _CA_RE.findall(text)}
    return rf, ca


def _iter_md_files(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    seen: set[Path] = set()
    for pat in patterns:
        for f in root.glob(pat):
            if f.is_file() and f.suffix == ".md":
                seen.add(f.resolve())
    return sorted(seen)


def _check_projection_drift(
    requirements_dir: str = "docs/requirements",
    projection_dir: str = "openspec",
) -> dict:
    """Advisory report: drift between the requirement source of truth and its SDD projection.

    Implements references/integrations/sdd-interop.md §5. Never raises on a "fail" — returns
    a structured report the agent (or a CI job) reads. Tag-based (anchored on
    RF-NN), stdlib-only, EN+pt-BR aware.
    """
    req_root = Path(requirements_dir)
    proj_root = Path(projection_dir)

    report: dict = {
        "requirements_dir": str(req_root),
        "projection_dir": str(proj_root),
        "ok": True,
        "summary": "",
        "findings": {
            "missing_in_projection": [],      # RF/RNF in docs/ absent from specs
            "duplicated_in_projection": [],   # RF/RNF tag in >1 spec file (should be exactly one)
            "orphan_in_projection": [],       # spec requirement lines w/o RF tag
            "ca_without_scenario": [],        # CA ids present but NO scenario block at all (coarse)
            "ears_weakened": [],              # weak-modal / no-SHALL req lines
        },
        "counts": {},
        "notes": [],
    }

    if not req_root.exists():
        report["ok"] = False
        report["summary"] = f"requirements_dir not found: {req_root}"
        return report
    if not proj_root.exists():
        report["ok"] = False
        report["summary"] = f"projection_dir not found: {proj_root}"
        return report

    # 1. Source-of-truth ids
    req_files = _iter_md_files(req_root, ("**/*.md",))
    src_rf: set[str] = set()
    src_ca: set[str] = set()
    for f in req_files:
        rf, ca = _collect_ids_from_text(f.read_text(encoding="utf-8", errors="replace"))
        src_rf |= rf
        src_ca |= ca

    # 2. Projection ids (+ per-file RF counts for duplication) + line-level signals
    spec_files = _iter_md_files(proj_root, _SPEC_GLOBS) or _iter_md_files(proj_root, ("**/*.md",))
    proj_rf: set[str] = set()
    rf_file_count: dict[str, int] = {}
    has_scenario = False
    for f in spec_files:
        text = f.read_text(encoding="utf-8", errors="replace")
        rf, _ = _collect_ids_from_text(text)
        proj_rf |= rf
        for tag in rf:
            rf_file_count[tag] = rf_file_count.get(tag, 0) + 1
        if re.search(r"^\s*(Scenario|Cenário|Scenarios?)\b", text, re.IGNORECASE | re.MULTILINE):
            has_scenario = True

        for ln, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ">", "|", "```")):
                continue
            has_shall = bool(_SHALL_RE.search(stripped))
            has_weak = bool(_WEAK_MODAL_RE.search(stripped))
            has_rf = bool(_RF_RE.search(stripped))
            mentions_system = bool(re.search(r"\b(the system|o sistema)\b", stripped, re.IGNORECASE))
            looks_req = has_shall or (has_weak and mentions_system) or has_rf
            if looks_req and not has_rf:
                report["findings"]["orphan_in_projection"].append(
                    {"file": str(f), "line": ln, "text": stripped[:160]}
                )
            if looks_req and has_weak and not has_shall:
                report["findings"]["ears_weakened"].append(
                    {"file": str(f), "line": ln, "text": stripped[:160]}
                )

    # 3. Reconcile
    fnd = report["findings"]
    fnd["missing_in_projection"] = sorted(src_rf - proj_rf)
    fnd["duplicated_in_projection"] = sorted(t for t, c in rf_file_count.items() if c > 1)
    if src_ca and not has_scenario:
        fnd["ca_without_scenario"] = sorted(src_ca)

    report["counts"] = {
        "requirements_files": len(req_files),
        "projection_spec_files": len(spec_files),
        "rf_in_source": len(src_rf),
        "rf_in_projection": len(proj_rf),
        "ca_in_source": len(src_ca),
        "missing": len(fnd["missing_in_projection"]),
        "duplicated": len(fnd["duplicated_in_projection"]),
        "orphans": len(fnd["orphan_in_projection"]),
        "ears_weakened": len(fnd["ears_weakened"]),
    }

    problems = (
        len(fnd["missing_in_projection"])
        + len(fnd["duplicated_in_projection"])
        + len(fnd["orphan_in_projection"])
        + len(fnd["ca_without_scenario"])
        + len(fnd["ears_weakened"])
    )
    report["ok"] = problems == 0
    if not spec_files:
        report["notes"].append("No projection spec files found — is the framework folder populated?")
    if report["ok"]:
        report["summary"] = f"In sync: {len(src_rf)} RF/RNF projected, {len(src_ca)} CA, no drift detected."
    else:
        bits: list[str] = []
        if fnd["missing_in_projection"]:
            bits.append(f"{len(fnd['missing_in_projection'])} missing from projection")
        if fnd["duplicated_in_projection"]:
            bits.append(f"{len(fnd['duplicated_in_projection'])} duplicated across specs")
        if fnd["orphan_in_projection"]:
            bits.append(f"{len(fnd['orphan_in_projection'])} orphan line(s)")
        if fnd["ca_without_scenario"]:
            bits.append("CA ids without any scenario block")
        if fnd["ears_weakened"]:
            bits.append(f"{len(fnd['ears_weakened'])} weak-modal line(s)")
        report["summary"] = "Drift detected: " + "; ".join(bits) + "."
    return report


@mcp.tool()
def check_projection_drift(
    requirements_dir: str = "docs/requirements",
    projection_dir: str = "openspec",
) -> dict:
    """Report drift between docs/requirements (source of truth) and its SDD projection.

    Advisory (never blocks). Compares RF/RNF/CA tags between the skill's
    `docs/requirements` spine and an OpenSpec (`openspec/`) or Spec Kit (`specs/`)
    projection. Findings: missing_in_projection, duplicated_in_projection,
    orphan_in_projection, ca_without_scenario (coarse/global), ears_weakened.
    EN + pt-BR (`SHALL`/`DEVE`). See references/integrations/sdd-interop.md §5.
    """
    return _check_projection_drift(requirements_dir, projection_dir)


# ---------------------------------------------------------------------------
# Generative tools — the imperative layer (create / close). Wrap the shell
# generators assets/new-item.sh + assets/gen-done-view.sh so an agent can ACT
# (allocate an id, instantiate a template, close an item) instead of only
# reading advice. This is what turns "create a spike when you can't estimate"
# from a manual chore into a single call.
# ---------------------------------------------------------------------------

NEW_ITEM_SH = SKILL_ROOT / "assets" / "new-item.sh"
GEN_DONE_SH = SKILL_ROOT / "assets" / "gen-done-view.sh"
_ITEM_KINDS = (
    "spike", "bug", "issue", "qa", "tx", "epic", "feature",
    "rf", "rnf", "pm", "runbook", "adr", "sprint",
)


def _run(cmd: list[str]) -> dict:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {"ok": p.returncode == 0, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except Exception as exc:  # noqa: BLE001 — surface any failure as data, never crash the server
        return {"ok": False, "stdout": "", "stderr": f"{type(exc).__name__}: {exc}"}


@mcp.tool()
def create_item(
    kind: str,
    slug: str,
    project_root: str = "docs",
    title: str = "",
    apply: bool = False,
) -> dict:
    """Create a backlog/requirements artifact with the next free ID (the generative layer).

    `kind` ∈ spike|bug|issue|qa|tx|epic|feature|rf|rnf|pm|runbook|adr|sprint. Allocates the next
    free ID (ADR scans BOTH tiers for the one global sequence), instantiates the correct
    `_TEMPLATE.md`, places it in the right bucket, and fills id/slug/date. `apply=False` → dry-run
    (returns the resolved id + destination path). Call this the moment the skill says "create a
    spike/bug/issue/…" instead of hand-copying a template. Wraps `assets/new-item.sh`.
    """
    if kind not in _ITEM_KINDS:
        return {"ok": False, "stdout": "", "stderr": f"unknown kind '{kind}' — one of: {', '.join(_ITEM_KINDS)}"}
    cmd = ["bash", str(NEW_ITEM_SH), kind, slug, "--root", project_root]
    if title:
        cmd += ["--title", title]
    if apply:
        cmd += ["--apply"]
    return _run(cmd)


@mcp.tool()
def generate_done_view(project_root: str = "docs", apply: bool = False) -> dict:
    """Regenerate the Status-driven DONE VIEW (`<root>/backlog/done/README.md`).

    Scans the backlog for items whose Status is ✅ Done and writes a read-only ledger
    (Kind · ID · Title · Where). Items are NOT moved — they keep their Status in place, so every
    ↑/↓ link keeps resolving. `apply=False` → prints the view without writing. Wraps
    `assets/gen-done-view.sh`.
    """
    cmd = ["bash", str(GEN_DONE_SH), "--root", project_root]
    if apply:
        cmd += ["--apply"]
    return _run(cmd)


@mcp.tool()
def close_item(item_file: str, project_root: str = "docs", apply: bool = False) -> dict:
    """Close a backlog item: set its Status to ✅ Done IN PLACE (no move) + regenerate the done view.

    `item_file` = path to the artifact (e.g. `docs/backlog/features/F-30-....md`). On `apply` it
    rewrites the item's single `**Status**` line to `✅ Done` and regenerates the done ledger. The
    file never leaves its bucket. `apply=False` → reports what it would do without writing.
    """
    path = Path(item_file)
    if not path.exists():
        return {"ok": False, "stdout": "", "stderr": f"not found: {item_file}"}
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = False
    for i, ln in enumerate(lines):
        if "**Status**" in ln:
            lines[i] = re.sub(r"(\*\*Status\*\*\s*:).*", r"\1 ✅ Done", ln)
            changed = True
            break
    if not apply:
        return {"ok": True, "stdout": f"would set **Status**: ✅ Done in {item_file} and regenerate the done view",
                "stderr": "" if changed else "warning: no **Status** line found"}
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    dv = _run(["bash", str(GEN_DONE_SH), "--root", project_root, "--apply"])
    return {"ok": dv["ok"], "stdout": f"Status set in {item_file}; {dv['stdout']}", "stderr": dv["stderr"]}


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
