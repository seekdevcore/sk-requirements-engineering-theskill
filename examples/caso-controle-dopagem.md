# Worked Example — Doping Control System (real *"CNPq"* 487777/2013-1 case)

> Real case presented in LECTURE 03 of the ERS course at *"IFPB"*. Project funded by *"CNPq"*; integrated system for Brazilian sports entities (*"ABCD"* — *"Autoridade Brasileira de Controle de Dopagem"*, *"COB"* — *"Comitê Olímpico Brasileiro"*, sports confederations). Walks through elicitation → specification → backlog → US with BDD in a real critical system.
>
> **Note on language preservation**: the original Feature, Epic, User Story, AC, FR, NFR, and business-rule (G/E) titles were authored in pt-BR in the source *"IFPB"* / *"CNPq"* project — Redmine cards, *"SVN"* commits, and academic papers reference them verbatim. This en-CA edition translates the artifact content for an English-reading audience; where a pt-BR identifier is load-bearing for traceability with the source material, it is glossed in *italics+quotes*. **Explanations, tables, analysis, and artifact content are all in en-CA.**

---

## 1. Context and problem

**Business problem**: Absence of centralized doping-test control in Brazil. Each sports confederation had its own manual process or local spreadsheet. *"ABCD"* needed to aggregate national data to report to *"WADA"* (World Anti-Doping Agency). *"STJD"* needed to follow infraction proceedings. Result: fragmented data, follow-up difficulty, risk of international penalties.

**Feasibility study** — Sommerville's 3 questions:

1. ✅ Contributes to objectives? Yes (fulfilling the *"Código Mundial Antidopagem"* / World Anti-Doping Code)
2. ✅ Fits schedule/budget? Yes (*"CNPq"* approved; *"IFPB"* team)
3. ✅ Integrates with systems in use? Partially (needs to import existing spreadsheets)

→ Project proceeds.

---

## 2. Elicitation (combined techniques)

Per [02-elicitacao.md](../references/02-elicitacao.md), no isolated technique would suffice. The project used:

| Technique | Source | What was discovered |
|---|---|---|
| **Interviews** | *"ABCD"*, *"COB"*, confederations | Current processes, difficulties, expectations |
| **Document analysis** | *"Código Mundial Antidopagem"*, *"STJD"* regulations, existing spreadsheets | Formal rules; existing data structure |
| **Brainstorming** | Team + *"ABCD"* | New features (statistics module for BI) |
| **Observation** | Visits to *"ABCD"* | How samples are collected, transported, kept in custody |

**Stakeholders identified** (Wiegers 5 criteria):

- *"ABCD"* (central authority — operational user)
- *"COB"* (Olympic sphere — consultative user)
- Sports confederations (register athletes)
- Athletes (subjects of the tests; sensitive data — critical privacy)
- *"OCDs"* and *"Escoltas"* (control officers, outsourced)
- *"STJD"* (judges infractions)
- Accredited laboratories (receive samples)
- *"Ministério do Esporte"* (regulator)

---

## 3. High-level requirements identified

### 3.1 Functional requirements by module

Elicitation produced **10 modules**:

```
ADMINISTRATIVE   — Athlete, Physician, Confederation, Events, Modalities,
                   Federations, Competitions, Coach
DOPING           — KIT Request/Authorization, Test/Sample, Laboratory,
                   Custody, Test History, Detected Substances, Results
STJD             — Proceeding, Opinion, Ruling, Infractions, Processing,
                   History, Penalties, Defences
OCD/ESCORT       — OCD, Escort, OCS, Competencies, Availability,
MANAGEMENT       — Event Allocation, Costs
GENERAL USE      — People, Notifications, Ordinances, Requests
FINANCIAL        — Fees, Payment Slips, Default, Bank Reconciliation
DOPING           — Business Intelligence (BI)
STATISTICS
TECHNICAL        — Competition Organization, Competition Registration,
                 — Competition Judging
ACCESS           — Access (RBAC)
CONTROL
```

Total: 133 features identified in the initial scope.

### 3.2 Business Rules (Gxx notation) and Exceptions (Exx notation)

The project adopted **two distinct notations** for rules (LECTURE 03 *"IFPB"*):

- **Gxx** — General business rules (valid across the entire system base).
- **Exx** — Specific exceptions (rules that apply only in particular conditions).

#### General rules (Gxx) — sample from the rules document (v0.23, 175 total rules)

```
G09 — There cannot be two people with the same CPF.
G10 — Only users with access permission to a type-5 screen may
      ACTIVATE a record whose status is INACTIVE.
G11 — The phone-number mask must be: COUNTRY CODE
      (AREA CODE) PHONE NUMBER.
G12 — In phone fields, the country code must already be suggested
      as 55 (Brazil).
G13 — While a record's status is INACTIVE, its data
      cannot be changed (sole exception: a user with a type-5
      profile may edit the ACTIVE field).
G14 — A person's age is a field computed from the date
      of birth.
G15 — After the CEP (postal code) is entered, the system must display the related
      Country, State, City, District and Street.
G16 — Federation listing: the set depends on the selected
      Confederation.
G17 — Modality listing: the set depends on the selected
      Confederation.
...
```

#### Specific exceptions (Exx)

```
E1 — The father's name must be different from the mother's name.
E2 — The system must derive the athlete's initials from the name,
     but they may be edited.
E3 — If the athlete has a disability, the Disability Class field is
     mandatory. Otherwise, the Class field must not be
     filled in.
...
```

Note that **these rules come from different sources**:

- **Gxx** come from the DOMAIN (*"WADA"* / *"Código Mundial Antidopagem"*, *"STJD"* regulations, identity policy). Easy to miss — they only surfaced via document analysis.
- **Exx** come from OBSERVATION (ethnography + interviews with the team that registers athletes) — real edge situations that only operators have in their heads.

> **Recommended pattern**: separating Gxx (invariant domain rules) from Exx (conditional edge exceptions) makes it easier to trace origin and maintenance responsibility. When an exception becomes a general rule (all cases now behave the same), promote it from Exx to Gxx in the document.

### 3.3 Non-Functional Requirements

| Type | Requirement | Metric |
|---|---|---|
| **Product - Availability** | System available during business hours (Mon-Fri, 8h-18h) | ≥99.5% |
| **Product - Security** | Athletes' data confidential | RBAC + encryption at rest |
| **Product - Reliability** | Automated backup | Daily, 1-year retention |
| **Product - Platform** | Web (accessible to remote confederations) | Multi-browser |
| **Organizational - Technology** | Stack defined by the *"IFPB"* team | Java/JSF, *"Hibernate"*, *"Primefaces"*, PostgreSQL, *"IReport"*/*"Jasper"* |
| **Organizational - Process** | Versioning + ticketing | *"SVN"* + *"Redmine"* + *"Astah"* for UML |
| **External - Compliance** | Meet *"WADA"* / *"Código Mundial Antidopagem"* | Annual audit |
| **External - Privacy** | *"LGPD"* (sensitive health data) | Consent + retention + access audit |

---

## 4. Specification — backlog hierarchy

Applying the *"IFPB"* model from [03-especificacao.md](../references/03-especificacao.md).

> **Practical lesson from LECTURE 03 *"IFPB"* — backlog scope legend**: the original project slide for *"Controle de Dopagem"* uses 4 colours to classify the scope status of each Feature/Module:
>
> - 🟦 **Initial scope of *"CNPq"* project 487777/2013-1** (what is contracted)
> - 🟩 **Added to scope on *"ABCD"* demand** (expanded scope with documented approval)
> - 🟧 **Not in project — proposal for a NEW project** (recorded for the next call)
> - ⬜ **Not in project — to be explored with Confederations** (still in feasibility analysis)
>
> **Why this matters**: visually marking who-asked-for-what and what-fits-in-budget avoids silent scope creep. In any real backlog, an item entering the scope must have documented origin and a status flag. **No origin ≡ scope creep**. See `Origin (requirements)` in [template-backlog-openproject.md §4](template-backlog-openproject.md).

> **⚠️ Important — multiple root Epics, no single "project-Epic" parent**: the *"Controle de Dopagem"* project has **three Epics at the top level, siblings to each other** (`WEB APPLICATION`, `MOBILE APPLICATION`, `SUPPORT, QUALITY AND INVESTIGATION ACTIVITIES`). There is no "Epic Doping Control" node as a common grandparent — the "product" as a whole is the **OpenProject context/repository** of the project, not an item of the hierarchy. Convention detail in [`../examples/template-backlog-openproject.md §3`](template-backlog-openproject.md).

```
PROJECT Doping Control (= OpenProject context/repository; NOT an EPIC)
│
├─ EPIC WEB APPLICATION                                ← Root Epic #1 (front: web platform)
│   ├─ EPIC ADMINISTRATIVE Module
│   │    └─ EPIC ATHLETE Management
│   │         ├─ EPIC Athlete REGISTRATION
│   │         │    ├─ FEATURE Basic Registration with personal data
│   │         │    ├─ FEATURE Athlete Sport Categories
│   │         │    ├─ FEATURE Athlete Sponsors
│   │         │    ├─ FEATURE Athlete Coach
│   │         │    ├─ FEATURE Bolsa Atleta grants received
│   │         │    ├─ FEATURE Medical Team associated with the Athlete
│   │         │    ├─ FEATURE Call-ups to the National Team
│   │         │    ├─ FEATURE Participation in Special Programs
│   │         │    ├─ FEATURE Athlete Clubs/Associations
│   │         │    └─ FEATURE Competition Results
│   │         ├─ EPIC Athlete LOOKUP
│   │         │    ├─ FEATURE GENERAL Athlete Lookup
│   │         │    └─ FEATURE INDIVIDUAL Extract (Sport Record)
│   │         └─ EPIC Athlete REPORTING
│   │              ├─ FEATURE GENERAL ATHLETE Listing
│   │              └─ FEATURE Athlete Listing by Confederation
│   ├─ EPIC DOPING Module
│   │    └─ ...
│   └─ ... (other modules)
│
├─ EPIC MOBILE APPLICATION                             ← Root Epic #2 (front: mobile platform)
│   └─ ... (own sub-hierarchy)
│
└─ EPIC SUPPORT, QUALITY AND INVESTIGATION ACTIVITIES  ← Root Epic #3 (front: cross-cutting activities)
    └─ ... (own sub-hierarchy)
```

> **Note on the Features listed above:** in the real backlog, **each `FEATURE Xxxxx` item has its own description** (client-deliverable, no technical terms), per the skill rule (Feature has a description; User Story has BDD). This case study elaborates in depth only the `GENERAL Athlete Lookup` Feature (§5–§8) to illustrate the full AC → US → BDD → Estimation flow; the others are represented only by their title in the diagram. **In a real project, a Feature missing its description is specification debt** — it surfaces as friction in Sprint Planning (PO has to re-explain the deliverable) and in US review (devs question the "why" of the story).

---

## 5. Feature: GENERAL Athlete Lookup

**Feature description (client-deliverable):**

Lets authorized operators (*"ABCD"*, *"COB"* and confederations) query the national athlete base on a single paginated screen, applying optional filters by *"CPF"*, name, coach, sponsor, physician, modality, category, grant type, special program, competition and competition dates. The lookup is automatically restricted to the federations associated with the logged-in user on the server — there is no blind "global lookup", even for administrators. The client deliverable is the operational entry point for all subsequent doping flows: call-up for testing (rule G09), analysis of the athlete's test history, and cross-referencing with *"STJD"* proceedings. At real volume (*"ABCD"* aggregates ~50,000 national athletes), the feature must respond with lazy pagination and server-side sorting.

> This description is what goes on the OpenProject/Redmine Feature card. Business language, no technical terms (JSF/Hibernate/Primefaces stay in the Tasks). The acceptance criteria below formalize the testable rules; BDD appears only in the User Stories (§7).

### 5.1 Acceptance Criteria (declarative style)

Applying [04-bdd-criterios-aceitacao.md](../references/04-bdd-criterios-aceitacao.md). 15 declarative ACs, **grouped by theme** (`CA - <Theme>` convention from Rule 7 of [05-convencoes-interpop.md](../references/05-convencoes-interpop.md)). ACs with **`[...]`** at the end of the title must be read together with the detail in §5.2.

#### 📋 CA - Access and visibility

| ID | Description | Detail? |
|---|---|---|
| `CA01` | Only authorized users may access the GENERAL ATHLETE Lookup feature. | — |
| `CA02` | The lookup must display only the athletes of the sport FEDERATIONS the user has access to in their account. | — |
| `CA03` | The lookup screen must contain the fields and layout as defined in the prototype. | — |

#### 📋 CA - Filters and search

| ID | Description | Detail? |
|---|---|---|
| `CA04` | The lookup must be performed taking into account the filter options entered by the user. | — |
| `CA05` | The CPF field is not mandatory. But if filled in, it must be in the format XXX.XXX.XXX-XX. If the CPF is invalid, issue an error message. | — |
| `CA06` | The DATE fields in the Competitions filter are NOT mandatory. The lookup must be performed according to what the user filled in. | — |
| `CA07` | The NAME, COACH, SPONSOR and PHYSICIAN fields are NOT mandatory. But if filled in, they must have at least 5 letters. The application must perform a PARTIAL search on the typed content. | — |

#### 📋 CA - Comboboxes (enablement, listing and search rules)

| ID | Description | Detail? |
|---|---|---|
| `CA08` | The CONFEDERATION combobox must apply the listing and search rules **[...]** | ✅ |
| `CA09` | The FEDERATION combobox must apply the filling and validation rules **[...]** | ✅ |
| `CA10` | The MODALITIES and CATEGORIES comboboxes must apply the listing-by-confederation rules **[...]** | ✅ |
| `CA11` | The GRANT TYPE, SPECIAL PROGRAM and COMPETITION TYPE comboboxes must apply the listing and search rules **[...]** | ✅ |
| `CA12` | The COMPETITION combobox must display only multi-sport competitions and competitions specific to the confederation selected by the user. | — |

#### 📋 CA - Presentation of results

| ID | Description | Detail? |
|---|---|---|
| `CA13` | The general athlete listing must be displayed in alphabetical order by default. | — |
| `CA14a` | The general athlete listing may be re-sorted by clicking on the column titles. | — |
| `CA14b` | The general athlete listing must be paginated with options to view 10, 50, 100 or all. | — |
| `CA15` | The general athlete listing must display all athletes by default. | — |

### 5.2 Detail of ACs with `[...]`

Each block below is what appears in the **item body** in OpenProject (AC Description field), following the `Rules to be applied:` + bullets convention.

#### CA08 — Detail

```
Rules to be applied:
- Must display only ACTIVE CONFEDERATIONS.
- In ALPHABETICAL order.
- Must display only the confederations the logged-in user is associated with in their access account.
- Must allow partial search while typing.
```

#### CA09 — Detail

```
Rules to be applied:
- The FEDERATION combobox must only be enabled if a CONFEDERATION is selected.
- Must display only ACTIVE Federations.
- In ALPHABETICAL order.
- Must display only the federations the logged-in user is associated with in their access account.
- Must allow partial search while typing.
```

#### CA10 — Detail

```
Rules to be applied:
- Must display only data from the confederations the user is associated with in their access account.
- Display only ACTIVE records.
- In ALPHABETICAL order.
```

#### CA11 — Detail

```
Rules to be applied:
- Must display only ACTIVE records.
- In ALPHABETICAL order.
- Must allow partial search while typing.
```

---

## 6. Slicing into User Stories (3 sprints)

Applying the LECTURE 09 flow (see [03-especificacao.md §6.5](../references/03-especificacao.md)):

### 6.1 Group ACs by sprint (incremental prioritization)

```
Sprint 1 — BASIC lookup (simplest possible deliverable)
  CA01 — Authorized access
  CA02 — Implicit filter by user's federation
  CA03 — Prototype layout
  CA13 — Default alphabetical order
  CA15 — Display all by default

Sprint 2 — Sorting + pagination
  CA14a — Re-sort on header click
  CA14b — Pagination 10/50/100/all

Sprint 3 — Advanced search
  CA04 — Applied filters
  CA05 — CPF validation
  CA06 — Optional dates
  CA07 — Partial search by name/etc.
  CA08-CA12 — Active comboboxes + alphabetical + partial search
```

### 6.2 Resulting User Stories

```
US BASIC Athlete Listing                                       (Sprint 1)
US Athlete Listing with sorting and pagination (no search)     (Sprint 2)
US Advanced Athlete Listing with search options (filter)       (Sprint 3)
```

---

## 7. BDD of US "BASIC Athlete Listing"

```gherkin
# language: en
Feature: Basic athlete listing

  Background:
    Given the user is logged in to the application
    And has access permission to the administrative module

  Scenario: Authorized user accesses the basic listing
    When accessing the administrative menu > ATHLETES
    Then the system must display the basic athlete list
    And the athletes must be only from the federations associated with the user (CA02)
    And the listing must be in alphabetical order by name (CA13)
    And all athletes must be displayed by default (CA15)
    And the layout must match the approved prototype (CA03)

  Scenario: User without permission is blocked
    Given the user does NOT have access permission to the administrative module
    When trying to access the URL /admin/atletas directly
    Then the system must return error 403
    And must not display any athlete data
```

**OpenProject relations** (traceability):

```
US BASIC Athlete Listing
├─ related-to: CA01 (authorized access)
├─ related-to: CA02 (federation filter)
├─ related-to: CA03 (layout)
├─ related-to: CA13 (alphabetical order)
└─ related-to: CA15 (display all by default)
```

---

## 8. Estimation (Planning Poker)

Chosen guide story: **"Add a nickname field to the athlete registration"** (delivered in the previous sprint — 1 point).

Estimates:

| User Story | Points | Justification |
|---|---|---|
| US BASIC Listing | **5** | Query + RBAC + standardized view + prototype integration |
| US Listing with sorting/pagination | **3** | Small extensions over the basic + *"Primefaces"* components |
| US Advanced Listing with filters | **13** | Multiple cascading comboboxes, partial search across several fields, *"CPF"* validation, conditional display rules |

Total for the GENERAL LOOKUP feature: **21 points**.

With an average velocity of 25pts/sprint, the feature essentially fills 1 whole sprint (or spreads across 2 alongside smaller US).

---

## 9. Validation

### 9.1 Sommerville checks applied

- ✅ **Validity**: confirmed with *"ABCD"* in review (July 2023)
- ✅ **Consistency**: CA08 and CA09 are consistent — CA09 only activates if CA08 is selected
- ✅ **Completeness**: the review revealed missing AC for export (CSV) — added later
- ✅ **Realism**: the Java/JSF stack is familiar to the team; fits the schedule
- ✅ **Verifiability**: each CA has an associated Gherkin scenario

### 9.2 Falbo dimensions per AC

Each AC validated against the 7 criteria. **Initial CA05 was**: "The CPF field must be validated". It failed on **completeness** (did not state format) and **verifiability** (how to test?). Rewritten to the current version with explicit XXX.XXX.XXX-XX format.

### 9.3 Prototypes validated with *"ABCD"*

*"Pencil"* wireframes + paper sketches → photo sent by email → validation meeting → adjustments → wireframe v2 → approved.

---

## 10. Ethical aspects (*"SBC"* layer)

Applying [09-etica-sbc.md](../references/09-etica-sbc.md):

| Principle | Application in the case |
|---|---|
| **§1.1 Human well-being** | System supports sport integrity (public good) |
| **§1.2 Avoid harm** | A false doping accusation destroys an athlete's career — NFR of strict audit |
| **§1.4 Non-discrimination** | System cannot privilege/penalize athletes by federation, gender, modality |
| **§1.6 Privacy** | Health data (substances) extremely sensitive — encryption at rest + audited access + defined retention |
| **§1.7 Confidentiality** | Positive test results CANNOT leak before the formal *"STJD"* process |
| **§2.5 ML evaluation** | (If this system aggregates ML for suspicious-pattern detection — continuous bias auditing) |
| **§3.7 Societal infrastructure** | System integrates with the national sport infrastructure; standards of operation above the commercial-system average |

Concrete ethical decision: **a positive result automatically blocks the confederation UI** (G10) — not to hide it, but to prevent informal leakage before due process.

---

## 11. Lessons from the case

1. **Document analysis was more valuable than interviews** — the *"WADA"* Code has 200 pages of technical rules nobody at *"ABCD"* remembers by heart
2. **Diverse stakeholders require explicit prioritization** — confederations wanted registration features; *"ABCD"* wanted operations features; the conflict was resolved with MoSCoW (project Must-have = *"ABCD"* operation)
3. **Slicing into US saved the project** — basic version delivered in 3 months generated traction; the rest evolved with feedback
4. **BDD in pt-BR engaged non-technical stakeholders** — *"ABCD"* physicians reviewed scenarios and pointed out missing rule G14
5. **Traceability in *"Redmine"* + *"SVN"*** was adequate to the scale (no need for DOORS)
6. **Privacy NFRs dominated implementation cost** — audit + encryption + retention took as much effort as the feature itself
