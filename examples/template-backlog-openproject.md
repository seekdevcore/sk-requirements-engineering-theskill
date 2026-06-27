# Template — Backlog in OpenProject style (complete worked example)

> Template **filled with a real example**, not an empty skeleton. Use it as a concrete starting point for any project backlog. Reflects the OpenProject hierarchy per the *"IFPB"* ERS course (LECTURES 07–09) and the *"Interpop"* convention. Replace the example with your domain while keeping all the conventions.

---

## 0. Pre-requisite — the backlog is BASED on the requirements document

**Rule zero (non-negotiable)**: the backlog **is a materialization of the requirements document**. Everything to be built is born in the requirements document; the backlog only organizes, slices, and prioritizes that content.

So:

- 🔁 **Before touching the backlog, ALWAYS verify whether the requirements document was changed.** During the project, the user/client may ask to alter, add, or remove requirements — and those changes must propagate to the backlog (not the other way around).
- 📎 **The top of the backlog must point to the requirements document** (link or relative path): `Requirements document: ../docs/specs/<feature>/REQUISITOS.md (rev. of DD/MM/YYYY)`.
- ⚠️ **Backlog changes without origin in the requirements document are suspicious**: either *scope creep* (scope growing without approval), or purely technical refinement (should become a Task, not a Feature). In both cases, **record the decision in the requirements document first**.
- 🔗 **Traceability runs both ways**: from the requirements document to the backlog (RF/RNF → Feature/CA) AND from the backlog to the document (every Feature/US/CA references which RF/RNF of the specification it satisfies).

> Whoever follows this discipline never has that "wait, did we agree on this or did someone invent it?" moment. Whoever does not, pays in rework.

---

## 1. Hard rules (non-negotiable)

Detail in [05-convencoes-interpop.md](../references/05-convencoes-interpop.md) and [04-bdd-criterios-aceitacao.md](../references/04-bdd-criterios-aceitacao.md).

1. **The requirements document is the source of truth.** Always check changes there before touching the backlog (see §0 above).
2. **No infinitive** in Epic/Feature/US titles: `"Booking list"`, not `"List bookings"`.
3. **No technical terms** in Epic/Feature/US/CA/NFR: REST endpoints, libs, frameworks, table names, shell commands — all of these go into **Tasks**.
4. **ALL artifacts have business-language descriptions**: Epic, Feature, US, CA, NFR. Readable by any stakeholder (PO, client, junior dev just arriving). No URLs, no method names, no stack.
5. **Feature has a description (paragraph) + ACs**. NEVER has BDD.
6. **User Story has BDD** (`Given/When/Then`) **inside the "Description" field itself** (not as separate child items in OpenProject) + ACs inherited via traceability. Never has its own ACs.
7. **AC is declarative, atomic, and testable**. If the rule requires sub-rules, end the title with **`[...]`** and detail in the body (see §2 below).
8. **ACs are always grouped** under a `CA - <Theme>` grouper, even when the Feature has only 1 AC. The grouping keeps visual consistency and eases future insertion.
9. **Nested Epic** is used when the domain has sub-classifications (module → group → operation). This is the faithful way to organize large systems in OpenProject.

---

## 2. `[...]` convention for ACs with detail (hard rule)

When an AC needs sub-rules to be fully testable, **end the title with `[...]`**. In the item body (the "description" field in OpenProject), open with `Rules to be applied:` followed by bullets.

**Why it exists**: whoever reads the backlog in **list mode** (OpenProject default view, with 50+ items on screen) must decide in 1 second whether that AC is self-sufficient or requires a click. The `[...]` signals this unambiguously.

### Concrete example (real case from the *"IFPB"* course)

**Title on the card** (visible in list mode):

```
CA09 - The FEDERATION combobox must apply the fill-in and validation rules as detailed [...]
```

**Description (item body, read on opening)**:

```
Rules to be applied:
- The FEDERATION combobox is only enabled if a CONFEDERATION is selected.
- It must show only ACTIVE federations.
- In ALPHABETICAL order.
- It must show only the federations the logged-in user is associated with in their access record.
- It must allow partial search as the user types.
```

**Contrast — self-sufficient AC (without `[...]`)**:

```
CA05 - The CPF field is not mandatory. But if filled in, it must be in the format XXX.XXX.XXX-XX. If the CPF is invalid, emit an error message.
```

It does not need `[...]` because the title already contains everything required to test.

---

## 3. Complete visual hierarchy (territory map)

```
📄 Requirements Document (SOURCE OF TRUTH — always check before touching anything)
    │
    ▼
PROJECT (not a node in OpenProject — it is the project repository/context)
    │
    ├─ 🟦 ROOT EPIC #1                                  ← one front of the project
    │   └─ 🟦 SUB EPIC                                  ← sub-domain (module, area)
    │       └─ 🟦 SUB-SUB EPIC                          ← sub-sub-domain
    │           └─ 🟦 SUB-SUB-SUB EPIC                  ← IFPB example reaches 4 levels
    │               └─ 🟩 FEATURE                       ← client-deliverable
    │                   ├─ 📋 AC group "CA - <Theme A>" ← ACs always grouped
    │                   │    ├─ ✅ CA01 - self-sufficient rule
    │                   │    ├─ ✅ CA02 - self-sufficient rule
    │                   │    └─ ✅ CA03 - rule with sub-rules [...]
    │                   ├─ 📋 AC group "CA - <Theme B>"
    │                   │    └─ ✅ CA04 - ...
    │                   └─ 🟦 USER STORY                ← one-sprint slice
    │                       ├─ 🎬 BDD: Scenario 1 (happy path)        ┐
    │                       ├─ 🎬 BDD: Scenario 2 (error/edge)        │ ← content of the
    │                       └─ 🎬 BDD: Scenario 3 (alternative)       ┘   US "Description"
    │                                                                     field (NOT child
    │                                                                     cards in OpenProject)
    │                       └─ 🔧 TASK                              ← technical unit
    │                                                                  (technical terms OK)
    │
    ├─ 🟦 ROOT EPIC #2                                  ← another front (sibling)
    │   └─ ... (same internal structure)
    │
    └─ 🟦 ROOT EPIC #N                                  ← other fronts (siblings)
        └─ ...
```

> **🔴 Important rule about multiple root Epics**: a project **may (and almost always does) have multiple root Epics at the top level**, siblings to each other, **without a single "project-Epic" parent**. Each root Epic represents an **independent front** of the project: a platform (Web Application, Mobile Application), an operational family (Support, Quality and Investigation Activities), or a cross-cutting module.
>
> **Why not create a single "Product Epic" as the grandparent of everything**: the "product" as a whole is the **OpenProject repository / project context** — not an item of the hierarchy. Forcing everything under a single "Product Epic" creates an empty parent node (no useful description), hurts navigation, and creates ambiguity ("is this root Epic the whole product, or is it a front?").
>
> **Real examples**:
>
> - ***"Controle de Dopagem"*** (*"IFPB"* course): `EPIC WEB APPLICATION` · `EPIC MOBILE APPLICATION` · `EPIC SUPPORT, QUALITY AND INVESTIGATION ACTIVITIES` — three root Epics, siblings at the top level.
> - ***"Interpop"***: `EP-10 Editorial Search` · `EP-09 Thematic Filters` · `EP-15 Newsletter` · `EP-20 Editorial Moderation` — several root Epics, siblings. There is no "*"Interpop"*" Epic as parent.

> **Note on BDD in OpenProject**: BDD scenarios are **content of the User Story "Description" field**, not child items of the hierarchy (they do not become their own cards). The schema above shows the **conceptual** relation (BDD belongs to the US). Whoever works with Cucumber/Behave externally may mirror each scenario in a corresponding `.feature` file.

---

## 4. WORKED EXAMPLE A — *"Interpop"* Editorial Search (1 Epic level)

Lean example for medium-scale systems. Reflects what is in production at *"Interpop"*.

> **Requirements document:** [`../docs/specs/busca-editorial/REQUISITOS.md`](../../../../Documentos/Projetos/interpop/docs/specs/busca-editorial/REQUISITOS.md) (rev. of 28/05/2026)
> **Last requirements-document change check:** 03/06/2026 — no changes since the last sprint.

### 🟦 EP-10 — Editorial Search

| Field | Value |
|---|---|
| **ID** | `EP-10` |
| **Priority** | 🟠 High |
| **Status** | In Progress |
| **Target sprint** | Sprint 3, Sprint 4 |
| **Belongs to** | Web Application |
| **Direct Features** | `F-30`, `F-31`, `F-32` |
| **Origin (requirements)** | RF-08, RF-09, RF-10, RNF-04 |

**Description:**

A set of features that lets the reader find *"Interpop"* articles through keywords and filters, with results ordered by relevance. Includes sharing the search by link (the URL preserves the typed term and the filters, letting the reader send the ready-made search to another person). The Epic covers everything from simple text search (Feature `F-30`) through thematic-filter search (`F-31`) and sharing (`F-32`).

---

### 🟩 F-30 — Text search of articles

| Field | Value |
|---|---|
| **ID** | `F-30` |
| **Type** | Feature |
| **Parent Epic** | `EP-10` |
| **Priority** | 🟠 High |
| **Status** | In Progress |
| **Target sprint** | Sprint 3 |
| **Client-deliverable?** | Yes |
| **Origin (requirements)** | RF-08, RF-09, RNF-04 |

**Description:**

A "Search" screen that lets the reader type a word or phrase and view the *"Interpop"* articles that contain that term in the title, the summary, or the body. The results appear ordered by relevance (articles with the term in the title appear first), with the searched term highlighted in yellow within each result. The list is paginated (loads 20 articles at a time, with a "Load more" button at the bottom) and respects a response time the reader perceives as instantaneous.

#### F-30 Acceptance Criteria

##### 📋 CA - Access and visibility

| ID | Description | Detail? |
|---|---|---|
| `CA01` | The search is accessible to any site visitor, with no need to log in. | — |
| `CA02` | The search shows only articles with **published** status. Articles in draft or under moderation never appear in the results. | — |
| `CA03` | If the reader types a term and there are no matching articles, the system displays the message "No articles found for <term>" and keeps the search field filled in. | — |

##### 📋 CA - Query behaviour

| ID | Description | Detail? |
|---|---|---|
| `CA04` | The search accepts terms with a **minimum of 2 characters** and a **maximum of 100 characters**. Terms outside that range do not trigger a query — the field displays the message "Type between 2 and 100 characters". | — |
| `CA05` | The search is **case-insensitive and diacritic-insensitive**: typing "POP", "pop", "Pop", or "póp" returns the same articles. | — |
| `CA06` | The search finds occurrences of the term in the article's **title**, **summary**, and **body**, in this order of relevance priority **[...]** | ✅ |
| `CA07` | The query must be performed taking into account the **thematic filter options** applied by the reader **[...]** | ✅ |

##### 📋 CA - Presentation of results

| ID | Description | Detail? |
|---|---|---|
| `CA08` | The results are presented as **stacked vertical cards**, containing title, summary (first 200 characters), publication date, and author. The searched term appears highlighted in yellow. | — |
| `CA09` | The list loads **20 articles per page**. At the bottom of the page there is a **"Load more"** button that adds the next 20. | — |
| `CA10` | The URL of the search page must preserve the term and the applied filters, in the format `/buscar?q=<term>&tema=<id>`, allowing sharing. | — |

##### 📋 CA - Response time

| ID | Description | Detail? |
|---|---|---|
| `CA11` | The first results screen must appear within **800ms (p95)** for an archive of up to 5,000 published articles. | — |
| `CA12` | When the query takes longer than 800ms, the system displays a **visual loading indicator** (card skeleton) so it does not give the impression of a frozen screen. | — |

#### Detail of ACs with `[...]`

##### CA06 — Detail

> **Appears in the CA06 item body in OpenProject:**

```
Rules to be applied:
- Relevance is calculated so that articles with the term in the TITLE receive the highest weight.
- Next, articles with the term in the SUMMARY receive intermediate weight.
- Finally, articles with the term only in the BODY receive the lowest weight.
- When two articles have the same relevance, the most recent appears first.
- Accented and unaccented terms are treated as equivalent ("acao" finds "ação").
- Uppercase and lowercase terms are treated as equivalent ("KPOP" finds "kpop").
```

##### CA07 — Detail

> **Appears in the CA07 item body in OpenProject:**

```
Rules to be applied:
- The reader can select ONE OR MORE thematic filters before or during the search.
- The filters are shown as clickable chips above the results list.
- When a filter is selected, the list is rebuilt WITHOUT losing the current search term.
- When all filters are removed, the search goes back to considering all themes.
- If the reader combines term + filter and there are no results, the CA03 message must mention both the term and the active filter.
```

#### F-30 User Stories

##### 🟦 US30.1 — Basic presentation and ordering of search results

| Field | Value |
|---|---|
| **ID** | `US30.1` |
| **Parent Feature** | `F-30` |
| **Priority** | 🟠 High |
| **Status** | In Progress |
| **Target sprint** | Sprint 3 |
| **Covered ACs** | `CA01`, `CA02`, `CA05`, `CA06`, `CA08`, `CA09`, `CA11` |
| **Story Points** | 8 |

**US Description (the "Description" field in OpenProject — BDD, all scenarios live here):**

```gherkin
Scenario: Reader performs a simple search and views ordered results
  Given the reader is on the Interpop home page
  And there are 142 published articles containing the word "kpop"
  When the reader accesses the search from the top menu
  And types "kpop" in the search field
  And presses Enter
  Then the system presents a list of article cards
  And the articles appear ordered from most relevant to least relevant
  And the first 20 articles appear on the first screen
  And the term "kpop" appears highlighted in yellow on each card
  And the full first screen loads in under 800ms

Scenario: Reader finds no results
  Given the reader is on the search page
  And there is NO published article with the word "xkcdunicornio"
  When the reader types "xkcdunicornio" and presses Enter
  Then the system displays the message "No articles found for xkcdunicornio"
  And the search field stays filled with the typed term

Scenario: Reader shares the search by link
  Given the reader is viewing the search results for "kpop"
  When the reader copies the URL from the address bar
  And sends it to another person
  And that other person opens the link in another browser
  Then the other person sees the same results, in the same order
  And the term "kpop" appears filled in the search field
```

**US30.1 Tasks** (technical terms ALLOWED):

| ID | Task description | Priority |
|---|---|---|
| `T30.1.1` | Implement endpoint `GET /api/v1/search/articles?q=&tema=&cursor=` with HMAC-signed keyset pagination. | 🟠 |
| `T30.1.2` | Index `tsvector` column (Postgres `to_tsvector('portuguese', title \|\| ' ' \|\| body)`) with weights A/B/C. | 🟠 |
| `T30.1.3` | Create React `<SearchPage>` component with a `useSearch` hook and 250ms debounce. | 🟠 |
| `T30.1.4` | Implement term highlighting in cards with `<mark>` + yellow CSS `#FFE9A0`. | 🟡 |
| `T30.1.5` | Add a card `loading` skeleton after 300ms of waiting. | 🟡 |
| `T30.1.6` | Write pytest tests covering CA01, CA02, CA05, CA06 (matrix with 12 terms). | 🟠 |
| `T30.1.7` | Write Playwright tests covering the 3 BDD scenarios above. | 🟠 |

##### 🟦 US30.2 — Thematic filtering of search results

| Field | Value |
|---|---|
| **ID** | `US30.2` |
| **Parent Feature** | `F-30` |
| **Priority** | 🟠 High |
| **Status** | Refining |
| **Target sprint** | Sprint 4 |
| **Covered ACs** | `CA07`, `CA10` |
| **Story Points** | 5 |

**US Description (the "Description" field in OpenProject — BDD):**

```gherkin
Scenario: Reader combines a search term with a theme filter
  Given the reader is on the search page with the term "kpop" typed in
  And there are 3 themes available: "Música", "Moda", "Cinema"
  When the reader selects the "Música" filter among the chips above the list
  Then the list is rebuilt showing only articles in the "Música" theme that contain "kpop"
  And the URL starts including the parameter tema=musica
  And the "Música" chip appears highlighted (Interpop primary colour)

Scenario: Reader removes all filters and keeps the term
  Given the reader is viewing results filtered by "kpop" + theme "Música"
  When the reader clicks the "X" of the "Música" chip
  Then the list goes back to showing articles of all themes with the word "kpop"
  And the tema parameter is removed from the URL
  And the term "kpop" stays filled in the search field
```

**US30.2 Tasks:**

| ID | Task description | Priority |
|---|---|---|
| `T30.2.1` | Add a `tema` parameter to the search endpoint; apply `WHERE article.tema_id = ANY(:temas)`. | 🟠 |
| `T30.2.2` | Implement a `<ChipFilter>` component that syncs with the query string via React Router. | 🟠 |
| `T30.2.3` | Cover the 2 BDD scenarios above with Playwright. | 🟠 |

---

## 📋 Cross-cutting Tasks (technical configurations that are NOT Features)

| ID | Description | Priority | For which US |
|---|---|---|---|
| `TX-12` | Add the `idx_article_search_vector` index in the migration `0008_search_index.sql`. | 🟠 | `T30.1.2` |
| `TX-13` | Configure the variable `SEARCH_DEBOUNCE_MS=250` in `.env.example` and in `config/settings/base.py`. | 🟡 | `T30.1.3` |
| `TX-14` | Add the `react-highlight-words` lib to `package.json` (~5KB gz). | 🟡 | `T30.1.4` |

---

## 📊 Backlog summary

| Level | Count |
|---|---|
| Epics (including sub-Epics) | 1 |
| Features | 1 (`F-30`) |
| ACs | 12 (in 4 groups: Access, Behaviour, Presentation, Response time — **2 with `[...]` detail**: `CA06`, `CA07`) |
| User Stories | 2 (`US30.1`, `US30.2`) |
| BDD scenarios | 5 |
| Tasks (US-bound) | 10 |
| Cross-cutting Tasks | 3 |
| **Total Story Points** | **8 (Sprint 3) + 5 (Sprint 4) = 13** |

### Sprint plan

| Sprint | Focus | Story Points | Features delivered |
|---|---|---|---|
| Sprint 3 | Functional end-to-end basic search (US30.1) | 8 | — (Feature F-30 not yet 100%) |
| Sprint 4 | Thematic filters (US30.2) + relevance review | 5 | `F-30` 100% |

---

## 🔗 Traceability

| Requirement (RF/RNF) | Origin (requirements doc) | Feature | US | AC | BDD | Task | Test |
|---|---|---|---|---|---|---|---|
| RF-08: The reader can search articles by free text | `REQUISITOS.md` §4.2 | `F-30` | `US30.1` | `CA01`, `CA05`, `CA06` | "Reader performs a simple search and views ordered results" | `T30.1.1`, `T30.1.2` | `backend/tests/test_search.py::test_busca_basica`, `e2e/search.spec.ts::busca-simples` |
| RNF-04: The first search screen must appear in ≤800ms (p95) | `REQUISITOS.md` §5.3 | `F-30` | `US30.1` | `CA11` | (same scenario above) | `T30.1.2` | `backend/tests/test_search_perf.py::test_p95_under_800ms` |
| RF-09: The reader can filter the search by editorial theme | `REQUISITOS.md` §4.3 | `F-30` | `US30.2` | `CA07`, `CA10` | "Reader combines a search term with a theme filter" | `T30.2.1`, `T30.2.2` | `e2e/search.spec.ts::filtro-tema` |

---

## ⚖️ Falbo validation (7 dimensions per Feature)

| Feature | Complete | Correct | Consistent | Realistic | Necessary | Prioritizable | Verifiable |
|---|---|---|---|---|---|---|---|
| `F-30` | ✅ input/rule/output of each AC | ✅ reviewed with PO on 03/06 | ✅ ACs do not contradict each other | ✅ Postgres + tsvector already mastered | ✅ reader requested in UX research | ✅ 🟠 High | ✅ 12 tests covering ACs |

---

## 5. WORKED EXAMPLE B — Deeply nested Epic (*"Athlete Registration"*, Doping Control system)

Example for large systems. Reflects the OpenProject screenshot from the *"IFPB"* ERS course.

> **Requirements document:** `docs/specs/controle-dopagem/REQUISITOS.md` (rev. of 12/11/2025)

### 🟦 EP-100 — Web Application

| Field | Value |
|---|---|
| **ID** | `EP-100` |
| **Priority** | 🟠 High |
| **Belongs to** | *"Sistema de Controle de Dopagem"* (*"CNPq"* 487777/2013-1) |
| **Origin (requirements)** | RF-001 to RF-133 (total scope) |
| **Sub-Epics** | `EP-100.1` (Administrative Module) and 9 other modules |

**Description:**

The entire web interface of the national anti-doping control system. It brings together ten operational modules (Administrative, Doping, *"STJD"*, *"OCD"*/*"Escortes"*, General Use, Financial, Statistical, Technical, Access Control) that serve *"ABCD"*, *"COB"*, sports confederations, athletes, and accredited laboratories.

---

### 🟦 EP-100.1 — Administrative Module

| Field | Value |
|---|---|
| **ID** | `EP-100.1` |
| **Parent Epic** | `EP-100` |
| **Origin (requirements)** | RF-001 to RF-040 |
| **Sub-Epics** | `EP-100.1.1` (Athlete Management), `EP-100.1.2` (Physician Management), … |

**Description:**

A module that brings together all the registration, lookup, and reporting operations for the actors that take part in regulated competitions: athletes, physicians, confederations, federations, sports, competitions, coaches. It is the system's **master-data** module — the other modules (Doping, *"STJD"*, Financial) consume data from it.

---

### 🟦 EP-100.1.1 — Athlete Management

| Field | Value |
|---|---|
| **ID** | `EP-100.1.1` |
| **Parent Epic** | `EP-100.1` |
| **Origin (requirements)** | RF-001 to RF-020 |
| **Sub-Epics** | `EP-100.1.1.1` (Registration), `EP-100.1.1.2` (Lookup), `EP-100.1.1.3` (Report) |

**Description:**

A set of operations that give the *"ABCD"*/confederation operator the complete view of each athlete: from the initial registration (personal data, categories, sponsors) through lookup with advanced filters and the generation of reports for oversight and accountability.

---

### 🟦 EP-100.1.1.1 — Athlete Registration

| Field | Value |
|---|---|
| **ID** | `EP-100.1.1.1` |
| **Parent Epic** | `EP-100.1.1` |
| **Origin (requirements)** | RF-001 to RF-010 |
| **Direct Features** | `F-200` Basic Registration, `F-201` Sports Categories, `F-202` Sponsors, `F-203` Coach, `F-204` Athlete Grant, `F-205` Medical Team, `F-206` Call-ups, `F-207` Special Programs, `F-208` Clubs/Associations, `F-209` Competition Results |

**Description:**

A set of screens that let the confederation operator register and keep up to date the complete record of each national athlete. The registration is segmented into ten independent Features, each covering a distinct aspect of the athlete's life (personal data, sports affiliations, technical support, financial, medical, and competition history). Each Feature is delivered separately because it may be filled in at different times (there is no mandatory order other than the basic registration coming before the others).

---

### 🟩 F-200 — Athlete Basic Registration

| Field | Value |
|---|---|
| **ID** | `F-200` |
| **Type** | Feature |
| **Parent Epic** | `EP-100.1.1.1` |
| **Priority** | 🔴 Immediate |
| **Origin (requirements)** | RF-001 |
| **Client-deliverable?** | Yes |

**Description:**

A registration screen with the athlete's essential personal data: full name, date of birth, *"CPF"*, gender, nationality, *"RG"*, and home address. It is the system's entry point for a new athlete — without this registration, none of the other Athlete Management Features can be used. The confederation operator fills in, validates, and saves; the athlete then appears in the national system.

#### F-200 Acceptance Criteria

##### 📋 CA - Personal-data registration

| ID | Description | Detail? |
|---|---|---|
| `CA01` | Only authorized users (confederation operator or *"ABCD"* administrator) can register athletes. | — |
| `CA02` | The system must prevent registering two athletes with the same CPF. If one already exists, display the message "CPF already registered for <athlete name>". | — |
| `CA03` | The date of birth must result in an age between 5 and 80 years at the moment of registration. Outside that range, the system displays a review alert. | — |
| `CA04` | The CPF must be validated for format and check digit **[...]** | ✅ |

##### CA04 — Detail (in the item body)

```
Rules to be applied:
- The CPF field is mandatory.
- It must be in the format XXX.XXX.XXX-XX (with dots and a dash).
- The check digit must be valid according to the Receita Federal rule.
- If invalid, display the message "Invalid CPF" next to the field, in red.
- Do not allow saving while the CPF is invalid.
```

> *The remaining Features (F-201 to F-209) follow the same pattern. In a real backlog, each Feature has its own section with description, ACs, US, and Tasks.*

---

## ✅ Smell test (run before merging the backlog)

- [ ] **Did you check the requirements document before touching the backlog?** (date of the last check recorded at the top of BACKLOG.md)
- [ ] Does every Feature/US/CA have an **origin link** (`Origin (requirements)`) pointing to the corresponding item in the requirements document?
- [ ] Does every Epic/Feature/US/CA/RNF have a **description** in business language without technical terms?
- [ ] Is every Feature **client-deliverable** (unambiguously)?
- [ ] Does every US have **BDD** with named scenarios (≥2 scenarios: happy + error/edge) in the US "Description" field?
- [ ] Is every AC **declarative, atomic, and testable**? Do ACs with sub-rules end with **`[...]`** and have "Rules to be applied:" in the body?
- [ ] Is every AC **inside a `CA - <Theme>` group** (even Features with only 1 AC)?
- [ ] Is the Epic **nested** when the domain has sub-classifications?
- [ ] Is every cross-cutting Task in **`TX-NN`**, outside the Epic/Feature/US hierarchy?
- [ ] **Priority** (🔴/🟠/🟡/🟢) on every node?
- [ ] **Stable IDs** (not renumbered on later changes)?
- [ ] **Traceability** RF/RNF → Feature → US → AC → BDD → Task → Test **complete** for each Feature?
- [ ] **Falbo validation** filled with a 1-line justification per dimension?
