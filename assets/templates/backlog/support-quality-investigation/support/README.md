<!-- CHILD-EPIC BUCKET — seeded by the scaffolder; skips if it exists. en-CA folder: `support/`.
     On OpenProject export → child Epic "Apoio" under the "Atividades de Apoio, Qualidade e Investigação" umbrella.
     Each TX-NN-*.md beside this README exports as a TASK child of the "Apoio" Epic. This is the migrated home of
     the former `atividades-complementares/` bucket (same TX-NN ids, same purpose). -->
# Support (*Apoio*) — child-Epic bucket

> **What it is**: child-bucket of [`../`](../) (the Support/Quality/Investigation umbrella).
> **On OpenProject**: child Epic **"Apoio"** under the umbrella root Epic.
> **Global priority**: 🟡 Normal.

---

## Product vision (becomes the *description* of the "Apoio" Epic on export)

Home of all **technical, configuration and infrastructure work that is NOT tied directly to a Feature or User Story** and is therefore a **cross-cutting Task `TX-NN`** — **not a Feature** (`SKILL.md` Rule 6 / Rule 4 of [`05-convencoes-interpop.md`](../../../../../references/05-convencoes-interpop.md)). Examples: environment variables, lint/format (ESLint/Prettier), CI/CD, `docker-compose`, initial folder scaffolding, observability (Sentry/Prometheus), config files.

> **Why it exists**: technical configuration is not a client-facing deliverable → not a Feature. But it needs a **visible, traceable** home for the technical team — here, as `TX-01`, `TX-02`, …
>
> **What does NOT belong here**: a technical task that **supports one specific US** — that is a `TNN.M.K` **inside that US**, not a `TX`.

## Items in this bucket (each `TX-NN-*.md` beside this README → a Task child of the "Apoio" Epic)

| ID | Technical task | Layer | Status |
| --- | --- | --- | --- |
| `TX-01` | `<config / infra / tooling>` | Backend/Infra | ⏳ Pending |

## Traceability

A `TX` serves the project, not a Feature — so it links **↑** to the **ADR** or **RNF** that motivates it (if any) and **↓** to the **commit/PR** that delivers it. This `README.md` is **not** exported as an item.

## Related ADRs

`<infra/tooling decisions, if any>`
