#!/usr/bin/env python3
"""openproject-api.py — OpenProject REST API round-trip adapter (PRIMARY method).

Pulls and pushes the ``docs/backlog/`` spine straight to the OpenProject REST API
v3 — no spreadsheet, no macro. The OpenProject "Excel synchronization" ``.xlsm``
template only runs on **Windows** (it drives the API through ``winhttpcom.dll``);
this adapter runs natively on **Linux / macOS / Windows** with just the Python 3
standard library (``urllib`` + ``ssl``). See references/integrations/openproject.md.

This is the distilled, generalized core of a real OpenProject automation (the
*"SIRA"* project): HTTP Basic ``apikey:<token>`` auth, paginated pull, type/priority
lookup, ``lockVersion`` optimistic locking, parent hierarchy via real API links.

CONFIG — by environment (NEVER hard-code a token in a committed file):
  OPENPROJECT_URL         base URL, e.g. https://openproject.example.com (or host:port)
  OPENPROJECT_TOKEN       your API token (OpenProject → My account → Access tokens → API)
                          — OR put ``API_KEY=<token>`` in a ``.env`` file (keep it gitignored)
  OPENPROJECT_PROJECT     project identifier — the slug ("my-project") OR the numeric id (163)
  OPENPROJECT_VERIFY_SSL  "false" to skip TLS verification (self-signed / private server);
                          default "true". Only disable for a server you control and trust.

COMMANDS:
  pull   GET every work package of the project → <out-dir>/openproject_dump.json
         (the round-trip anchor: it carries each work package's OpenProject id +
         lockVersion, which the push needs to UPDATE instead of duplicate).
  push   project docs/backlog/ → CREATE/UPDATE work packages over the API
         (hierarchy via real parent links, descriptions, priority).

SAFETY:
  - push is DRY-RUN by default (prints the operation plan, writes nothing). --apply executes.
  - Idempotent: matches an existing work package by the "<our-id> " Subject prefix
    (EP-NN / F-NN / USNN.M) → UPDATE; otherwise CREATE. Run ``pull`` first so push can match.
  - Per-item error isolation: one failed work package does not abort the batch (--apply).
  - Optimistic locking: re-reads each work package's lockVersion immediately before PATCH,
    and retries once on a 409 conflict.
  - Retry with backoff on 429 / 5xx (honours Retry-After).

USAGE:
  # 1) authenticate by env (example for a private, self-signed server)
  export OPENPROJECT_URL=https://openproject.example.com
  export OPENPROJECT_TOKEN=xxxxxxxx            # or API_KEY=... in .env
  export OPENPROJECT_PROJECT=my-project        # slug or numeric id
  # export OPENPROJECT_VERIFY_SSL=false        # only for a self-signed cert you trust

  python3 assets/integrations/openproject-api.py pull
  python3 assets/integrations/openproject-api.py push                 # dry-run plan
  python3 assets/integrations/openproject-api.py push --apply         # execute
  python3 assets/integrations/openproject-api.py push --with-tasks --apply
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
_OUR_ID = re.compile(r"\b(EP-?\d+(?:\.\d+)*|F-?\d+|US-?\d+\.\d+|T-?\d+\.\d+\.\d+[a-z]?|TX-?\d+)\b", re.I)


# ─────────────────────────── config / auth ───────────────────────────

def _read_dotenv_token(root: Path) -> str | None:
    """Read API_KEY=<token> from a .env at the project root. Strips surrounding
    whitespace and quotes — a trailing space in the .env is a classic cause of a
    silent 401 (learned the hard way on the *"SIRA"* server)."""
    env = root / ".env"
    if not env.is_file():
        return None
    m = re.search(r"^\s*API_KEY\s*=\s*(.*)$", env.read_text(encoding="utf-8"), re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else None


def load_config(root: Path) -> tuple[str, str, str, bool]:
    url = (os.environ.get("OPENPROJECT_URL") or "").strip().rstrip("/")
    token = (os.environ.get("OPENPROJECT_TOKEN") or "").strip().strip("\"'") or _read_dotenv_token(root)
    project = (os.environ.get("OPENPROJECT_PROJECT") or "").strip()
    verify = (os.environ.get("OPENPROJECT_VERIFY_SSL", "true").strip().lower()
              not in {"false", "0", "no", "off"})
    missing = [n for n, v in (("OPENPROJECT_URL", url), ("OPENPROJECT_TOKEN", token),
                              ("OPENPROJECT_PROJECT", project)) if not v]
    if missing:
        sys.exit("error: missing config: " + ", ".join(missing)
                 + "\n  set them as environment variables (token may live in .env as API_KEY=...)."
                 + "\n  see the header of this file for the full list.")
    return url, token, project, verify


class Client:
    """Tiny OpenProject API v3 client (stdlib only) with retry/backoff + lockVersion helpers."""

    def __init__(self, base: str, token: str, verify_ssl: bool):
        self.base = base
        self._ctx = ssl.create_default_context()
        if not verify_ssl:
            self._ctx.check_hostname = False
            self._ctx.verify_mode = ssl.CERT_NONE  # self-signed / private server (trust-on-purpose)
        self._auth = base64.b64encode(f"apikey:{token}".encode()).decode()
        self._types: dict[str, str] | None = None
        self._priorities: dict[str, str] | None = None

    def api(self, method: str, path: str, body: dict | None = None, *, retries: int = 3) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        for attempt in range(retries + 1):
            req = urllib.request.Request(
                self.base + path, data=data, method=method,
                headers={"Authorization": f"Basic {self._auth}", "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, context=self._ctx, timeout=60) as r:
                    return json.load(r) if r.status != 204 else {}
            except urllib.error.HTTPError as ex:
                # 429 / 5xx → transient: back off and retry (honour Retry-After).
                if ex.code in (429, 500, 502, 503, 504) and attempt < retries:
                    wait = float(ex.headers.get("Retry-After", 2 ** attempt))
                    time.sleep(min(wait, 30))
                    continue
                detail = ex.read().decode(errors="replace")[:400]
                raise OpenProjectError(method, path, ex.code, detail) from None
            except urllib.error.URLError as ex:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise OpenProjectError(method, path, 0, str(ex.reason)) from None
        raise OpenProjectError(method, path, 0, "exhausted retries")

    # -- lookups (cached) --------------------------------------------------
    def types(self) -> dict[str, str]:
        """name → /api/v3/types/{id}. From the API (not a dump) so every configured
        type is present even if no work package uses it yet — this is exactly the
        ``KeyError: 'Task'`` bug the *"SIRA"* export hit and fixed."""
        if self._types is None:
            j = self.api("GET", "/api/v3/types")
            self._types = {t["name"]: f"/api/v3/types/{t['id']}" for t in j["_embedded"]["elements"]}
        return self._types

    def priorities(self) -> dict[str, str]:
        if self._priorities is None:
            j = self.api("GET", "/api/v3/priorities")
            self._priorities = {p["name"]: f"/api/v3/priorities/{p['id']}"
                                for p in j["_embedded"]["elements"]}
        return self._priorities

    # -- work packages -----------------------------------------------------
    def list_all(self, project: str) -> dict:
        elements, offset, total = [], 1, 0
        while True:
            page = self.api("GET", f"/api/v3/projects/{project}/work_packages"
                                   f"?pageSize=200&offset={offset}")
            total = page.get("total", 0)
            batch = page.get("_embedded", {}).get("elements", [])
            elements.extend(batch)
            if len(elements) >= total or not batch:
                break
            offset += 1
        return {"total": total, "elements": elements}

    def create(self, subject: str, type_href: str, project: str,
               parent_id: int | None = None, description: str = "",
               priority_href: str | None = None) -> dict:
        links = {"type": {"href": type_href}, "project": {"href": f"/api/v3/projects/{project}"}}
        if parent_id:
            links["parent"] = {"href": f"/api/v3/work_packages/{parent_id}"}
        if priority_href:
            links["priority"] = {"href": priority_href}
        body: dict = {"subject": subject, "_links": links}
        if description:
            body["description"] = {"raw": description}
        return self.api("POST", "/api/v3/work_packages", body)

    def patch(self, wp_id: int, fields: dict, *, lock: int | None = None) -> dict:
        """PATCH with a FRESH lockVersion (re-read right before write); 1 retry on 409."""
        if lock is None:
            lock = self.api("GET", f"/api/v3/work_packages/{wp_id}")["lockVersion"]
        body = {"lockVersion": lock, **fields}
        try:
            return self.api("PATCH", f"/api/v3/work_packages/{wp_id}", body)
        except OpenProjectError as ex:
            if ex.code == 409:  # someone edited between our GET and PATCH — re-read + retry once
                fresh = self.api("GET", f"/api/v3/work_packages/{wp_id}")["lockVersion"]
                return self.api("PATCH", f"/api/v3/work_packages/{wp_id}", {"lockVersion": fresh, **fields})
            raise


class OpenProjectError(RuntimeError):
    def __init__(self, method: str, path: str, code: int, detail: str):
        self.code = code
        super().__init__(f"HTTP {code} on {method} {path}: {detail}")


# ─────────────────────────── backlog → ops ───────────────────────────

def _load_parser():
    """Reuse the exact docs/backlog/ parser from the sibling Excel adapter (DRY).
    The module filename has hyphens, so load it by path."""
    spec = importlib.util.spec_from_file_location("p2op", HERE / "project-to-openproject.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _our_id(subject: str) -> str | None:
    m = _OUR_ID.search(subject or "")
    return m.group(0) if m else None


def _depth(subject_with_indent: str) -> int:
    return (len(subject_with_indent) - len(subject_with_indent.lstrip(" "))) // 4


def build_plan(rows: list[dict], existing: list[dict]) -> list[dict]:
    """Turn parsed backlog rows into ordered CREATE/UPDATE ops.

    Hierarchy: rows arrive in tree order (Epic→Feature→US→Task) with the Subject
    indented 4 spaces/level. The parent of a row is the most recent row one level
    shallower. Existing work packages are matched by their ``<our-id>`` Subject prefix.
    """
    op_by_ourid = {}  # our-id → existing OpenProject element (subject carries "<our-id> ...")
    for e in existing:
        oid = _our_id(e.get("subject", ""))
        if oid:
            op_by_ourid[_norm_id(oid)] = e

    plan: list[dict] = []
    stack: dict[int, str] = {}  # depth → our-id of the last row at that depth (its parent anchor)
    for r in rows:
        subj_indented = r["Subject"]
        depth = _depth(subj_indented)
        clean = re.sub(r"\s*[\U0001F534\U0001F7E0\U0001F7E1\U0001F7E2]\s*", " ",
                       subj_indented.strip()).strip()  # "<our-id> <title>" — NO indent, NO priority emoji
        oid = _norm_id(_our_id(clean) or clean)
        stack[depth] = oid
        parent_oid = stack.get(depth - 1) if depth > 0 else None
        existing_el = op_by_ourid.get(oid)
        plan.append({
            "our_id": oid,
            "type": r["Type"],
            "subject": clean,
            "priority": r.get("Priority") or "Normal",
            "description": r.get("Description") or "",
            "parent_our_id": parent_oid,
            "existing": existing_el,
        })
    return plan


def _norm_id(ident: str) -> str:
    ident = ident.strip().upper()
    if ident.startswith("US"):
        return re.sub(r"^US-?", "US", ident)
    return re.sub(r"^(EP|TX|F|T)-?", lambda m: m.group(1) + "-", ident)


# ─────────────────────────── commands ───────────────────────────

def cmd_pull(client: Client, project: str, out_dir: Path, apply: bool) -> None:
    data = client.list_all(project)
    dump = out_dir / "openproject_dump.json"
    by_type: dict[str, int] = {}
    for e in data["elements"]:
        t = (e.get("_links", {}).get("type", {}) or {}).get("title", "?")
        by_type[t] = by_type.get(t, 0) + 1
    print(f"== pull == {len(data['elements'])}/{data['total']} work packages")
    print("  by type: " + (", ".join(f"{k}={v}" for k, v in sorted(by_type.items())) or "(none)"))
    if not apply:
        print(f"\n  PLAN  {dump}\n\nDry-run — nothing written. Re-run with --apply.")
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    dump.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  write {dump}")


def cmd_push(client: Client, project: str, root: Path, out_dir: Path,
             with_tasks: bool, apply: bool) -> None:
    parser = _load_parser()
    rows = parser.collect(root, with_tasks)

    dump = out_dir / "openproject_dump.json"
    existing = []
    if dump.is_file():
        existing = json.loads(dump.read_text(encoding="utf-8")).get("elements", [])
        print(f"  matched against {len(existing)} existing work packages (from {dump.name}).")
    else:
        print(f"  note  no {dump} — every item will be a CREATE. Run `pull --apply` first to enable UPDATE.")

    plan = build_plan(rows, existing)
    types = client.types() if apply else {}
    priorities = client.priorities() if apply else {}

    creates = sum(1 for p in plan if not p["existing"])
    updates = len(plan) - creates
    print(f"\n{'APPLY' if apply else 'DRY-RUN'} — {len(plan)} work packages "
          f"({creates} CREATE, {updates} UPDATE)\n")
    for p in plan:
        verb = "UPDATE" if p["existing"] else "CREATE"
        par = f"  ↳ under {p['parent_our_id']}" if p["parent_our_id"] else "  (root)"
        print(f"  [{verb}] {p['type']:<11} {p['subject'][:70]}{par}")
    if not apply:
        print("\n(DRY-RUN — nothing sent. Re-run with --apply to execute.)")
        print("Tip: run `pull --apply` first so existing items UPDATE instead of duplicating.")
        return

    # type sanity-check up front (clear message instead of a mid-batch KeyError)
    needed = {p["type"] for p in plan}
    unknown = needed - set(types)
    if unknown:
        sys.exit(f"error: OpenProject has no type(s) named {sorted(unknown)}. "
                 f"Configured types: {sorted(types)}. Rename in docs/backlog/ or in OpenProject.")

    print("\n>>> APPLYING...\n")
    opid_by_ourid: dict[str, int] = {}
    for e in existing:  # seed with ids already in OpenProject
        oid = _our_id(e.get("subject", ""))
        if oid:
            opid_by_ourid[_norm_id(oid)] = e["id"]

    ok = fail = 0
    for p in plan:
        parent_id = opid_by_ourid.get(p["parent_our_id"]) if p["parent_our_id"] else None
        prio_href = priorities.get(p["priority"])
        try:
            if p["existing"]:
                wp_id = p["existing"]["id"]
                fields: dict = {"subject": p["subject"]}
                if p["description"]:
                    fields["description"] = {"raw": p["description"]}
                client.patch(wp_id, fields, lock=p["existing"].get("lockVersion"))
                opid_by_ourid[p["our_id"]] = wp_id
                print(f"  ok  UPDATE #{wp_id} {p['our_id']}")
            else:
                res = client.create(p["subject"], types[p["type"]], project,
                                    parent_id=parent_id, description=p["description"],
                                    priority_href=prio_href)
                opid_by_ourid[p["our_id"]] = res["id"]
                print(f"  ok  CREATE #{res['id']} {p['our_id']}")
            ok += 1
        except OpenProjectError as ex:
            fail += 1
            print(f"  FAIL {p['our_id']}: {ex}")
    print(f"\nDone: {ok} ok, {fail} failed on project {project}.")
    if fail:
        print("Re-run `pull --apply` then `push --apply` to retry only what is still missing (idempotent).")


def main() -> None:
    ap = argparse.ArgumentParser(description="OpenProject REST API round-trip adapter for docs/backlog/.")
    ap.add_argument("command", choices=["pull", "push"], help="pull = download work packages; push = project backlog")
    ap.add_argument("--root", default="docs", help="docs root (default: docs)")
    ap.add_argument("--out-dir", default="openproject", help="dump/output dir (default: openproject)")
    ap.add_argument("--with-tasks", action="store_true", help="(push) also emit T/TX tasks")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args()

    root = Path(args.root)
    project_root = root.parent if root.name == "docs" else Path.cwd()
    url, token, project, verify = load_config(project_root)
    print("== openproject-api.py ==")
    print(f"url={url}  project={project}  verify_ssl={verify}  command={args.command}  apply={args.apply}")
    client = Client(url, token, verify)
    out_dir = Path(args.out_dir)

    try:
        if args.command == "pull":
            cmd_pull(client, project, out_dir, args.apply)
        else:
            cmd_push(client, project, root, out_dir, args.with_tasks, args.apply)
    except OpenProjectError as ex:
        if ex.code == 401:
            sys.exit(f"{ex}\n  → 401 = bad/empty token. Check OPENPROJECT_TOKEN (or .env API_KEY) "
                     f"has NO trailing space and is a valid API token.")
        sys.exit(str(ex))


if __name__ == "__main__":
    main()
