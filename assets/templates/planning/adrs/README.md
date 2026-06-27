<!-- GENERIC TEMPLATE — adapt to your project. See references/10-estrutura-projeto.md §5 (two-tier ADRs). -->
# ADRs — Architecture Decision Records (PROJECT level)

> System-wide **cross-cutting** architectural decisions, MADR format (Markdown ADR).
> Decisions local to a single feature live in `../../specs/<feature>/adrs/` (TIER 2), sharing the SAME global numbering.

## Convention

- **Sequential global numbering** (`ADR-NNN-slug.md`) — continuous across tier 1 (here) and tier 2 (specs).
- Status: `Accepted` | `Superseded by ADR-NNN` | `Deprecated` | `Proposed`.
- Changing a decision → write a **new** ADR that supersedes the old one (NEVER edit the previous one).
- Renumbering is **forbidden** (ADR-005 is always ADR-005, even once deprecated).
- Variant tag (`-DB`, `-FE`, `-UI`) when the same number resolves parallel decisions across distinct layers.

## Catalogue

| ID | Title | Status |
| --- | --- | --- |
| [001](./ADR-001-....md) | <decision> | Accepted |

## Cross-ref

- `../../specs/<feature>/adrs/INDEX.md` — feature-local ADRs (tier 2).
