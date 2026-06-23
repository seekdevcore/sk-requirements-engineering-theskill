<!-- STRUCTURAL FOLDER — seeded by the scaffolder; skips if it exists. Top-level under docs/ (sibling of
     requirements/, backlog/). Home of operational procedures. This skill owns the HOME + the TRACEABILITY
     CONTRACT only; the step authoring (commands, verification, rollback) belongs to the documentation-engineer
     agent / the `incident-runbook-templates` skill. -->
# Runbooks — operational procedures (`RB-NN`)

> **What it is**: a top-level folder under `docs/` (sibling of `requirements/`, `backlog/`), one `RB-NN-<slug>.md` per operational procedure (deploy, recovery, key rotation, scaling…).
> **Not a backlog item / not an OpenProject work package** (like an ADR).

A runbook is the **operational realization of a dependability `RNF`** — it is the procedure that actually delivers the resilience/availability target (`RTO`/`RPO`, `AVAIL`) a requirement promises. [`references/13-confiabilidade-seguranca.md §6`](../../../references/13-confiabilidade-seguranca.md) already notes that resilience is *sociotechnical* — incident runbooks and on-call are part of meeting the `RNF`.

## Traceability (the part this skill owns)

- **↑ up** — the `RNF` it **operationalizes** (resilience `RTO`/`RPO`, availability) and the `F-NN`/spec it serves.
- **↔ related** — the `PM-NN` postmortems that exercised or updated it (a recovery runbook is born from, and validated by, real incidents).

## Writing one

The `RB-NN-_TEMPLATE.md` here carries only the **traceability skeleton**. For the executable steps (commands, verification, rollback), use the **`documentation-engineer`** agent or the **`incident-runbook-templates`** skill — then keep the ↑ link to the `RNF` filled so the procedure stays traceable to the requirement it serves.
