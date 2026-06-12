# OpenProject — backlog ↔ work packages (REST API round-trip)

> **When to use this reference**: when the team tracks the backlog in **OpenProject** and wants this skill's
> `docs/backlog/` spine to *feed* it. The **primary** method is the **OpenProject REST API v3** (a small Python
> adapter that pulls and pushes work packages directly — runs on Linux/macOS/Windows). The legacy
> **[Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)**
> `.xlsm` template is kept only as a **Windows-only fallback** (§6). This skill owns the **quality of the backlog
> item** (business-language titles, BDD, priority, traceability); OpenProject owns the **work-package tracking**
> (boards, sprints, assignees). This file is the bridge. **Optional** — skip if the project does not use OpenProject.

> **Only `docs/backlog/` is projected.** The `docs/requirements/` side (`RF`/`RNF`) is the *why* — it is **not**
> a work package and is **not** exported. The work packages are the backlog: **Epics → Features → User Stories**
> (and, optionally, Tasks). Source of truth stays in `docs/backlog/`; the OpenProject project is a *projection*.

> ⚠️ **Why the API is primary (and the `.xlsm` is not).** OpenProject's Excel-sync template drives the API
> through `winhttpcom.dll` — a **Windows-only** COM component. On Linux/macOS (or LibreOffice) the macro simply
> does not run. A real project (*"SIRA"*) hit exactly this wall and moved to the REST API, which needs nothing
> but Python 3 stdlib. So this skill defaults to the API and demotes the spreadsheet to a fallback.

---

## ✅ For you to use it — plain steps (no jargon)

Want to put your whole backlog into OpenProject without typing item by item? Here is the simple path — it works
on **any** computer (Windows, Mac or Linux):

1. **Get your access code in OpenProject.** Sign in → click your name (top corner) → **My account** →
   **Access tokens** → create an **API** token. A code appears — copy it and keep it safe (treat it like a
   password; never share it or commit it to git).
2. **Tell the skill three things** (you set them once, as environment variables — or put the token in a small
   `.env` file you keep private):
   - your OpenProject **address** (e.g. `https://openproject.your-company.com`),
   - your **access code** (from step 1),
   - your **project** (its short name/slug, or its number).
3. **Download what's already there** (so nothing gets duplicated): ask me (or run the adapter) to **`pull`**.
   It saves a snapshot of the current work packages.
4. **Send your backlog.** Ask me to **`push`**. First it shows a *preview* (what it will create/update,
   nothing sent yet). When it looks right, run it **for real** (`--apply`). OpenProject creates your Epics,
   Features and User Stories and **nests one inside the other by itself** (Epic on top, Feature under it, and so
   on) — you do **not** link them by hand.
5. **Changed the backlog later?** Just `pull` then `push` again — it **updates** what already exists and only
   **creates** what's new (it matches items by the `EP-NN`/`F-NN`/`USNN.M` code at the start of each title).

> **Private or self-signed server?** If your OpenProject runs on an internal address with a "not trusted"
> certificate, there is **one extra setting** to allow it (`OPENPROJECT_VERIFY_SSL=false`). Only do this for a
> server you control and trust. I will walk you through it.
>
> **The "links" between tasks that depend on each other** (like "this one only after that one") are filled in a
> **second pass**, after the items exist and have numbers (§4). I will guide you when the time comes.

---

## 1. Authenticate by environment (never hard-code a token)

The adapter reads its configuration from environment variables (the token may instead live in a `.env` file as
`API_KEY=…`, kept gitignored):

| Variable | What it is | Example |
|---|---|---|
| `OPENPROJECT_URL` | base URL of your OpenProject | `https://openproject.example.com` (or `https://host:port`) |
| `OPENPROJECT_TOKEN` | your API token (My account → Access tokens → **API**) | `a1b2c3…` *(or `API_KEY=a1b2c3…` in `.env`)* |
| `OPENPROJECT_PROJECT` | project identifier — **slug or numeric id** | `my-project` **or** `163` |
| `OPENPROJECT_VERIFY_SSL` | `false` to skip TLS check (self-signed/private) — default `true` | `false` *(trust-on-purpose only)* |

```bash
export OPENPROJECT_URL=https://openproject.example.com
export OPENPROJECT_TOKEN=xxxxxxxxxxxxxxxx     # or API_KEY=... in a gitignored .env
export OPENPROJECT_PROJECT=my-project         # slug or numeric id
# export OPENPROJECT_VERIFY_SSL=false         # only for a self-signed cert you trust
```

> **Auth scheme**: HTTP Basic with the literal username `apikey` and the token as the password
> (`Authorization: Basic base64("apikey:<token>")`). This is the standard OpenProject API-key scheme.

---

## 2. The adapter — pull / push (the primary path)

```bash
# 2.1 download the current work packages (the round-trip anchor — carries OpenProject ids + lockVersion)
python3 assets/integrations/openproject-api.py pull --apply

# 2.2 project docs/backlog/ → OpenProject (DRY-RUN first: prints the CREATE/UPDATE plan, sends nothing)
python3 assets/integrations/openproject-api.py push
python3 assets/integrations/openproject-api.py push --apply            # execute
python3 assets/integrations/openproject-api.py push --with-tasks --apply  # also create T/TX as Tasks
```

What it does:

- **`pull`** — paginated `GET /api/v3/projects/<project>/work_packages` → writes
  `openproject/openproject_dump.json` (`{total, elements}`, the raw work packages incl. `id`, `lockVersion`,
  `subject`, `description`, and all `_links`). This is what lets `push` **update instead of duplicate**.
- **`push`** — reads `docs/backlog/` with the **same parser** as the Excel adapter (Epics → product vision;
  Features → business description; the `User story` headings inside → their **BDD** as the description; Tasks
  only with `--with-tasks`), then for each item:
  - **matches** an existing work package by the `<our-id>` prefix of its Subject (`EP-NN`/`F-NN`/`USNN.M`) →
    **UPDATE** (PATCH subject + description); else **CREATE** (POST).
  - resolves the **type** href from `GET /api/v3/types` (by name — robust even when no work package uses a type
    yet; this is the `KeyError: 'Task'` trap the *"SIRA"* export hit) and the **priority** href from
    `/api/v3/priorities`.
  - wires the **parent** via a real API link (`_links.parent.href`) — §3.

Safety built in (lessons from the real project):

- **DRY-RUN by default** — `push` prints the plan and sends nothing until `--apply`.
- **Idempotent** — re-running `pull` then `push` updates what exists and creates only what's new; safe to repeat.
- **Per-item error isolation** — one failed work package does not abort the batch (it reports `FAIL <id>` and
  continues; re-run to retry only the missing ones).
- **Optimistic locking** — re-reads each work package's `lockVersion` immediately before a PATCH and retries
  once on a `409` conflict (someone else edited in between).
- **Retry/backoff** — on `429`/`5xx`, honours `Retry-After` with exponential backoff.

> **Round-trip rule** (same spirit as `references/integrations/sdd-interop.md`): the backlog's source of truth
> stays in `docs/backlog/`. When something changes in OpenProject during execution, reconcile it back into the
> backlog files first, then re-`push`. The `<our-id>` prefix in the Subject is what matches a work package back
> to its `docs/backlog/` file.

---

## 3. Hierarchy is automatic (real parent links)

The adapter emits items in tree order (Epic → Feature → User story → Task) and sets each work package's
**`_links.parent.href`** to the OpenProject id of its parent (resolved on the fly: a parent created earlier in the
same run, or one already present from the `pull`). So OpenProject **nests the tree for you** — you never wire
parent/child by hand.

| Type | Depth | Parent |
|---|---|---|
| `Epic` | 0 | none (root) |
| `Feature` | 1 | its Epic |
| `User story` | 2 | its Feature |
| `Task` | 3 | its User Story (or, for cross-cutting `TX`, the *Complementary Activities* Epic — §7) |

> **Our id lives in the Subject, not in an id column.** OpenProject assigns its **own** numeric id (different from
> our `EP-NN`/`F-NN`/`USNN.M`). Keeping our stable id at the **start of the Subject** keeps traceability visible
> inside OpenProject and is exactly what the next `pull`/`push` uses to re-match the work package.

---

## 4. Relations are a second pass (they need OpenProject ids)

Cross-item **Relations** (`follows`, `blocks`, `precedes`, `relates`, `requires`, …) reference OpenProject's
**numeric ids**, which do not exist until the work packages are created. So relations are a **round-trip**, after
the first `push`:

1. `push --apply` → hierarchy + descriptions + priority created; OpenProject assigns ids.
2. `pull --apply` → the dump now has every numeric id.
3. Create the relations you want with `POST /api/v3/work_packages/{id}/relations`
   (`{"_links": {"to": {"href": "/api/v3/work_packages/<other-id>"}}, "type": "follows"}`).
4. Relation **types must be the English API terms**: `relates, duplicates, duplicated, blocks, blocked, precedes,
   follows, includes, partof, requires, required`.

> The backlog models **hierarchy + traceability**, not arbitrary cross-item dependencies — so the adapter does
> not invent relations; you add the few that matter in this second pass.

---

## 5. Field mapping (what the API carries)

| Concept | API field | Source in `docs/backlog/` |
|---|---|---|
| Type | `_links.type.href` (lookup by name via `/types`) | the artifact kind (Epic/Feature/User story/Task) |
| Project | `_links.project.href = /api/v3/projects/<id>` | `OPENPROJECT_PROJECT` |
| Parent | `_links.parent.href = /api/v3/work_packages/<id>` | the hierarchy (§3) |
| Priority | `_links.priority.href` (lookup by name via `/priorities`) | the item's emoji 🔴🟠🟡🟢 → `Immediate`/`High`/`Normal`/`Low` |
| Concurrency | root `lockVersion` (required on PATCH) | from the `pull` dump (re-read fresh before write) |
| Title | `subject` | `# <our-id> — <business title>` heading |
| Body | `description.raw` (markdown) | Epic = product vision · Feature = business description · **User Story = its BDD** |

---

## 6. Windows-only fallback — the Excel-synchronization `.xlsm`

If you are on **Windows** and prefer a spreadsheet, the legacy path still works. There is a second adapter that
emits the table OpenProject's Excel-sync template expects:

```bash
python3 assets/integrations/project-to-openproject.py --apply           # CSV always; XLSX if openpyxl present
python3 assets/integrations/project-to-openproject.py --with-tasks --apply
```

- It writes `openproject/openproject-backlog.csv` (+ `.xlsx` if `openpyxl` is installed; `uv add openpyxl`).
- **Seven columns**: `Type · ID · Subject · Priority · Description · Parent · Relations`. `ID`/`Parent`/`Relations`
  are left blank; the **Subject is indented 4 spaces per level**, and on upload the macro reads the indentation,
  nests the tree, and auto-fills `Parent`.
- Recipe: in OpenProject download the **Excel-synchronization template** (`.xlsm`), configure it (URL, token,
  project), paste the generated columns, press **Ctrl + B** to upload.

> ⚠️ **The macro is Windows-only** (`winhttpcom.dll`). On Linux/macOS/LibreOffice it will not send. There, use the
> **REST API adapter** (§2) instead. The `.xlsm` is also where the token sits in a cell — keep that file
> **gitignored** (see §7).

---

## 7. Security (lessons from the real deployment)

- **Token in environment or a gitignored `.env`, never in a committed file.** The `.xlsm` stores the token in a
  cell — add `*.xlsm` (and `.env`, and any private API-script folder) to `.gitignore`.
- **Trailing whitespace in `.env` → silent `401`.** A stray space after `API_KEY=<token>` makes the auth header
  wrong and the server answers `401 Unauthorized` with no obvious cause. The adapter **strips** surrounding
  whitespace/quotes for exactly this reason; if you hit a 401, check for a trailing space first.
- **Self-signed / private server**: `OPENPROJECT_VERIFY_SSL=false` disables TLS verification — acceptable only
  for a server you control. Prefer installing the CA / using a real certificate when you can.
- **A token that ever appeared in a terminal, log, or screen-share is compromised — rotate it.** Revoke it in
  My account → Access tokens and issue a new one.

---

## 8. The two mandatory root Epics (skill default)

The skill's default backlog hierarchy (from the *"IFPB"* course) always ends with **two mandatory root Epics**,
siblings to the project's feature-front Epics:

- **`Improvements`** (pt-BR *"Melhorias"*) — product enhancements/refinements of existing things.
- **`Complementary Activities`** (pt-BR *"Atividades Complementares"*) — the home for cross-cutting **`TX`**
  (technical/config/infra work not tied to a Feature/US, per Rule 4 of `05-convencoes-interpop.md`).

They are generated by the scaffolder with the same idempotent *create-if-missing / never-overwrite* logic as the
rest of the spine, and the user can always adapt. *(Their detailed function is documented with the scaffolder
templates.)*

---

*External: [OpenProject API v3](https://www.openproject.org/docs/api/) ·
[Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)
(Windows-only fallback; URLs may move — search "OpenProject API v3" / "OpenProject Excel synchronization").
Cross-references: `05-convencoes-interpop.md` (ids, priority scale, business-language titles),
`04-bdd-criterios-aceitacao.md` (BDD = the User Story's content), `10-estrutura-projeto.md` (the `docs/backlog/`
spine), `../integrations/README.md` (integrations index). Adopted here as an **optional** backlog-tracking
bridge — the source of truth stays in `docs/backlog/`.*
