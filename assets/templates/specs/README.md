<!-- GENERIC TEMPLATE — adapt to your project. Only present when the project uses SDD. -->
# Specs — Spec-Driven Development (the "HOW")

> Every non-trivial feature gets a `<feature-slug>/` folder with the **design contract** the
> implementation must satisfy. Design first, code second. The **why** lives in `../requirements/`;
> the **what/when** in `../backlog/`.

## Per-feature structure

```
specs/<feature-slug>/
├── DESIGN.md            design contract (architecture, data model, layers)
├── BACKLOG.md           local task breakdown (mirrors backlog/features/F-NN)
├── TEST-STRATEGY.md     how the feature is tested
├── SECURITY-REVIEW.md   threat model + mitigations
└── adrs/                this feature's TIER-2 ADRs (INDEX.md + tracker.md + ADR-NNN)
```

## Spec index

| Feature | Spec | Status |
| --- | --- | --- |
| <name> | [<slug>](./<slug>/DESIGN.md) | 📝 |

Use `_feature-template/` as the starting point (`cp -r _feature-template <slug>`).
