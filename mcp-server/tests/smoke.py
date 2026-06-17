"""Smoke test for the MCP server.

Runs the same checks the CI `mcp-smoke` job runs, but as a real script with
detailed prints — easier to debug than a bash heredoc when the environment
behaves differently from local. Exits with a non-zero status on any failure.

Usage::

    uv run python tests/smoke.py
"""

from __future__ import annotations

import sys

from requirements_engineering_mcp.server import (
    EXAMPLES_DIR,
    REFERENCES_DIR,
    SKILL_MD,
    SKILL_ROOT,
    check_projection_drift,
    list_examples,
    list_hard_rules,
    list_references,
    mcp,
    validate_acceptance_criterion,
    validate_user_story,
)


def main() -> int:
    failed: list[str] = []

    def check(name: str, ok: bool, observed: object = None) -> None:
        prefix = "PASS" if ok else "FAIL"
        print(f"  [{prefix}] {name}", end="")
        if observed is not None and not ok:
            print(f"  observed={observed!r}")
        else:
            print()
        if not ok:
            failed.append(name)

    print("=== Layout discovery ===")
    print(f"  SKILL_ROOT       = {SKILL_ROOT}")
    print(f"  SKILL_MD         = {SKILL_MD}")
    print(f"  REFERENCES_DIR   = {REFERENCES_DIR}")
    print(f"  EXAMPLES_DIR     = {EXAMPLES_DIR}")
    print()

    print("=== Identity ===")
    check("mcp.name == 'engenharia-de-requisitos'",
          mcp.name == "engenharia-de-requisitos",
          mcp.name)
    check("SKILL_ROOT exists", SKILL_ROOT.exists(), SKILL_ROOT)
    check("SKILL_MD exists", SKILL_MD.exists(), SKILL_MD)
    print()

    print("=== Corpus discovery ===")
    refs = sorted(p.name for p in REFERENCES_DIR.rglob("*.md") if p.name != "README.md") if REFERENCES_DIR.exists() else []
    exs_md = sorted(p.name for p in EXAMPLES_DIR.glob("*.md")) if EXAMPLES_DIR.exists() else []
    exs_ft = sorted(p.name for p in EXAMPLES_DIR.glob("*.feature")) if EXAMPLES_DIR.exists() else []
    print(f"  references/.md   = {len(refs)} → {refs}")
    print(f"  examples/.md     = {len(exs_md)} → {exs_md}")
    print(f"  examples/.feat   = {len(exs_ft)} → {exs_ft}")
    check("references count == 15", len(refs) == 15, len(refs))
    check("examples count (md + feature) == 8", len(exs_md) + len(exs_ft) == 8, len(exs_md) + len(exs_ft))
    print()

    print("=== Tool outputs ===")
    refs_out = list_references()
    exs_out = list_examples()
    rules_out = list_hard_rules()
    print(f"  list_references()  → {len(refs_out)} chars, first 80: {refs_out[:80]!r}")
    print(f"  list_examples()    → {len(exs_out)} chars, first 80: {exs_out[:80]!r}")
    print(f"  list_hard_rules()  → {len(rules_out)} chars, first 80: {rules_out[:80]!r}")
    check("list_references() is non-empty str", isinstance(refs_out, str) and len(refs_out) > 0)
    check("list_examples() is non-empty str", isinstance(exs_out, str) and len(exs_out) > 0)
    check("list_hard_rules() is non-empty str", isinstance(rules_out, str) and len(rules_out) > 0)
    check("list_references() mentions '01-fundamentos'", "01-fundamentos" in refs_out.lower())
    check("list_references() mentions 'requirements engineering'",
          "requirements engineering" in refs_out.lower())
    check("list_examples() mentions 'caso-controle-dopagem'",
          "caso-controle-dopagem" in exs_out.lower())
    check("list_examples() mentions 'worked example'",
          "worked example" in exs_out.lower())
    check("list_hard_rules() mentions 'hard rules'", "hard rules" in rules_out.lower())
    check("list_hard_rules() mentions 'source of truth'",
          "source of truth" in rules_out.lower())
    print()

    print("=== Validators run without raising ===")
    try:
        vus = validate_user_story("Listagem de reservas do usuário")
        check("validate_user_story returns str", isinstance(vus, str) and len(vus) > 0)
    except Exception as exc:  # noqa: BLE001
        check(f"validate_user_story did not raise (got {type(exc).__name__}: {exc})", False)

    try:
        vac = validate_acceptance_criterion("O sistema deve responder em ≤800ms (p95).")
        check("validate_acceptance_criterion returns str", isinstance(vac, str) and len(vac) > 0)
    except Exception as exc:  # noqa: BLE001
        check(f"validate_acceptance_criterion did not raise (got {type(exc).__name__}: {exc})", False)

    try:
        drift = check_projection_drift("___nonexistent_req___", "___nonexistent_proj___")
        check(
            "check_projection_drift returns advisory dict (ok=False on missing dir)",
            isinstance(drift, dict) and drift.get("ok") is False and "summary" in drift,
        )
    except Exception as exc:  # noqa: BLE001
        check(f"check_projection_drift did not raise (got {type(exc).__name__}: {exc})", False)
    print()

    print("=== Load-bearing skill invariants (behavioral guardrails — see tests/skill-behavior-scenarios.md) ===")
    # These assert that the load-bearing discipline machinery still EXISTS in SKILL.md.
    # Each maps to a RED-GREEN pressure scenario; deleting a guardrail (which would let an
    # agent rationalize past it) flips the check red here, in CI, before it ships.
    skill_text = SKILL_MD.read_text(encoding="utf-8").lower()
    invariants = {
        "S1 — §0 first-action structure check is MANDATORY":
            "first action" in skill_text and "mandatory" in skill_text,
        "S1/S7 — rule zero: requirements doc is the source of truth":
            "source of truth" in skill_text,
        "S2 — Feature=description vs User Story=BDD distinction":
            "user story" in skill_text and "bdd" in skill_text,
        "S3 — technical config is a cross-cutting Task (TX-NN), not a Feature":
            "tx-" in skill_text,
        "S4 — Feature atomicity (one Feature = one thing)":
            "atomicity" in skill_text,
        "S5 — NFR must be quantitative":
            "quantitative" in skill_text,
        "S6 — progressive refinement / the backlog iceberg":
            "iceberg" in skill_text,
        "anti-patterns catalogue is present":
            "anti-pattern" in skill_text,
        "points to the canonical hard rules in references/05":
            "05-convencoes-interpop" in skill_text,
    }
    for name, ok in invariants.items():
        check(name, ok)
    print()

    if failed:
        print(f"=== ❌ {len(failed)} check(s) failed ===")
        for name in failed:
            print(f"  - {name}")
        return 1

    print("=== ✅ all checks passed ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
