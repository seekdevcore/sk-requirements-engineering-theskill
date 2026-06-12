# OpenProject — backlog → Excel synchronization (optional integration)

> **When to use this reference**: when the team tracks the backlog in **OpenProject** and wants this skill's
> `docs/backlog/` spine to *feed* it through the **[OpenProject Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)**
> (an OpenProject-provided `.xlsm` template that pushes/pulls work packages via the API). This skill owns the
> **quality of the backlog item** (business-language titles, priority, traceability); OpenProject owns the
> **work-package tracking** (boards, sprints, assignees). This file is the bridge. **Optional** — skip if the
> project does not use OpenProject.

> **Only `docs/backlog/` is projected.** The `docs/requirements/` side (`RF`/`RNF`) is the *why* — it is **not**
> a work package and is **not** exported. The work packages are the backlog: **Epics → Features → User Stories**
> (and, optionally, Tasks). Source of truth stays in `docs/backlog/`; the OpenProject project is a *projection*.

---

## 1. The column standard (the skill default — adaptable)

The exported table has exactly **four columns**, named as OpenProject shows them in the work-package table:

| Column | What it carries | Rule |
|---|---|---|
| **Type** | the work-package type | `Epic` · `Feature` · `User story` · `Task` (match your OpenProject configured type names) |
| **ID** | OpenProject's own numeric id | **left blank** on export — OpenProject **assigns** it on import (their id ≠ ours) |
| **Subject** | the readable title | **`<our-id> <business-language title>`** — e.g. `EP-10 Gestão de Salas (Admin)`, `F-26 Aprovação de reserva`, `US25.2 Recursos de Filtragem…` |
| **Priority** | the work-package priority | the *"Interpop"* scale mapped to OpenProject: 🔴 → `Immediate` · 🟠 → `High` · 🟡 → `Normal` · 🟢 → `Low` |

> **Why our id lives in the Subject, not the ID column** — OpenProject's `ID` is auto-assigned and is *its own*
> (a different number from our `EP-NN`/`F-NN`/`USNN.M`). Putting our stable id at the **start of the Subject**
> keeps the traceability visible inside OpenProject (and survives re-import), exactly as the OpenProject UI
> renders it. The `ID` column stays blank so OpenProject creates + numbers the work package.

> **Hierarchy**: the four columns above are the skill default (it is what the user specified, and what the
> non-Enterprise work-package table shows). The export emits rows in **hierarchy order** (each Epic, then its
> Features, then their User Stories); set the OpenProject **parent** relationship after import, or add a `Parent`
> column if your OpenProject Excel template uses one. The "relations" column is an Enterprise add-on.

---

## 2. The adapter (generate the table)

```bash
# dry-run (prints the work-package table, writes nothing)
python3 assets/integrations/project-to-openproject.py

# write it (CSV always; XLSX too when openpyxl is installed)
python3 assets/integrations/project-to-openproject.py --apply
python3 assets/integrations/project-to-openproject.py --with-tasks --apply   # also emit T/TX as Tasks
```

- Reads `docs/backlog/epics/*.md` (→ `Epic`) and `docs/backlog/features/*.md` (→ `Feature` + the `User story`
  headings inside; `Task` only with `--with-tasks`).
- Writes `openproject/openproject-backlog.csv` (stdlib, always) and `openproject/openproject-backlog.xlsx`
  (only if `openpyxl` is available — `uv add openpyxl` / `pip install openpyxl`; CSV-only otherwise).
- **Dry-run by default**, `--apply` to write, **never overwrites** an existing file (`set`-strict spirit).
- Title is taken from the `# <id> — <title>` heading; priority from the item's emoji (🔴🟠🟡🟢) or a
  `Prioridade`/`Priority` line; missing priority defaults to `Normal`.

---

## 3. The Excel-synchronization recipe

1. In OpenProject, open your project's work-package view → **download the Excel-synchronization template**
   (`.xlsm`) per the [OpenProject docs](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/).
2. Run the adapter (`--apply`) → open `openproject/openproject-backlog.xlsx` (or `.csv`).
3. **Paste the rows** (`Type` · `ID` · `Subject` · `Priority`) into the sync template (leave the `ID` column
   empty for new work packages — OpenProject fills it on the first push).
4. Push from the template → OpenProject creates the Epics/Features/User Stories and assigns their numeric ids.
5. On later runs, OpenProject's ids come back in the template; reconcile titles/priority and re-push.

> **Round-trip rule** (same spirit as the SDD bridge, `references/integrations/sdd-interop.md`): the backlog's
> source of truth stays in `docs/backlog/`. When something changes in OpenProject during execution, reconcile it
> back into the backlog files first, then re-export. Never let the OpenProject copy silently diverge — the
> `<our-id>` prefix in the Subject is what lets you match a work package back to its `docs/backlog/` file.

---

## 4. The two mandatory root Epics (skill default)

The skill's default backlog hierarchy (from the *"IFPB"* course) always ends with **two mandatory root Epics**,
siblings to the project's feature-front Epics:

- **`Improvements`** (pt-BR *"Melhorias"*)
- **`Complementary Activities`** (pt-BR *"Atividades complementares"*)

They are generated by the scaffolder with the same idempotent *create-if-missing / never-overwrite* logic as the
rest of the spine, and the user can always adapt. *(Their detailed function is documented with the scaffolder.)*

---

*External: [OpenProject Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)
(repos/URLs may move — search "OpenProject Excel synchronization"). Cross-references:
`05-convencoes-interpop.md` (ids, priority scale, business-language titles), `10-estrutura-projeto.md` (the
`docs/backlog/` spine), `../integrations/README.md` (integrations index). Adopted here as an **optional**
backlog-tracking bridge — the source of truth stays in `docs/backlog/`.*
