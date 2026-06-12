# Integrations — index

> **One folder, three homes.** Each integration of this skill with an external tool lives in **three places** by function (the skill's taxonomy is function-based, not feature-based). This index ties them together so you can find all three parts of any integration at a glance.
>
> - **Doc** (the *what/why/how*) → here, `references/integrations/<name>.md` — reachable via the MCP as `requirements://reference/<name>`.
> - **Adapter** (the *executable*) → `../../assets/integrations/<name>.sh` (or equivalent).
> - **Validator** (the *advisory check*, when applicable) → the MCP server, `../../mcp-server/`.

## Available integrations

| Integration | Doc | Adapter | Validator |
|---|---|---|---|
| **SDD — OpenSpec · GitHub Spec Kit** (project the `docs/` spine into a Spec-Driven Development execution loop, preserving `[RF-NN]` tags) | [`sdd-interop.md`](sdd-interop.md) | [`../../assets/integrations/project-to-sdd.sh`](../../assets/integrations/project-to-sdd.sh) | `check_projection_drift` ([`../../mcp-server/`](../../mcp-server/README.md)) |
| **OpenProject — backlog → Excel sync** (project `docs/backlog/` Epics/Features/User Stories into OpenProject work packages: `Type`/`ID`/`Subject`/`Priority`) | [`openproject.md`](openproject.md) | [`../../assets/integrations/project-to-openproject.py`](../../assets/integrations/project-to-openproject.py) | — (round-trip via the `<our-id>` Subject prefix) |

## Planned

| Integration | Status |
|---|---|
| *(none currently)* | propose one via the "how to add" steps below |

## How to add a new integration

1. **Doc** → add `references/integrations/<name>.md` (the crosswalk, the projection/sync recipe, the round-trip rule). It is auto-exposed by the MCP as `requirements://reference/<name>` (the server scans `references/` recursively, excluding this `README.md`).
2. **Adapter** → add `assets/integrations/<name>.sh` (or the script in the right language) — dry-run by default, never overwrites, `set -Eeuo pipefail`.
3. **Validator** (optional) → add an advisory `@mcp.tool()` to `mcp-server/` that never blocks, only reports drift.
4. **Index** → add a row to the table above.

> **Source of truth stays in `docs/`.** Every integration *projects from* the `docs/requirements/` + `docs/backlog/` spine into the external tool's format — never the other way around. The `[RF-NN]` identifier is what carries traceability across the boundary; preserve it.
