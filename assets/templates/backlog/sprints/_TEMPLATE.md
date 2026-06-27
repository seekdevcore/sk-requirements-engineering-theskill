<!-- GENERIC TEMPLATE — copy to sprint-N-<slug>.md.
     PRINCIPLE: do NOT rewrite the Epic/Feature/US — REFERENCE the existing docs (traceability lives at the source).
     TWO status axes (one row carries both). The EMOJI is the stable token; the word is BILINGUAL — write it in the
     person's/team's language (EN or pt-BR):
       • Status        = sprint work progress + who:  ⏳ To do/A fazer · 🔨 Doing/Fazendo · ✅ Done/Feito · ⤳ Skipped/Adiado
       • Status Final  = GitHub-derived PR state (as in the project's root README):  ✅ Merged/Mergeada · 🔄 In review/Em revisão · 📭 PR open/PR aberta · — (no PR/sem PR)
     BLOCKS = one per person (the block title names WHO does it), mirroring the SIRA root-README roadmap.
     Anything dropped to a later sprint goes to the "Adiados (skipped)" section with a reason — and its Status becomes ⤳ Skipped. -->
# Sprint N — <short goal>

> **Period**: DD/MM — DD/MM · **Goal**: <single goal of the sprint>
> **Team**: <people> · **Coverage gate**: <e.g. 40%>

## References (do not rewrite — only link)

> What enters this sprint **is already specified** in the backlog/requirements. Here we only **reference** the source documents — traceability lives in them, you do not copy the Epic/Feature/US content here.

| Source | Document |
| --- | --- |
| Requirements (RF/RNF) | [requirements/](../../requirements/) |
| Epic(s) in scope | [EP-NN](../epics/EP-NN-....md) |
| Feature(s) in scope | [F-NN](../features/F-NN-....md) · [F-NN](../features/F-NN-....md) |

## Legend for the two statuses (bilingual — use the person's/team's language)

> The **emoji is the stable token**; the word next to it is **bilingual** (EN / pt-BR) — write it in the language of whoever fills it in. Mixing languages across blocks is OK (each person in their own).

- **Status** — progress within the sprint (and implicitly *who*, via the block): **⏳ To do / A fazer** · **🔨 Doing / Fazendo** · **✅ Done / Feito** · **⤳ Skipped / Adiado** (see [§ Deferred](#deferred-to-another-sprint-skipped))
- **Status Final** — PR state on GitHub (as in the project's root README): **✅ Merged / Mergeada** · **🔄 In review / Em revisão** · **📭 PR open / PR aberta** · **— (no PR / sem PR)**

## Blocks — who does what (mirrors the project's root README)

> One **block per person**; the block title says **who**. Each row **references** the US in the Feature document (does not rewrite the US). The **PR** column comes right after **Status Final**.

### Block 1 — <block theme> · *<EN Person>*  <!-- example: English-speaking person -->

| US | Description | Status | Status Final | PR |
| --- | --- | --- | --- | --- |
| [US-NN.M](../features/F-NN-....md) | <short ref — links the US, does not rewrite> | 🔨 Doing | — | — |
| [US-NN.M](../features/F-NN-....md) | <…> | ✅ Done | ✅ Merged | [#NNN](https://github.com/<org>/<repo>/pull/NNN) |

**Conclusion:** X / Y user stories completed.

### Block 2 — <block theme> · *<pt-BR Person>*  <!-- example: Portuguese-speaking person -->

| US | Description | Status | Status Final | PR |
| --- | --- | --- | --- | --- |
| [US-NN.M](../features/F-NN-....md) | <…> | ⏳ A fazer | 🔄 Em revisão | [#NNN](https://github.com/<org>/<repo>/pull/NNN) |

**Conclusion:** X / Y user stories completed.

## Deferred to another sprint (skipped)

> Every US that **does not fit** in this sprint (lack of time, dependency, reprioritization, any reason) goes here — with a **reason** and a **destination**. In the block above, its **Status** becomes **⤳ Skipped**. That way no one has to dig through history for why something did not make it in.

| US | Block / Owner | Reason for deferral | Goes to |
| --- | --- | --- | --- |
| [US-NN.M](../features/F-NN-....md) | Block N · *<Person>* | <lack of time / blocked by US-XX / reprioritized / …> | Sprint N+1 |

## Retrospective (fill in at the end of the sprint)

- **Delivered**: <US with Status ✅ Done/Feito · Status Final ✅ Merged/Mergeada>
- **Deferred (skipped)**: <US + reason — see § Deferred>
- **Learnings**: <what to improve next time>
