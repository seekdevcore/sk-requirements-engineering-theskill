# OpenProject — backlog → Excel synchronization (optional integration)

> **When to use this reference**: when the team tracks the backlog in **OpenProject** and wants this skill's
> `docs/backlog/` spine to *feed* it through the **[OpenProject Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)**
> (an OpenProject-provided `.xlsm` template that pushes/pulls work packages via the API). This skill owns the
> **quality of the backlog item** (business-language titles, BDD, priority, traceability); OpenProject owns the
> **work-package tracking** (boards, sprints, assignees). This file is the bridge. **Optional** — skip if the
> project does not use OpenProject.

> **Only `docs/backlog/` is projected.** The `docs/requirements/` side (`RF`/`RNF`) is the *why* — it is **not**
> a work package and is **not** exported. The work packages are the backlog: **Epics → Features → User Stories**
> (and, optionally, Tasks). Source of truth stays in `docs/backlog/`; the OpenProject project is a *projection*.

---

## 1. The column standard (the skill default — adaptable)

The export has **seven columns**, named as OpenProject's Excel-sync template uses them:

| Column | What it carries | Rule |
|---|---|---|
| **Type** | the work-package type | `Epic` · `Feature` · `User story` · `Task` (match your OpenProject configured type names) |
| **ID** | OpenProject's own numeric id | **left blank** on a fresh export — OpenProject **assigns** it on import (their id ≠ ours) |
| **Subject** | the readable title, **indented** | `<our-id> <business title>` (`EP-10 Gestão de Salas`, `F-26 Aprovação de reserva`, `US25.2 …`), **prefixed with 4 spaces per hierarchy level** (see §2) |
| **Priority** | the work-package priority | *"Interpop"* scale → OpenProject: 🔴 `Immediate` · 🟠 `High` · 🟡 `Normal` · 🟢 `Low` |
| **Description** | the OpenProject Description field | **a User Story's description IS its BDD** (the Gherkin scenarios); a **Feature** carries its business-language description; an **Epic** its product vision |
| **Parent** | the parent work package | **left blank** — auto-filled by OpenProject from the Subject indentation (§2) |
| **Relations** | dependencies (follows/blocks/…) | **left blank** — a second pass (§3); needs OpenProject ids |

> **Why our id is in the Subject, not the ID column** — OpenProject's `ID` is auto-assigned and is *its own*
> (a different number from our `EP-NN`/`F-NN`/`USNN.M`). Putting our stable id at the **start of the Subject**
> keeps the traceability visible inside OpenProject (and survives re-import), exactly as the OpenProject UI
> renders it. The `ID` column stays blank so OpenProject creates + numbers the work package.

---

## 2. Hierarchy is automatic (no manual parent/child)

The OpenProject Excel-sync template builds the parent/child hierarchy from **indentation**: **4 empty spaces
before the Subject** mark a work package as a child. The adapter emits the Subject already indented by depth, so
on upload OpenProject **nests the tree and auto-fills the `Parent` column for you** — you never wire the
relations by hand.

| Type | Depth | Subject indent |
|---|---|---|
| `Epic` | 0 | `EP-10 Gestão de Salas (Admin)` |
| `Feature` | 1 | `····F-26 Aprovação de reserva` |
| `User story` | 2 | `········US25.2 Recursos de Filtragem…` |
| `Task` | 3 | `············T-26.1.1` |

(`·` = a space. The 4-space marker is the OpenProject default; rows are emitted in hierarchy order so the
indentation nests correctly.)

---

## 3. Relations are a second pass (they need OpenProject ids)

Cross-item **Relations** (`follows`, `blocks`, `precedes`, `relates`, `requires`, …) use the `Relations` column
with the syntax `"<type> <id>, <type> <id>"` (e.g. `follows 12345, precedes 45678`) — and the **id is
OpenProject's**, which **does not exist until the first import**. So relations are a **round-trip**:

1. Run the adapter → import the table (hierarchy + descriptions + priority created; OpenProject assigns ids).
2. **Export the work packages back from OpenProject** (Excel-sync *download*) — now every row has its numeric id.
3. Fill the `Relations` column with `"<type> <openproject-id>"` for the dependencies you want.
4. Re-import (upload) → OpenProject wires the relations.

> The adapter emits `Relations` as an **empty** column (the backlog models hierarchy + traceability, not
> arbitrary cross-item dependencies). Relation **types must be the English API terms**: `relates, duplicates,
> duplicated, blocks, blocked, precedes, follows, includes, partof, requires, required`.

---

## 4. The adapter

```bash
# dry-run (prints the work-package table, writes nothing)
python3 assets/integrations/project-to-openproject.py

# write it (CSV always; XLSX too when openpyxl is installed)
python3 assets/integrations/project-to-openproject.py --apply
python3 assets/integrations/project-to-openproject.py --with-tasks --apply   # also emit T/TX as Tasks
```

- Reads `docs/backlog/epics/*.md` (→ `Epic`, description = product vision) and `docs/backlog/features/*.md`
  (→ `Feature`, description = business paragraph; the `User story` headings inside, description = their BDD;
  `Task` only with `--with-tasks`).
- Writes `openproject/openproject-backlog.csv` (stdlib, always) and `openproject/openproject-backlog.xlsx`
  (only if `openpyxl` is available — `uv add openpyxl` / `pip install openpyxl`; CSV-only otherwise; the XLSX
  wraps the Description column).
- **Dry-run by default**, `--apply` to write, **never overwrites** an existing file.
- Title from the `# <id> — <title>` heading; priority from the item's emoji (🔴🟠🟡🟢) or a
  `Prioridade`/`Priority` line; missing priority defaults to `Normal`.

### The Excel-synchronization recipe

1. In OpenProject, download the **Excel-synchronization template** (`.xlsm`) per the
   [OpenProject docs](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)
   and configure it (URL, API token, project).
2. Run the adapter (`--apply`) → open `openproject/openproject-backlog.xlsx` (or `.csv`).
3. **Paste the columns** into the sync template (leave `ID`/`Parent`/`Relations` empty for new work packages).
4. Upload (`Ctrl + B`) → OpenProject creates the Epics/Features/User Stories, **nests them from the indentation**,
   assigns ids, and fills `Parent`. For relations, do the §3 round-trip.

> **Round-trip rule** (same spirit as `references/integrations/sdd-interop.md`): the backlog's source of truth
> stays in `docs/backlog/`. When something changes in OpenProject during execution, reconcile it back into the
> backlog files first, then re-export. The `<our-id>` prefix in the Subject is what lets you match a work package
> back to its `docs/backlog/` file.

---

## 5. The two mandatory root Epics (skill default)

The skill's default backlog hierarchy (from the *"IFPB"* course) always ends with **two mandatory root Epics**,
siblings to the project's feature-front Epics:

- **`Improvements`** (pt-BR *"Melhorias"*)
- **`Complementary Activities`** (pt-BR *"Atividades complementares"*)

They are generated by the scaffolder with the same idempotent *create-if-missing / never-overwrite* logic as the
rest of the spine, and the user can always adapt. *(Their detailed function is documented with the scaffolder.)*

---

*External: [OpenProject Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)
(URLs may move — search "OpenProject Excel synchronization"). Cross-references:
`05-convencoes-interpop.md` (ids, priority scale, business-language titles), `04-bdd-criterios-aceitacao.md`
(BDD = the User Story's content), `10-estrutura-projeto.md` (the `docs/backlog/` spine),
`../integrations/README.md` (integrations index). Adopted here as an **optional** backlog-tracking bridge — the
source of truth stays in `docs/backlog/`.*
