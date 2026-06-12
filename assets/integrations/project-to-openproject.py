#!/usr/bin/env python3
"""project-to-openproject.py — project the docs/backlog/ spine into an OpenProject-importable
work-package table (Type / ID / Subject / Priority) for the OpenProject "Excel synchronization".

Design (see references/integrations/openproject.md):
  - Only docs/backlog/ matters — Epics, Features, User Stories are the work packages.
    The requirements/ side is NOT exported (it is the *why*, not a backlog item).
  - Our stable id (EP-NN / F-NN / USNN.M) goes INTO the Subject ("<id> <business title>",
    exactly as it reads in the OpenProject UI). The OpenProject ID column is left BLANK so
    OpenProject assigns its own numeric id on import (their id != ours).
  - Priority maps the Interpop scale to OpenProject's default priorities:
        🔴 -> Immediate · 🟠 -> High · 🟡 -> Normal · 🟢 -> Low

Usage:
  project-to-openproject.py [--root docs] [--with-tasks] [--out-dir openproject] [--apply]

Safety: DRY-RUN by default (prints the table, writes nothing). --apply writes
  <out-dir>/openproject-backlog.csv   (always — stdlib only)
  <out-dir>/openproject-backlog.xlsx  (only if `openpyxl` is installed)
Never overwrites an existing file (skips + warns). This is the default skill format;
the user can always adapt the columns/types to their OpenProject configuration.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

COLUMNS = ["Type", "ID", "Subject", "Priority"]

_PRIO_EMOJI = {"🔴": "Immediate", "🟠": "High", "🟡": "Normal", "🟢": "Low"}
_PRIO_WORD = {
    "imediata": "Immediate", "immediate": "Immediate",
    "alta": "High", "high": "High",
    "normal": "Normal",
    "baixa": "Low", "low": "Low",
}
_EP_RE = re.compile(r"EP-?\d+(?:\.\d+)*", re.I)
_F_RE = re.compile(r"\bF-?\d+\b", re.I)
_US_RE = re.compile(r"US-?\d+\.\d+", re.I)
_T_RE = re.compile(r"\b(?:T-?\d+\.\d+\.\d+[a-z]?|TX-?\d+)\b", re.I)


def _norm(ident: str) -> str:
    """EP12 -> EP-12 ; F26 -> F-26 ; US25.2 -> US25.2 (US keeps no hyphen, per conventions)."""
    ident = ident.upper()
    if ident.startswith("US"):
        return ident  # USNN.M form (no hyphen)
    return re.sub(r"^(EP|TX|F|T)-?", lambda m: m.group(1) + "-", ident)


def _detect_priority(block: str) -> str:
    for emoji, name in _PRIO_EMOJI.items():
        if emoji in block:
            return name
    low = block.lower()
    m = re.search(r"(priorid\w*|priority)[^\n]*", low)
    scope = m.group(0) if m else ""
    for word, name in _PRIO_WORD.items():
        if re.search(r"\b" + re.escape(word) + r"\b", scope):
            return name
    return "Normal"


def _title(heading: str, ident: str) -> str:
    t = re.sub(r"^#{1,6}\s*", "", heading).strip()
    t = re.sub(r"^" + re.escape(ident) + r"\s*[—:\-]\s*", "", t, flags=re.I).strip()
    # also strip a non-normalized id prefix (e.g. "EP12 — ")
    t = re.sub(r"^(EP|F|US|T|TX)-?\d+(?:\.\d+)*\s*[—:\-]\s*", "", t, flags=re.I).strip()
    return t


def _subject(ident: str, title: str) -> str:
    return f"{ident} {title}".strip()


def _first_heading(text: str, level_prefix: str = "# ") -> str | None:
    for line in text.splitlines():
        if line.startswith(level_prefix):
            return line
    return None


def collect(root: Path, with_tasks: bool) -> list[dict]:
    backlog = root / "backlog"
    if not backlog.is_dir():
        sys.exit(f"error: no '{backlog}' — run from a project with the docs/ spine "
                 f"(assets/scaffold-structure.sh).")
    rows: list[dict] = []

    # --- Epics (epics/*.md) ---
    for f in sorted((backlog / "epics").glob("*.md")) if (backlog / "epics").is_dir() else []:
        if f.stem == "_TEMPLATE":
            continue
        text = f.read_text(encoding="utf-8")
        h1 = _first_heading(text) or f.stem
        m = _EP_RE.search(f.stem) or _EP_RE.search(h1)
        if not m:
            continue
        ident = _norm(m.group(0))
        rows.append({"Type": "Epic", "ID": "", "Subject": _subject(ident, _title(h1, ident)),
                     "Priority": _detect_priority(text[:800])})

    # --- Features (features/*.md), each followed by its User Stories (+ Tasks) ---
    for f in sorted((backlog / "features").glob("*.md")) if (backlog / "features").is_dir() else []:
        if f.stem == "_TEMPLATE":
            continue
        text = f.read_text(encoding="utf-8")
        h1 = _first_heading(text) or f.stem
        mf = _F_RE.search(f.stem) or _F_RE.search(h1)
        if not mf:
            continue
        fid = _norm(mf.group(0))
        rows.append({"Type": "Feature", "ID": "", "Subject": _subject(fid, _title(h1, fid)),
                     "Priority": _detect_priority(text[:800])})
        # User Stories: '### US-NN.M — title' (or any heading carrying a US id)
        for line in text.splitlines():
            if line.lstrip().startswith("#") and _US_RE.search(line):
                uid = _norm(_US_RE.search(line).group(0))
                rows.append({"Type": "User story", "ID": "",
                             "Subject": _subject(uid, _title(line, uid)), "Priority": "Normal"})
        if with_tasks:
            for tid in sorted({_norm(m.group(0)) for m in _T_RE.finditer(text)}):
                rows.append({"Type": "Task", "ID": "", "Subject": tid, "Priority": "Normal"})
    return rows


def write_outputs(rows: list[dict], out_dir: Path, apply: bool) -> None:
    csv_path = out_dir / "openproject-backlog.csv"
    xlsx_path = out_dir / "openproject-backlog.xlsx"

    if not apply:
        print(f"\n  PLAN  {csv_path}  ({len(rows)} work packages)")
        print(f"  PLAN  {xlsx_path}  (if openpyxl present)")
        print("\nDry-run — nothing written. Re-run with --apply.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    if csv_path.exists():
        print(f"  skip  {csv_path} (exists — not overwritten)")
    else:
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        print(f"  write {csv_path}")

    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ModuleNotFoundError:
        print("  note  openpyxl not installed — CSV only. `uv add openpyxl` (or pip) for .xlsx.")
        return
    if xlsx_path.exists():
        print(f"  skip  {xlsx_path} (exists — not overwritten)")
        return
    wb = Workbook()
    ws = wb.active
    ws.title = "Backlog"
    ws.append(COLUMNS)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append([r[c] for c in COLUMNS])
    for col, width in zip("ABCD", (14, 8, 80, 12)):
        ws.column_dimensions[col].width = width
    wb.save(xlsx_path)
    print(f"  write {xlsx_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Project docs/backlog/ into an OpenProject Type/ID/Subject/Priority table.")
    ap.add_argument("--root", default="docs", help="docs root (default: docs)")
    ap.add_argument("--out-dir", default="openproject", help="output dir (default: openproject)")
    ap.add_argument("--with-tasks", action="store_true", help="also emit T/TX tasks as work packages")
    ap.add_argument("--apply", action="store_true", help="write the files (default: dry-run)")
    args = ap.parse_args()

    rows = collect(Path(args.root), args.with_tasks)
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["Type"]] = counts.get(r["Type"], 0) + 1
    print("== project-to-openproject.py ==")
    print(f"root={args.root}/  out-dir={args.out_dir}/  with-tasks={args.with_tasks}  apply={args.apply}")
    print("work packages: " + (", ".join(f"{k}={v}" for k, v in counts.items()) or "(none found)"))
    print(f"columns: {' | '.join(COLUMNS)}   (ID blank → OpenProject assigns; our id lives in Subject)")
    write_outputs(rows, Path(args.out_dir), args.apply)


if __name__ == "__main__":
    main()
