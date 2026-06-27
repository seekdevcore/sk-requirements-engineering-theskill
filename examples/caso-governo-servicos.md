# Worked Example — In-Person Service Booking in the *"Portal do Cidadão"* Project

> Fictional but realistic case from the *"Portal do Cidadão"* project (Brazilian municipal digital-government service; Django 5 + DRF + Next.js 15). Shows how a **public-sector** feature maps to the skill's RE framework — useful for teams building citizen-facing services where accessibility (*"eMAG"*/WCAG AA), data minimization (*"LGPD"*), audit trails, and non-digital fallback are not "nice-to-haves" but legal and ethical obligations. Reference commit (illustrative): `b7f3a90` (feat(booking): confirmed identity + LGPD minimization + low-connectivity channel).

---

## 1. Context and problem

**Public-service problem**: the municipality offers in-person services (issuing duplicate documents, booking appointments at health clinics) across several service units. Historically the citizen had to physically queue at dawn to get one of the limited daily slots — first-come, first-served, no remote option. The *"Portal do Cidadão"* aims to replace the dawn queue with an online appointment booking.

**Diagnosis**: a naive booking form would *solve the queue but create new exclusions*. An elderly citizen with low connectivity or no smartphone would simply be locked out of a service they are legally entitled to. Equally, a careless form would over-collect personal data (CPF, address, health condition) without declared purpose or retention limit — an *"LGPD"* violation waiting to happen. **The implicit requirement** here is that going digital must not narrow access nor weaken the citizen's rights — the kind of constraint ethnography and stakeholder analysis surface (see [02-elicitacao.md §7](../references/02-elicitacao.md)). Once discussed, it became explicit through the RNFs and business rules below.

---

## 2. Stakeholders

Applying Wiegers 2003 (see [01-fundamentos.md §5](../references/01-fundamentos.md)):

| Stakeholder | Interest |
|---|---|
| **Citizen (general)** | Book a slot remotely, without dawn queues, with a reliable confirmation |
| **Elderly / low-connectivity citizen** | Reach the service without depending on a fast connection or a smartphone; have a non-digital fallback |
| **Unit clerk** | Receive a clean, identity-confirmed schedule; not handle no-shows or duplicate bookings |
| **Public manager of the department** | Reduce queues, prove transparency, comply with *"LGPD"* and accessibility law |
| **Data Protection Officer (DPO)** | Ensure each personal field has declared purpose, consent, and a retention deadline |
| **Auditor / comptroller** | Inspect a complete trail of who scheduled, changed, or cancelled what, and when |
| **Person with a disability** | Operate the whole flow by keyboard and screen reader, with sufficient contrast |

---

## 3. AS-IS → TO-BE analysis

Applying the analysis from [08-analista-negocios.md §3](../references/08-analista-negocios.md):

### AS-IS (before the *"Portal do Cidadão"*)

```
Citizen → goes in person to the unit at dawn
  → takes a physical ticket by order of arrival
  → the day's slots run out; many go back home without service
  → personal data jotted on paper, with no disposal deadline
  → the elderly and those who live far away are the most penalized
```

**Pains**:

- Access depends on physical presence at dawn — excludes the elderly, workers, and people far from the unit
- No remote confirmation; the citizen never knows if there will be a slot
- Personal data on paper, with no declared purpose nor retention limit
- No auditable record of who got served and why

### TO-BE

```
Citizen → accesses the Portal (or calls the call centre — fallback channel)
  → confirms identity → chooses service, unit, and available time slot
  → receives confirmation (with a protocol number) by e-mail/SMS
  → only the necessary data is collected, with declared purpose and retention period
  → every action is logged in a consultable audit trail
```

### GAP analysis

| Gap | Solution |
|---|---|
| Booking with no identity confirmation enables fraud and no-shows | RF: mandatory identity confirmation before booking; G: "No booking without confirmation of the citizen's identity" |
| Form over-collects personal data with no purpose or deadline | RNF: minimization + consent RF; G: "Personal data collected has a declared purpose and retention period" |
| Digital-only path excludes low-connectivity / non-smartphone citizens | availability RNF + fallback-channel RF (telephone call centre) |
| Flow unusable by screen reader / keyboard only | accessibility RNF (*"eMAG"*/WCAG AA) + accessibility CA |
| Administrative actions leave no inspectable trace | audit-trail RNF; every administrative action logged and consultable |

---

## 4. Feature: In-Person Service Booking

**Feature description (client-deliverable):**

Allows the citizen to remotely book a time slot for in-person service at a municipal unit (for example, issuing a duplicate document or booking an appointment at a health clinic), replacing the dawn queue. The booking is only confirmed after the citizen's identity is confirmed, and the confirmation is sent with a protocol number. The system collects only the data strictly necessary for the service, always with declared purpose, explicit consent, and a defined retention period — the citizen can view and request the deletion of their data. So as not to exclude those with poor internet or no smartphone, there is a fallback channel (telephone call centre) that records the same booking in the system. The whole flow is operable by keyboard and screen reader, with sufficient contrast (*"eMAG"*/WCAG AA). Every administrative action (create, reschedule, cancel, attend) is logged in an audit trail consultable by the comptroller.

> This description is what goes on the backlog Feature card. It is **written in business language**, readable by any stakeholder — including a public manager who is not technical. The ACs below formalize the testable rules; BDD appears only in the User Stories (§5).

### 4.1 Acceptance Criteria (declarative style)

11 ACs, **grouped by theme** (Rule 7 of [05-convencoes-interpop.md](../references/05-convencoes-interpop.md)). ACs with **`[...]`** at the end of the title must be read together with the detail in §4.2.

#### 📋 CA - Identity and slot booking

| ID | Description | Detail? |
|---|---|---|
| `CA01` | No slot is booked unless the citizen's identity has been confirmed beforehand **[...]** | ✅ |
| `CA02` | The same citizen cannot have two active bookings for the same service at the same unit **[...]** | ✅ |
| `CA03` | When confirming the booking, the citizen receives a protocol number and a confirmation through a chosen channel (e-mail or SMS). | — |
| `CA04` | A slot already booked by another citizen stops appearing as available. | — |

#### 📋 CA - Citizen privacy and data (LGPD)

| ID | Description | Detail? |
|---|---|---|
| `CA05` | The system collects only the data necessary for the service; no extra field is required **[...]** | ✅ |
| `CA06` | Each personal data item collected has a declared purpose and a retention period visible to the citizen at the moment of collection **[...]** | ✅ |
| `CA07` | The citizen can view and request the deletion of their personal data at any time **[...]** | ✅ |

#### 📋 CA - Accessibility and inclusion

| ID | Description | Detail? |
|---|---|---|
| `CA08` | The entire booking flow is operable by keyboard alone and announced correctly by a screen reader **[...]** | ✅ |
| `CA09` | There is a non-digital fallback channel (telephone call centre) that records the same booking in the system **[...]** | ✅ |

#### 📋 CA - Transparency and audit trail

| ID | Description | Detail? |
|---|---|---|
| `CA10` | Every administrative action on a booking (create, reschedule, cancel, attend) is logged with author, date, and reason **[...]** | ✅ |
| `CA11` | The audit trail is consultable by the comptroller and cannot be edited or deleted by an ordinary clerk. | — |

### 4.2 Detail of ACs with `[...]`

Each block below is what appears in the **item body** in the backlog (AC Description field), following the `Rules to be applied:` + bullets convention.

#### CA01 — Detail

```
Rules to be applied:
- The citizen's identity is confirmed before any booking is created.
- If identity confirmation fails, no slot is blocked or booked.
- The slot only leaves the set of available slots after the booking is confirmed with a confirmed identity.
- The booking is linked to the confirmed identity, allowing later lookup and cancellation by the citizen themselves.
```

#### CA02 — Detail

```
Rules to be applied:
- A citizen with an active booking for the same service at the same unit cannot create a second active booking.
- The duplicate booking attempt is refused with the message "You already have an active booking for this service at this unit".
- Bookings for different services (or different units) are allowed in parallel.
- After the service, cancellation, or rescheduling, the booking stops counting as active and a new one can be created.
```

#### CA05 — Detail

```
Rules to be applied:
- The form requests only what is necessary for the chosen service (e.g., name, identification document, contact for confirmation).
- No sensitive-data field is required when the service does not need it.
- When a health service requires sensitive data (e.g., specialty), that data is requested in a prominent and justified manner.
- Optional fields are clearly marked as optional; the citizen can complete the booking without filling them in.
```

#### CA06 — Detail

```
Rules to be applied:
- At the moment of collection, each data item shows what it will be used for (purpose) and how long it will be kept (retention period).
- The citizen gives explicit consent before the collection is carried out.
- The declared purpose cannot be broadened later without new consent.
- Once the retention period has elapsed, the data is automatically discarded or anonymized.
```

#### CA07 — Detail

```
Rules to be applied:
- The citizen has an area where they view all the personal data the system keeps about them.
- The citizen can request the deletion of their data; the request is logged and fulfilled within the legal deadline.
- Deletion does not erase records that the law requires to be preserved (e.g., the audit trail of a service already provided), but anonymizes the personal link when possible.
- The response to the access/deletion request is confirmed to the citizen through a contact channel.
```

#### CA08 — Detail

```
Rules to be applied:
- Every control in the flow (choose service, unit, slot, confirm) is reachable and actionable by keyboard alone, in logical order.
- Each field and button has a label announced correctly by the screen reader.
- Error and success messages are announced to the screen reader, not just displayed visually.
- The contrast between text and background meets the minimum required for comfortable reading.
```

> **Technical note (does not go on the CA08 card)**: the contrast minimum maps to a ratio of at least 4.5:1 for normal text (WCAG AA), and screen-reader announcements map to `aria-live` regions plus correct `label` association. This technical mapping is the responsibility of the Tasks (see §7 Traceability), not the AC.

#### CA09 — Detail

```
Rules to be applied:
- There is a telephone call centre where a clerk records the booking on behalf of the citizen.
- The booking created by the call centre is the same system record — it appears in the same unit schedule and generates the same protocol number.
- Identity confirmation by the call centre follows a verification equivalent to that of the digital channel.
- No citizen is left without access to the service for lacking adequate internet or a smartphone.
```

#### CA10 — Detail

```
Rules to be applied:
- Every creation, rescheduling, cancellation, and marking of service generates a record in the audit trail.
- Each record keeps who performed the action, when, and the reason (when applicable, e.g., the cancellation reason).
- The record is immutable once created: corrections enter as new records, they do not overwrite.
- The trail allows the complete history of a booking to be reconstructed.
```

### 4.3 Technical annex — Decision table for `can_book(citizen, service, unit)`

> **Note**: this annex is a **technical derivation** of CA01 + CA02 for whoever implements the booking guard. It is not AC detail in the "Rules to be applied:" style — it is an exhaustive decision table. In a real project, this becomes a comment in the code or a test table (`pytest.mark.parametrize`).

```
Decision table can_book(citizen, service, unit) → (allowed, reason)

  • identity NOT confirmed                                       → (False, "identity_not_confirmed")
  • identity confirmed, no active booking, slot available        → (True,  "ok")
  • identity confirmed, already has active booking same service  → (False, "duplicate")
  • identity confirmed, active booking on ANOTHER service        → (True,  "ok")
  • identity confirmed, no slot available at that time           → (False, "no_slot")
  • previous booking already attended/cancelled (not active)     → (True,  "ok")
```

---

## 5. User Stories (with BDD)

### US 1 — Confirm identity before reserving the slot

```
US Confirm the citizen's identity before reserving the slot

Description (BDD):
  Given the citizen has chosen a service, unit, and time slot
  And their identity has NOT yet been confirmed
  When they try to confirm the booking
  Then the system does NOT create the booking
  And the slot remains available to other citizens
  And the system requests identity confirmation

  Scenario 2: Identity confirmed
  Given the citizen's identity has been confirmed
  And there is a slot available at the chosen time
  When they confirm the booking
  Then the system creates the booking linked to the identity
  And the slot stops appearing as available
  And the citizen receives a confirmation protocol number

Related to: CA01, CA03, CA04
Story Points: 5
```

### US 2 — Block duplicate active booking

```
US Prevent a duplicate active booking for the same service at the same unit

Description (BDD):
  Given the citizen already has an active booking for "duplicate document" at the "Centro" unit
  When they try to create another booking for the same service at the same unit
  Then the system refuses and displays "You already have an active booking for this service at this unit"
  But a booking for "health-clinic appointment" at the same unit is created normally

Related to: CA02
Story Points: 3
```

### US 3 — Collect only what is necessary, with declared purpose and retention

```
US Collect minimal data with declared purpose and retention period

Description (BDD):
  Given the citizen fills in the booking form
  When a personal data item is requested
  Then the system displays the purpose and the retention period of that data item
  And only carries out the collection after explicit consent
  And no field beyond what the service needs is required

Related to: CA05, CA06
Story Points: 5
```

### US 4 — Citizen accesses and deletes their own data

```
US Allow the citizen to view and request the deletion of their own data

Description (BDD):
  Given the citizen accesses the privacy area
  When they request to see the data the system keeps about them
  Then the system lists all the personal data stored

  Scenario 2: Deletion request
  Given the citizen has requested the deletion of their data
  When the request is processed
  Then the personal data is deleted or anonymized
  And the records the law requires to be preserved have their personal link anonymized
  And the citizen receives confirmation that the request was fulfilled

Related to: CA07
Story Points: 5
```

### US 5 — Whole flow operable by keyboard and screen reader

```
US Make the booking flow accessible by keyboard and screen reader

Description (BDD):
  Given the citizen navigates using only the keyboard
  When they go through the booking flow
  Then all controls are reachable and actionable in logical order
  And each field and button is announced correctly by the screen reader
  And error and success messages are announced, not just displayed

Related to: CA08
Story Points: 5
```

### US 6 — Non-digital fallback channel

```
US Record a booking through the telephone call centre (low-connectivity channel)

Description (BDD):
  Given a citizen without adequate internet calls the call centre
  When the clerk records the booking on behalf of the citizen
  Then the system creates the same booking record, with the same protocol number
  And the booking appears in the unit schedule the same as the digital channel's
  And the citizen's identity is confirmed by an equivalent verification

Related to: CA09
Story Points: 3
```

### US 7 — Immutable audit trail of administrative actions

```
US Log every administrative action in an immutable audit trail

Description (BDD):
  Given a clerk cancels a booking stating the reason
  When the action is executed
  Then a record is created in the trail with author, date, and reason
  And the record cannot be edited or deleted by an ordinary clerk
  And the comptroller can reconstruct the entire history of the booking

Related to: CA10, CA11
Story Points: 3
```

---

## 6. Applied validation (Sommerville 5 + Falbo 7)

Applying [06-validacao.md](../references/06-validacao.md):

| Check | Application |
|---|---|
| **Validity** (Sommerville) | Confirmed with the manager and DPO: "Yes, going digital cannot exclude the elderly nor over-collect data" |
| **Consistency** | CA09 (fallback) and CA01 (identity) are consistent — the call centre confirms identity by an equivalent verification |
| **Completeness** | The initial set lacked CA07 (access/deletion right); discovered in review with the DPO before coding |
| **Realism** | Implementable in Django 5 + DRF + Next.js 15 without external dependency; fallback reuses the same booking service |
| **Verifiability** | Each AC has a corresponding test in `tests/test_agendamento.py` and `tests/test_acessibilidade.py` |
| **Complete (Falbo)** | ACs describe input (booking request), rule (identity + minimization + access), output (reservation + protocol + audit record) |
| **Correct (Falbo)** | Validated with the public manager, the DPO, and an accessibility reviewer |
| **Necessary (Falbo)** | Yes — legal obligation (*"LGPD"* + accessibility law) and real exclusion risk |
| **Prioritizable (Falbo)** | 🔴 Immediate for CA01/CA06/CA08 (legal/ethical), 🟠 High for CA09, 🟡 Normal for CA03 |
| **Verifiable (Falbo)** | Automated accessibility checks + booking tests pass before release |

---

## 7. Implemented traceability

Applying [07-mudanca-rastreabilidade.md](../references/07-mudanca-rastreabilidade.md):

```
Commit b7f3a90: feat(booking): confirmed identity + LGPD minimization + low-connectivity channel
├─ apps/agendamento/services.py
│    ├─ pode_reservar(cidadao, servico, unidade) → (bool, motivo)
│    │    └─ requires confirmed identity and no duplicate active booking (CA01, CA02)
│    ├─ reservar(cidadao, servico, unidade, horario) → Agendamento
│    │    └─ creates booking, issues protocol number, sends confirmation (CA03, CA04)
│    └─ registrar_via_central(atendente, cidadao, ...) → Agendamento (CA09)
├─ apps/privacidade/models.py
│    ├─ DadoColetado.finalidade / .prazo_retencao (CA06)
│    └─ Consentimento.registrar(cidadao, finalidade) (CA06)
├─ apps/privacidade/services.py
│    ├─ exportar_dados_do_cidadao(cidadao) (CA07)
│    └─ excluir_ou_anonimizar(cidadao) → preserves legal trail (CA07)
├─ apps/auditoria/models.py
│    └─ RegistroAuditoria (append-only; no update/delete for a clerk) (CA10, CA11)
├─ web/components/agendamento/ (Next.js)
│    └─ keyboard navigation + aria-live + AA contrast (CA08)
├─ apps/agendamento/tests/test_agendamento.py
│    ├─ test_nao_reserva_sem_identidade_confirmada (CA01)
│    ├─ test_horario_some_apos_reserva (CA04)
│    ├─ test_reserva_duplicada_recusada (CA02)
│    ├─ test_servico_diferente_permitido (CA02)
│    ├─ test_protocolo_e_confirmacao_enviados (CA03)
│    └─ test_central_cria_mesmo_registro (CA09)
├─ apps/privacidade/tests/test_lgpd.py
│    ├─ test_coleta_minima_sem_campo_extra (CA05)
│    ├─ test_finalidade_e_retencao_exibidas (CA06)
│    ├─ test_descarte_apos_prazo_retencao (CA06)
│    ├─ test_cidadao_consulta_proprios_dados (CA07)
│    └─ test_exclusao_anonimiza_preservando_trilha (CA07)
├─ apps/auditoria/tests/test_auditoria.py
│    ├─ test_acao_administrativa_gera_registro (CA10)
│    └─ test_atendente_nao_edita_nem_apaga_trilha (CA11)
└─ web/tests/test_acessibilidade.py
     ├─ test_fluxo_navegavel_por_teclado (CA08)
     └─ test_contraste_minimo_AA (CA08)
```

**Every AC has a traceable test**, every test describes a domain rule.

### RNF (always quantitative + measurement method; EARS optional)

| ID | RNF | Quantitative target + measurement | EARS (optional) |
|---|---|---|---|
| `RNF-01` | Accessibility | 100% of critical flows navigable by keyboard; normal-text contrast ≥ 4.5:1; 0 critical violations in the automated auditor (*"eMAG"*/WCAG AA). Measurement: axe-core in CI + manual review with a screen reader. | While a citizen navigates by keyboard alone, the *"Portal do Cidadão"* shall keep all controls reachable and announced. |
| `RNF-02` | Privacy / minimization | 0 fields collected without declared purpose and period; data discarded/anonymized within 24 h after the retention period. Measurement: audited data inventory + purge job verified in test. | When the retention period of a data item is reached, the *"Portal do Cidadão"* shall discard or anonymize the data within 24 h. |
| `RNF-03` | Availability / inclusion | Booking-service availability ≥ 99.5% monthly; telephone fallback channel available 100% of service hours. Measurement: uptime monitor + call-centre operation log. | When the digital channel is unavailable, the *"Portal do Cidadão"* shall keep booking operable through the telephone call centre. |
| `RNF-04` | Audit trail | 100% of administrative actions logged; append-only trail consultable in ≤ 3 s per booking. Measurement: audit test coverage + lookup-time measurement. | When an administrative action occurs on a booking, the *"Portal do Cidadão"* shall log author, date, and reason immutably. |

### G (business rules / global invariants)

| ID | Global rule |
|---|---|
| `G-01` | No booking without confirmation of the citizen's identity. |
| `G-02` | Every personal data item collected has a declared purpose and a retention period. |
| `G-03` | No citizen is left without access to the service for lack of internet or a smartphone (fallback guaranteed). |
| `G-04` | Every administrative action is logged immutably and is consultable by the comptroller. |

---

## 8. Ethical layer (*"SBC"* 002/2024)

Applying [09-etica-sbc.md](../references/09-etica-sbc.md):

| Principle | Application in the case |
|---|---|
| **§1.1 Well-being** | Replacing the dawn queue with remote booking reduces hardship, especially for the elderly and distant residents |
| **§1.2 Avoid harm** | Identity confirmation prevents fraudulent bookings that would deny slots to legitimate citizens |
| **§1.3 Honesty** | Each personal field declares purpose and retention; nothing is collected silently |
| **§1.4 Non-discrimination** | The non-digital fallback guarantees that low-connectivity citizens are not second-class users |
| **§2.9 Secure systems** | Defence in depth: identity guard (service) + minimization (privacy model) + append-only audit trail |
| **§3.6 Care when modifying** | The fallback channel writes to the same booking service, so future changes cannot silently exclude the phone path |

**Ethical decision**: chose a **non-digital fallback as a first-class requirement** (CA09 + RNF-03) over a **digital-only MVP** that would have shipped faster. Justification: a public service may not exclude citizens for lack of connectivity — inclusion outranks delivery speed here. Trade-off documented.

---

## 9. Lessons from the case (applicable to future *"Portal do Cidadão"* features)

1. **Going digital is not automatically inclusive** — without CA09 (fallback), the portal would have *narrowed* access for the people who needed it most
2. **LGPD is a requirement, not an afterthought** — purpose + retention + consent + access/deletion belong in the ACs (CA05..CA07), not in a privacy policy nobody reads
3. **Accessibility has a measurable target** — RNF-01 (keyboard 100%, contrast ≥ 4.5:1, 0 critical axe violation) turns "be accessible" into something a CI pipeline can fail on
4. **The audit trail is part of the requirement** — public accountability means every administrative action is reconstructable (CA10/CA11), and the trail must be append-only
5. **A business rule (G) outranks a screen** — G-01 (no booking without identity) and G-03 (no one excluded) are invariants every future feature inherits
6. **Identity confirmation came from a risk, not a screen** — making it explicit as CA01 prevented a whole class of fraud and no-shows before a line was coded

---

## 10. Applying this template to next *"Portal do Cidadão"* features

For any new feature (e.g., "service-protocol lookup"), reuse this structure:

1. **Stakeholders explicitly identified** — and always include the most-excluded citizen (elderly, low connectivity, disability)
2. **AS-IS / TO-BE** documented (clear gap), naming who today is left out
3. **Declarative ACs with stable IDs** (`CA-PROTO-01`, `CA-PROTO-02`, ...), grouped by theme
4. **User Stories slicing ACs into incremental slices** with BDD in the description
5. **RNFs always quantitative + measurement method**, optionally in EARS; never "be fast/accessible/private" without a number
6. **Business rules (G)** capture the invariants — identity, purpose-declared data, inclusion, auditability
7. **Validation against Falbo 7 + Sommerville 5** before coding, with the DPO and an accessibility reviewer in the room
8. **Ethical layer**: concrete question — who can be *excluded* or *harmed* by this feature, and what is the fallback?
9. **Defence in depth**: apply each invariant in ≥2 independent layers (service guard + data model + audit)
10. **Tests traceable to the ACs** (booking, *"LGPD"*, accessibility, audit), not code-oriented tests

In public-sector projects, this level of RE ceremony is not bureaucracy — it is how the team **proves** to citizens, the DPO, and the comptroller that the service is inclusive, lawful, and accountable by design.
