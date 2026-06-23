<!-- STRUCTURAL FOLDER — seeded by the scaffolder; skips if it exists. Top-level under docs/ (sibling of
     requirements/, backlog/). Home of production-incident records. This skill owns the HOME + the TRACEABILITY
     CONTRACT only; the authoring craft (blameless culture, timeline, 5-whys, action items) belongs to the
     documentation-engineer agent / the `postmortem-writing` skill. -->
# Postmortems — production-incident records (`PM-NN`)

> **What it is**: a top-level folder under `docs/` (sibling of `requirements/`, `backlog/`), one `PM-NN-<slug>.md` per production incident.
> **Not a backlog item / not an OpenProject work package** (like an ADR) — only its *corrective actions* (`BUG`/`TX`/`RB`) are.

A postmortem is the **"after" evidence** of requirements engineering — it records that a **dependability `RNF`** (availability, reliability, resilience — see [`../../../references/13-confiabilidade-seguranca.md`](../../../references/13-confiabilidade-seguranca.md)) or a `CA` **failed in production**, and closes the loop back to the requirement that should have held.

## Traceability (the part this skill owns)

- **↑ up** — the `RNF`/`CA` the incident **violated** (e.g. `AVAIL`, `RTO`/`RPO`, a publish-action `CA`).
- **← origin** — the `ISS-NN` it was **triaged** from (an *incident* is a triage outcome of the [issues inbox](../backlog/support-quality-investigation/issues/README.md), alongside Bug/Spike/TX/Melhoria), or a monitoring alert.
- **↓ down** — corrective `BUG-NN`/`TX-NN`, a new `RB-NN` runbook, and any **RNF tightening** — which goes through the **requirements document first** (rule zero, `SKILL.md §2.1`), then the backlog. Every action item carries an id so it is tracked to closure.

## Writing one

The `PM-NN-_TEMPLATE.md` here carries only the **traceability skeleton**. For the blameless write-up (timeline, root cause, 5-whys, action items), use the **`documentation-engineer`** agent or the **`postmortem-writing`** skill — then keep the ↑/← /↓ links filled so the incident stays traceable.
