# Worked Example — Data Isolation Between Organizations in the *"GestorPro"* Project

> Fictional but realistic case from the *"GestorPro"* project (a multi-tenant SaaS for clinic and school management; Django 5 + DRF + PostgreSQL 16 + React 19). Each client organization is a **tenant** that shares the same physical database with the others while staying isolated from them. Shows how a **shared-base multi-tenant** feature maps to the skill's RE framework — useful for auditing tenancy specifications or as a template for new tenant-scoped features. Reference commit (illustrative): `b7c3f02` (feat(tenancy): per-organization isolation with RLS + atomic provisioning).
>
> **Note on language**: this worked example is written in **en-CA** (the skill's default language). Code symbols, file paths, identifiers, and commit-message conventions are kept verbatim; Brazilian domain terms (*"GestorPro"*, *"LGPD"*) are kept in their original form.

---

## 1. Context and problem

**Business problem**: *"GestorPro"* sells management software to clinics and schools. Each client (a clinic, a school) is an **organization** — a tenant — and all tenants live in one shared PostgreSQL base to keep operational cost low. The first version scoped queries by `organization_id` only at the application layer (a `.filter(organization=request.user.organization)` scattered across viewsets). This is fragile: a single forgotten filter, a raw query, a careless admin action, or an ORM mistake leaks one clinic's patient records into another clinic's screen — a catastrophic *"LGPD"* incident and the end of the product's reputation.

**Diagnosis**: tenant isolation was an **implicit, application-only requirement** with no safety net at the database. There was also no formal contract for "how a new organization is born" (provisioning could leave orphan rows) and no path for an organization to **export** or **erase** its data (LGPD portability and right to be forgotten). These are the kinds of requirements that surface only when you ask "what happens when this single filter is forgotten?" — see [02-elicitacao.md §7](../references/02-elicitacao.md). Once raised, they became explicit.

---

## 2. Stakeholders

Applying Wiegers 2003 (see [01-fundamentos.md §5](../references/01-fundamentos.md)):

| Stakeholder | Interest |
|---|---|
| **Product owner (*"GestorPro"*)** | Guarantee no tenant ever sees another tenant's data; protect the brand from a leak |
| **Organization administrator** (clinic/school owner) | Manage their own users and data; never touch another organization |
| **End user** (receptionist, teacher) | Operate within one organization without seeing isolation as friction |
| **Data subject** (patient, student) | Have their data isolated, exportable, and erasable under LGPD |
| **DPO / privacy officer** | Demonstrate isolation and fulfill portability/erasure requests per tenant |
| **Platform SRE** | Ensure a "noisy" tenant cannot degrade the others (quota and limits) |
| **External auditor** (hypothetical) | Verify cross-tenant access is provably impossible, not just unlikely |

---

## 3. AS-IS → TO-BE analysis

Applying the analysis from [08-analista-negocios.md §3](../references/08-analista-negocios.md):

### AS-IS (before commit b7c3f02)

```
ReceptionistA (Org A) → GET /api/v1/pacientes/
  → Viewset filters .filter(organization=user.organization)  [application only]
  → Returns Org A patients  ✅ (when the filter is present)

DeveloperX adds a new report endpoint, forgets the filter
  → GET /api/v1/relatorios/ returns ALL patients, every org  ❌ LEAK
  → Database has no second line of defence
```

**Pains**:

- Isolation depends on every developer remembering one filter, everywhere, forever
- A raw SQL query or a Django Admin listing bypasses the filter entirely
- New-organization signup ran several inserts without a transaction → orphan rows on failure
- No way for an organization to export or delete its own dataset (LGPD gap)
- One organization importing 2 M rows could exhaust shared resources for everyone

### TO-BE

```
ReceptionistA (Org A) → GET /api/v1/pacientes/
  → Session sets app.current_org = A; Postgres RLS enforces org = A
  → Returns Org A patients

DeveloperX's new endpoint forgets the application filter
  → RLS still scopes the rows to Org A  → no leak (safety net holds)

Admin A → POST /api/v1/organizacoes/  (new org signup)
  → Single transaction: create org + seed roles + admin user
  → On any failure: full rollback, zero orphans

Admin A → POST /api/v1/organizacoes/A/exportacao/   → ZIP of Org A only
Admin A → DELETE /api/v1/organizacoes/A/             → erases Org A only
```

### GAP analysis

| Gap | Solution |
|---|---|
| Isolation lives only in application filters; one omission leaks data | NFR: Row-Level Security policy in PostgreSQL as a database-level safety net (ADR-021) |
| Cross-tenant access attempts are not explicitly denied or logged | FR: deny + audit-log on any out-of-tenant access attempt |
| Tenant boundary is not expressed as a domain invariant | G: "Every piece of information belongs to exactly one organization" |
| Signup ran multiple inserts unguarded → orphans on failure | NFR: atomic provisioning in one transaction (no orphan rows) |
| No LGPD export/erasure per organization | FR: per-tenant export and erasure endpoints |
| A noisy tenant can starve shared resources | NFR: per-organization quota and rate limit |

---

## 4. Feature: Data isolation between organizations

**Feature description (client-deliverable):**

Ensures that each client organization of *"GestorPro"* sees and manipulates exclusively its own data, even while sharing the same physical base with the others. The belonging rule — every piece of information belongs to exactly one organization — is applied consistently across all read and write operations, with a safety net in the database (Row-Level Security) that stays in force even if an application filter is forgotten. The deliverable to the client is the guarantee that no clinic or school can, under any circumstance — including a direct query, a new report, or an administrative action — access another organization's data. The feature also covers the birth of a new organization (a signup that creates the tenant and its seed data in a single transaction, leaving no orphan rows), the portability of an organization's data (full export), and the right to be forgotten (full per-organization erasure), in compliance with *"LGPD"* (Brazil's General Data Protection Law).

> This description is what goes on the backlog Feature card. It is **written in business language**, readable by any stakeholder. The ACs below formalize the testable rules; BDD appears only in the User Stories (§5).

### 4.1 Goals and business rules (G)

| ID | Business rule |
|---|---|
| `G-01` | Every piece of information belongs to exactly one organization. |
| `G-02` | An organization's administrator neither accesses nor modifies another organization's data. |
| `G-03` | The birth of an organization either happens completely or does not happen at all — it never leaves orphan rows. |
| `G-04` | An organization's data can be exported and erased in isolation, without affecting the others. |

### 4.2 Non-functional requirements (quantitative, EARS body)

| ID | NFR | Measurement method | Priority |
|---|---|---|---|
| `RNF-01` | **Data isolation between organizations.** WHILE a session is bound to organization X, THE SYSTEM SHALL return 0 (zero) records belonging to any organization Y ≠ X, across 100% of read and write queries, guaranteed by an RLS policy in the database. | Cross-isolation test suite (1 scenario per tenant-scoped table) running with the application filter turned off; target: 0 leaks in 100% of cases. | 🔴 Immediate |
| `RNF-02` | **Cross-access denial.** IF a request attempts to read or write a record of an organization different from the session, THEN THE SYSTEM SHALL deny the operation and record the attempt in the audit log within ≤ 200 ms. | BDD test of a cross-access attempt verifies the denied response and the presence of 1 entry in the audit log. | 🔴 Immediate |
| `RNF-03` | **Per-organization quota and usage limit.** WHILE an organization consumes resources, THE SYSTEM SHALL limit it to 600 requests/min and 5 GB of storage per organization, without one organization's consumption raising the p95 latency of the others above 400 ms. | Load test with 1 "noisy" tenant (10× traffic) and measurement of the p95 latency of the other tenants via APM. | 🟠 High |
| `RNF-04` | **Atomic provisioning of a new organization.** WHEN a new-organization signup is submitted, THE SYSTEM SHALL create the tenant and its seed data in a single transaction; IF any step fails, THEN it SHALL roll back fully, leaving 0 orphan rows. | A test that injects a failure in the final provisioning step and verifies a count of 0 in all tables for the tenant. | 🔴 Immediate |
| `RNF-05` | **Per-organization data export.** WHEN an administrator requests the export, THE SYSTEM SHALL produce a package containing only its organization's data, within ≤ 5 min for up to 1 M records. | An export test validates that the package contains only the requesting tenant's IDs and measures the generation time. | 🟡 Normal |
| `RNF-06` | **Per-organization data erasure (forgetting).** WHEN an administrator confirms the organization's erasure, THE SYSTEM SHALL remove 100% of that tenant's data within ≤ 24 h, without affecting any record of another organization. | An erasure test verifies a count of 0 for the target tenant and an unchanged count for a neighbouring tenant. | 🟡 Normal |

### 4.3 Acceptance Criteria (declarative style)

11 ACs, **grouped by theme**. ACs with **`[...]`** at the end of the title must be read together with the detail in §4.4.

#### 📋 CA - Belonging and isolation

| ID | Description | Detail? |
|---|---|---|
| `CA01` | Every read returns only records of the current session's organization; no record of another organization appears. | — |
| `CA02` | Every write stores the record bound to the current session's organization; it is not possible to write on behalf of another organization. | — |
| `CA03` | The database safety net (RLS) keeps isolating even when the application filter is omitted **[...]** | ✅ |
| `CA04` | An attempt to access another organization's record is denied and recorded in the audit log **[...]** | ✅ |

#### 📋 CA - Per-organization quota and limit

| ID | Description | Detail? |
|---|---|---|
| `CA05` | An organization that exceeds the request limit receives a limit-exceeded response, without affecting the others **[...]** | ✅ |
| `CA06` | An organization that reaches the storage limit is prevented from writing new data until it frees space, without affecting the others. | — |

#### 📋 CA - Birth of an organization

| ID | Description | Detail? |
|---|---|---|
| `CA07` | The signup of a new organization creates the tenant and its seed data as a single unit **[...]** | ✅ |
| `CA08` | If any step of the signup fails, nothing is persisted — no orphan rows of the incomplete organization remain. | — |

#### 📋 CA - Portability and forgetting

| ID | Description | Detail? |
|---|---|---|
| `CA09` | An organization's export contains only that organization's data **[...]** | ✅ |
| `CA10` | An organization's erasure removes all of that tenant's data and none of another tenant's **[...]** | ✅ |
| `CA11` | After erasure, the organization's identifier cannot be reused to access old data; any access returns as non-existent. | — |

### 4.4 Detail of ACs with `[...]`

Each block below is what appears in the **item body** in the backlog (AC Description field), following the `Rules to be applied:` + bullets convention.

#### CA03 — Detail

```
Rules to be applied:
- The isolation policy in the database (RLS) holds independently of the application layer.
- Even if a new endpoint forgets the per-organization filter, the database returns only rows of the session's organization.
- Direct queries (reports, internal exports, administrative actions) also respect the database policy.
- The application keeps filtering by organization — RLS is the second line of defence, not a replacement for the first.
```

#### CA04 — Detail

```
Rules to be applied:
- Every attempt to read or write a record of an organization different from the session is denied.
- The denied attempt generates an entry in the audit log (who, which target organization, when, which resource).
- Another organization's resource responds as non-existent, without revealing that it exists (it does not distinguish "not found" from "forbidden").
- No data of the target organization is exposed in the denial response.
```

#### CA05 — Detail

```
Rules to be applied:
- Each organization has its own request-per-minute limit.
- On exceeding the limit, the organization receives a "limit exceeded" response (retry after an interval).
- One organization's consumption cannot raise the others' latency above the RNF-03 target.
- The limit is measured and applied per organization, never globally in a way that penalizes well-behaved tenants.
```

#### CA07 — Detail

```
Rules to be applied:
- The signup creates the organization, its seed roles (administrator, operator), and the first administrator user.
- All these steps occur in a single transaction: either all persist, or none persists.
- There is no visible intermediate state: there is never a "half-created" organization accessible.
- The initial administrator can only sign in after the entire transaction has been confirmed.
```

#### CA09 — Detail

```
Rules to be applied:
- The export includes only records whose organization is the requester's.
- No identifier, reference, or metadata of another organization appears in the package.
- The package is delivered in an open, readable format (LGPD portability), with the organization's main entities.
- The export generation respects the time limit defined in RNF-05.
```

#### CA10 — Detail

```
Rules to be applied:
- The erasure removes all records belonging to the target tenant, across all tenant-scoped tables.
- No record of any other organization is touched during the erasure.
- The erasure is explicitly confirmed by the organization's own administrator (irreversible action).
- A neighbouring tenant's record count stays unchanged before and after the erasure.
```

> **Technical note (does not go on the cards)**: the isolation safety net is implemented as a PostgreSQL Row-Level Security policy keyed on the session variable `app.current_org`, set per request from the authenticated user's organization. Deny-and-audit (CA04) maps to HTTP 404 (not 403) to avoid resource enumeration. This technical mapping is the responsibility of the Tasks (see §7 Traceability), not the AC.

### 4.5 Technical annex — Cross-tenant access matrix

> **Note**: this annex is a **technical derivation** of G-01/G-02 + CA01/CA02/CA04 for whoever implements the isolation layer. It is not AC detail in the "Rules to be applied:" style — it is an exhaustive truth table. In a real project, this becomes a `pytest.mark.parametrize` table.

```
Exhaustive matrix: session_org(S) accessing record_org(R)

       • S=A reads record(org=A)        → allowed (rows returned)
       • S=A reads record(org=B)        → denied (0 rows; 404; audit log)
       • S=A writes record(org=A)       → allowed
       • S=A writes record(org=B)       → denied (404; audit log)
       • S=A raw query without filter    → RLS scopes to org=A only (CA03)
       • S=None (no org bound)          → denied (RLS yields 0 rows)
       • S=A reads org A after A deleted → denied (CA11; resource gone)
```

---

## 5. User Stories (with BDD)

### US 1 — Apply isolation at the database layer

```
US Apply the per-organization isolation policy in the database (RLS)

Description (BDD):
  GIVEN that the session is bound to organization A
  AND there are records of organizations A and B in the same table
  WHEN a read query is executed WITHOUT the application filter
  THEN the database returns only records of organization A
  AND no record of organization B appears

Related to: CA01, CA03, G-01, RNF-01
Story Points: 5
```

### US 2 — Deny and audit cross-tenant access

```
US Deny and record an attempt to access another organization

Description (BDD):
  GIVEN that the authenticated user belongs to organization A
  AND a record belongs to organization B
  WHEN I GET /api/v1/pacientes/{id_of_B}/
  THEN the system responds as a non-existent resource (404)
  AND no data of organization B is exposed
  AND an entry is written to the audit log with the target organization

Related to: CA04, G-02, RNF-02
Story Points: 3
```

### US 3 — Atomic provisioning of a new organization

```
US Provision a new organization atomically

Description (BDD):
  GIVEN that provisioning creates organization + seed roles + administrator
  WHEN one of the steps fails (simulated via mock on the final step)
  THEN the entire transaction is rolled back
  AND no record of the incomplete organization remains
  AND the organization's identifier is not reserved

  Scenario 2: Successful provisioning
  GIVEN a valid new-organization signup
  WHEN provisioning completes
  THEN the organization, the seed roles, and the administrator exist
  AND the administrator can only sign in after the transaction is confirmed

Related to: CA07, CA08, G-03, RNF-04
Story Points: 5
```

### US 4 — Per-organization quota and limit

```
US Apply per-organization quota and usage limit

Description (BDD):
  GIVEN that organization A exceeds the request-per-minute limit
  WHEN A sends more requests in the same minute
  THEN A receives a limit-exceeded response
  AND organization B, well-behaved, keeps responding within the latency target

Related to: CA05, CA06, RNF-03
Story Points: 3
```

### US 5 — Export an organization's data (portability)

```
US Export an organization's data

Description (BDD):
  GIVEN that I am the administrator of organization A
  WHEN I request the export of my organization's data
  THEN I receive a package containing only records of organization A
  AND no identifier of another organization appears in the package
  AND the package is generated within the defined time limit

Related to: CA09, G-04, RNF-05
Story Points: 3
```

### US 6 — Erase an organization's data (right to be forgotten)

```
US Erase an organization's data

Description (BDD):
  GIVEN that I am the administrator of organization A
  AND there is a neighbouring organization B with N records
  WHEN I confirm the erasure of my organization
  THEN all records of organization A are removed
  AND organization B's record count stays N
  AND later accesses to organization A return as non-existent

Related to: CA10, CA11, G-04, RNF-06
Story Points: 5
```

---

## 6. Applied validation (Sommerville 5 + Falbo 7)

Applying [06-validacao.md](../references/06-validacao.md):

| Check | Application |
|---|---|
| **Validity** (Sommerville) | Confirmed with the product owner: "Yes — a tenant must never, under any circumstance, see another tenant's data" |
| **Consistency** | CA01/CA02 (application filter) and CA03 (RLS) are consistent — RLS reinforces, never contradicts, the application filter |
| **Completeness** | The initial set was missing CA11 (no reuse of a deleted org's identifier); discovered in review before coding |
| **Realism** | Implementable in PostgreSQL 16 RLS + Django session variables, no exotic dependency |
| **Verifiability** | Each AC has a corresponding pytest test in `tests/test_tenant_isolation.py` |
| **Complete (Falbo)** | ACs describe input (request + session org), rule (RLS + matrix), output (rows / 404 / audit log) |
| **Correct (Falbo)** | Validated with the product owner and the DPO (LGPD scope) |
| **Necessary (Falbo)** | Yes — a cross-tenant leak is an existential risk for the product |
| **Prioritizable (Falbo)** | Isolation 🔴 Immediate; export/erasure 🟡 Normal (regulatory but not launch-blocking) |
| **Verifiable (Falbo)** | Cross-tenant leak suite runs with the application filter disabled — 0 leaks required to pass |

---

## 7. Implemented traceability

Applying [07-mudanca-rastreabilidade.md](../references/07-mudanca-rastreabilidade.md):

```
Commit b7c3f02: feat(tenancy): per-organization isolation with RLS + atomic provisioning
├─ apps/tenancy/models.py
│    ├─ Organization (root tenant)
│    └─ TenantScopedModel (abstract: organization FK + filtered manager)
├─ apps/tenancy/db/policies.sql
│    └─ RLS policy USING (organization_id = current_setting('app.current_org')::uuid)
├─ apps/tenancy/middleware.py
│    └─ set_current_org(request) → SET app.current_org = user.organization_id
├─ apps/tenancy/services.py
│    ├─ provision_organization(payload) → Organization   [transaction.atomic]
│    │    └─ full rollback if any step fails (CA08)
│    ├─ export_organization(org) → ZIP   (only the tenant's records)
│    └─ delete_organization(org) → None  (tenant-scoped cascade + invalidates id)
├─ apps/tenancy/throttling.py
│    └─ PerOrganizationRateThrottle (600/min) + StorageQuotaGuard (5 GB)
├─ apps/tenancy/tests/test_tenant_isolation.py
│    ├─ test_read_returns_only_session_org (CA01)
│    ├─ test_write_binds_to_session_org (CA02)
│    ├─ test_rls_isolates_when_app_filter_disabled (CA03, RNF-01)
│    ├─ test_cross_tenant_read_returns_404_and_audits (CA04, RNF-02)
│    └─ test_cross_tenant_matrix (exhaustive parametrize)
├─ apps/tenancy/tests/test_provisioning.py
│    ├─ test_provision_is_atomic (CA07, RNF-04)
│    └─ test_provision_rollback_leaves_no_orphans (CA08)
├─ apps/tenancy/tests/test_quota.py
│    ├─ test_noisy_tenant_throttled_others_unaffected (CA05, RNF-03)
│    └─ test_storage_limit_blocks_writes (CA06)
└─ apps/tenancy/tests/test_lgpd.py
     ├─ test_export_contains_only_tenant_data (CA09, RNF-05)
     ├─ test_delete_removes_only_target_tenant (CA10, RNF-06)
     └─ test_deleted_org_id_not_reusable (CA11)
```

**Every AC has a traceable test**, every test describes a domain rule.

---

## 8. Ethical layer (*"SBC"* 002/2024)

Applying [09-etica-sbc.md](../references/09-etica-sbc.md):

| Principle | Application in the case |
|---|---|
| **§1.1 Well-being** | Patients and students trust that their records stay within one organization; isolation protects that trust |
| **§1.2 Avoid harm** | A cross-tenant leak of health or school records is grave, possibly irreversible harm; the RLS safety net reduces the risk |
| **§1.3 Honesty** | The declared promise ("your data is yours alone") now matches the implementation — not just an application filter |
| **§1.4 Non-discrimination** | Quota and limits apply per organization by the same rule; no tenant is privileged by who they are |
| **§2.5 Privacy (LGPD)** | Per-tenant export (portability) and erasure (right to be forgotten) are first-class features, not afterthoughts |
| **§2.9 Secure systems** | Defence in depth: application filter + database RLS + deny-and-audit + atomic provisioning |
| **§3.6 Care when modifying** | A forgotten filter no longer leaks data, because the database holds the line (regression risk neutralized) |

**Ethical decision**: chose a **shared base with RLS** over **a separate database per tenant**. Justification: at *"GestorPro"* scale (many small clinics/schools), a database-per-tenant model multiplies operational cost and migration risk; RLS gives a provable isolation boundary at the row level. Trade-off documented: shared base demands the RLS net be tested as rigorously as the application filter — hence RNF-01 runs with the application filter disabled.

---

## 9. Lessons from the case (applicable to future *"GestorPro"* features)

1. **Tenant isolation declared in the pitch** had become an implicit requirement; **making it explicit via ACs + a database safety net** was the missing step
2. **Defence in depth** beats a single filter: application manager + database RLS + deny-and-audit, all enforce the boundary
3. **Test the safety net with the first layer disabled** — RNF-01 only proves anything if the application filter is off during the leak suite
4. **Provisioning is part of the requirement** — "an organization is born atomically or not at all" (G-03) prevents the orphan-row class of bug at the source
5. **LGPD is a feature, not paperwork** — per-tenant export and erasure are testable ACs (CA09, CA10, CA11), traceable to RNF-05/RNF-06
6. **Quota protects the commons** — a per-organization limit (RNF-03) keeps one noisy tenant from degrading every other tenant on the shared base

---

## 10. Applying this template to next *"GestorPro"* features

For any new tenant-scoped feature (e.g., "appointment scheduling", "grade book"), reuse this structure:

1. **Stakeholders explicitly identified** (including the data subject and the DPO)
2. **AS-IS / TO-BE** documented (clear gap, especially the "forgotten filter" risk)
3. **Business rules (G) stated as invariants** (`G-01` belonging, `G-02` no cross-tenant access)
4. **Declarative ACs with stable IDs** (`CANN`), grouped by theme
5. **NFRs always quantitative** with a measurement method, optionally an EARS body
6. **User Stories slicing ACs into incremental slices** with BDD in the description
7. **Validation against Falbo 7 + Sommerville 5** before coding
8. **Ethical layer**: concrete question — whose privacy is at stake, and what happens on a leak?
9. **Defence in depth**: enforce the tenant invariant in ≥2 independent layers (application + database)
10. **Tests traceable to the ACs**, with the cross-tenant suite running against the database net alone

In multi-tenant SaaS like *"GestorPro"*, this level of RE ceremony **prevents the one bug you cannot recover from** — a cross-tenant data leak — by turning "remember the filter" into a provable, tested invariant.
