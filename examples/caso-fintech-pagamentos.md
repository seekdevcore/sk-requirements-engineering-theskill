# Worked Example — Card Charging and Wallet Balance in the *"PagLeve"* Project

> Fictional but realistic case from the *"PagLeve"* project (Brazilian fintech — digital wallet that charges cards and holds user balance; Django 5 + DRF + React 19 + an external acquirer). Shows how a **payments-domain** feature maps to the skill's RE framework, with the domain differential made explicit: card-data protection (*"PCI"* — Payment Card Industry data-security standard), charge idempotency, reconciliation, anti-fraud limits, strong authentication, and an immutable audit trail. Reference commit: `a7f31c0` (feat(payments): idempotent charge on a tokenized card + audit trail).
>
> **Note on language**: this worked example is written in **en-CA** (the skill's default language). Code symbols, file paths, identifiers, and commit-message conventions are kept verbatim; Brazilian domain terms (*"PagLeve"*, *"LGPD"*, *"PIX"*) are kept in their original form.

---

## 1. Context and problem

**Business problem**: *"PagLeve"* lets a user pay an *order* with a credit card and keeps the remaining money as wallet balance for later use. The first version stored, in its own database, the full card number plus the security code (CVV) "to make the next charge easier", and re-tried failed charges by simply firing the request again. Two real incidents followed: a duplicate charge on a customer whose first request timed out (the customer was billed twice for one *order*), and a security review flagging that storing CVV is forbidden by the card-network rules and turns the whole database into *"PCI"* scope.

**Diagnosis**: the feature mixed two undocumented-but-critical requirements that the happy-path spec never named — **a charge must never bill the customer twice for the same attempt**, and **the system must never persist card secrets**. Both are the kind of requirement that surfaces only when you ask "what is the worst money/legal outcome here?" (see [02-elicitacao.md §7](../references/02-elicitacao.md)). Once raised, they became explicit FRs, NFRs, and invariants.

---

## 2. Stakeholders

Applying Wiegers 2003 (see [01-fundamentos.md §5](../references/01-fundamentos.md)):

| Stakeholder | Interest |
|---|---|
| **Payer (cardholder)** | Be charged exactly once per *order*; never have card secrets leaked; recover money on failure |
| **Merchant / order owner** | Receive the value of a confirmed *order*; trust that a "paid" status is real money |
| **Founder / owner of *"PagLeve"*** | No double-charge incidents; stay out of unnecessary *"PCI"* scope; survive an acquirer audit |
| **Acquirer (external partner)** | Receive well-formed, idempotent charge requests; have every movement reconcile against its statement |
| **Anti-fraud team** | Block charge floods and suspicious high-value operations before money moves |
| **Auditor / regulator (*"Bacen"* — Central Bank of Brazil, *"PCI-QSA"*)** | Immutable, complete log of who touched which financial datum, when, and why |
| **Customer support** | Explain to a customer what happened to a charge without ever reading the full card number |

---

## 3. AS-IS → TO-BE analysis

Applying the analysis from [08-analista-negocios.md §3](../references/08-analista-negocios.md):

### AS-IS (before commit a7f31c0)

```
Payer → POST /payments/charge { order, card_number, cvv, amount }
  → System stores card_number + cvv in plaintext in its own database
  → System calls the acquirer
  → Timeout on the response → app re-tries the same POST
  → Acquirer processes the 2nd call as a new charge
  → Payer is billed TWICE for the same order
  → Balance and acquirer statement diverge; nobody detects it in time
```

**Pains**:

- Card secret (CVV) and full PAN stored in the application database — forbidden by network rules, expands PCI scope to everything
- Re-tried charge produces a second real billing — no notion of "same attempt"
- No reconciliation: internal movements and the acquirer statement could silently diverge
- No record of who accessed a given customer's card data

### TO-BE

```
Payer → POST /payments/charge
          Idempotency-Key: <attempt-key>
          { order, card_token, amount }
  → System NEVER receives or stores CVV; the number became a token ("vault")
  → Same Idempotency-Key already seen → returns the SAME result, no re-charge
  → New key → charges once, records a movement traceable to the order
  → Access to the financial datum enters the immutable audit trail
  → Daily reconciliation checks every movement against the acquirer statement
```

### GAP analysis

| Gap | Solution |
|---|---|
| CVV/PAN stored in app DB | RNF-01 + G-02: card secrets never persisted; PAN replaced by token, shown masked |
| Re-try bills twice | RF-02 + RNF-02: charge keyed by `Idempotency-Key`; same key returns same result |
| Internal balance vs acquirer statement can diverge | RF-04 + RNF-03: daily reconciliation; every movement traceable to an *order* |
| No anti-fraud ceiling / weak auth on sensitive ops | RNF-04 + RNF-05: block after N attempts; value above threshold requires 2nd factor |
| No record of financial-data access | RNF-06 + G-04: immutable audit trail on every access |
| Balance could go negative on race | G-01: balance invariant never below zero (atomic debit) |

---

## 4. Feature: Card charging and balance keeping

**Feature description (client-deliverable):**

Lets the *payer* pay an *order* with a credit card and keep the change as balance in the *"PagLeve"* wallet. The charge is made exactly once per attempt: if the same attempt is re-sent (timeout, double tap, reprocessing), the customer is never billed twice. Sensitive card data stays protected — the system never stores the security code or the card track, replaces the number with a "vault" (token), and always displays the number masked. Every money movement is traceable back to the *order* that originated it and matches the acquirer statement in the daily reconciliation. Sensitive operations go through an anti-fraud limit and, above a certain value, through a second identity confirmation. Every access to a financial datum is recorded in a way that cannot be erased or altered. The deliverable to the client (*"Helena"*, the project's founder/owner) is the guarantee that no customer is billed twice, no card secret is stored, and no balance goes negative.

> This description is what goes on the OpenProject Feature card. It is **written in business language**, readable by any stakeholder — including the acquirer's auditor. The ACs below formalize the testable rules; BDD appears only in the User Stories (§5).

### 4.0 Goals (G) and Non-Functional Requirements (NFR)

> Domain differential. **Goals (G)** are invariants the system must never violate. **NFRs are always quantitative** with a measurement method; EARS phrasing is offered as the optional precision layer (see [11-ears.md](../references/11-ears.md)). The `[...]` convention links to detail.

#### 🎯 Goals (invariants)

| ID | Goal | Priority |
|---|---|---|
| `G-01` | No wallet balance ever goes negative at any moment. | 🔴 Immediate |
| `G-02` | No card secret (security code, track, PIN) is stored anywhere in the system. | 🔴 Immediate |
| `G-03` | Every charge has an origin traceable to a single *order*. | 🟠 High |
| `G-04` | Every access to a financial datum is recorded immutably. | 🟠 High |

#### ⚙️ Non-Functional Requirements (quantitative)

| ID | NFR (business language) | Measurement | Priority |
|---|---|---|---|
| `RNF-01` | The card number is never displayed in full: at most the last 4 digits appear; the rest is masked. | Inspection of payloads and screens; log scan for PAN (0 occurrences). | 🔴 Immediate |
| `RNF-02` | The same charge attempt (same idempotency key) results in at most **1** real charge, even with re-sends. | Re-send test: N=50 re-sends of the same key → 1 debit at the acquirer. | 🔴 Immediate |
| `RNF-03` | In the daily reconciliation, **100%** of the day's movements match the acquirer statement; a divergence > 0 raises an alert the same day. | Daily job compares movements × statement; counts divergences. | 🟠 High |
| `RNF-04` | After **5** refused charge attempts on the same card within **10** minutes, the card is blocked from new attempts for **30** minutes. | Attempt load test; verifies the block on the 6th. | 🟠 High |
| `RNF-05` | A charge of a value above **R$ 2,000.00** requires a second identity confirmation (2nd factor) before moving money. | Test with a value below/above the threshold; verifies the 2nd-factor requirement. | 🟠 High |
| `RNF-06` | Every read or write access to a financial datum generates an audit record that cannot be altered or erased **[...]** | An UPDATE/DELETE attempt on the audit record fails; append-only verified. | 🟠 High |

> **RNF-02 in EARS (optional)**: `WHEN a charge request arrives with an already-seen idempotency key, THE SYSTEM SHALL return the result of the original charge without triggering a new charge at the acquirer.`
> **RNF-05 in EARS (optional)**: `IF the charge value is greater than R$ 2,000.00, THEN THE SYSTEM SHALL require a second identity confirmation before moving money.`

### 4.1 Acceptance Criteria (declarative style)

11 ACs, **grouped by theme** (Rule 7 of [05-convencoes-interpop.md](../references/05-convencoes-interpop.md)). ACs with **`[...]`** must be read together with the detail in §4.2.

#### 📋 CA - Card-data protection

| ID | Description | Detail? |
|---|---|---|
| `CA01` | On any attempt to store the card's security code (CVV), track, or PIN, the system rejects the operation and no secret is persisted. | — |
| `CA02` | The card number is replaced by a "vault" (token) before any persistence; the original number is not kept. | — |
| `CA03` | In every display (screen, receipt, log, support), the card number appears masked, with at most the last 4 digits. | — |

#### 📋 CA - Idempotent charge

| ID | Description | Detail? |
|---|---|---|
| `CA04` | Each charge attempt carries an idempotency key; the same key never generates more than one real charge **[...]** | ✅ |
| `CA05` | On receiving the charge, the system responds with one of three business results **[...]** | ✅ |
| `CA06` | The charge is transactional: if it fails between recording the movement and updating the balance, both are rolled back — no partial state ever remains. | — |

#### 📋 CA - Balance, traceability and reconciliation

| ID | Description | Detail? |
|---|---|---|
| `CA07` | The wallet balance never goes negative; a debit that would leave the balance negative is refused. | — |
| `CA08` | Every money movement points to exactly one source *order* **[...]** | ✅ |
| `CA09` | The daily reconciliation checks every movement against the acquirer statement and flags any divergence. | — |

#### 📋 CA - Anti-fraud, strong authentication and audit

| ID | Description | Detail? |
|---|---|---|
| `CA10` | Charges refused in sequence on the same card lead to a temporary block, and high values require a second factor **[...]** | ✅ |
| `CA11` | Every access to a financial datum enters the immutable audit trail, with who, when, and what. | — |

### 4.2 Detail of ACs with `[...]`

Each block below is what appears in the **item body** in OpenProject (AC Description field), following the `Rules to be applied:` + bullets convention.

#### CA04 — Detail

```
Rules to be applied:
- Every charge request carries an idempotency key unique to the attempt.
- If the key has never been seen, the system charges once and stores the result associated with the key.
- If the key has already been seen, the system returns the SAME previous result, without triggering a new charge.
- A re-send due to timeout, double tap, or reprocessing NEVER generates a second charge.
```

#### CA05 — Detail

```
Rules to be applied:
- When the card is accepted and there is authorization, the system confirms the charge (operation accepted) and moves the money.
- When the card is refused by the acquirer, the system reports "Charge refused by the operator" and no balance is altered.
- When the operation violates a PagLeve rule (no required 2nd factor, card blocked by anti-fraud, invalid card data), the system rejects it with the message of the violated rule and no money moves.
- In all rejection cases, no financial movement is created and no balance is altered.
```

> **Technical note (does not go on the CA05 card)**: the 3 business results map respectively to HTTP 201, 402 and 422 on `POST /api/v1/payments/charge`. This technical mapping is the responsibility of the Tasks (see §7), not the AC.

#### CA08 — Detail

```
Rules to be applied:
- Every money movement (charge, refund, balance use) references exactly one source order.
- There is no "orphan" movement without an associated order.
- The customer receipt and the reconciliation report derive from this movement↔order relationship.
- The relationship is sufficient to reconstruct, from an order, all the movements it generated.
```

#### CA10 — Detail

```
Rules to be applied:
- After 5 refused charges on the same card within 10 minutes, the card is blocked from new attempts for 30 minutes.
- During the block, new attempts with that card are refused by the anti-fraud rule, without calling the acquirer.
- A charge of a value above R$ 2,000.00 requires a second identity confirmation before moving money.
- If the second factor is not satisfied, the charge is rejected and no money moves.
```

#### RNF-06 — Detail

```
Rules to be applied:
- Every read or write of a financial datum (tokenized card, movement, balance) generates an audit record.
- The record stores who accessed it, when, which resource, and which action.
- The record is append-only: attempts to alter or erase an audit record fail.
- The trail is sufficient for an external auditor to reconstruct the access history of a financial datum.
```

### 4.3 Technical annex — Idempotency resolution table

> **Note**: this annex is a **technical derivation** of CA04 + CA05 for whoever implements the charge service. It is not AC detail in the "Rules to be applied:" style — it is an exhaustive table. In a real project, this becomes a `pytest.mark.parametrize` test table.

```
Charge resolution by (idempotency key, previous state)

       • (new key, no charge)               → charges 1x, stores result      → 201
       • (repeated key, result=accepted)    → returns previous result        → 201 (identical)
       • (repeated key, result=refused)     → returns previous refusal       → 402 (identical)
       • (repeated key, in processing)      → waits/returns same result      → no 2nd charge
       • (new key, card blocked by AF)      → refused by anti-fraud          → 422
       • (new key, value > R$2,000, no 2FA) → requires 2nd factor            → 422
```

---

## 5. User Stories (with BDD)

### US 1 — Card secrets are never stored, number always masked

```
US Reject persistence of CVV/track/PIN, tokenize, and display the card masked

Description (BDD):
  GIVEN that a charge arrives with card data
  WHEN the system processes the card
  THEN the security code (CVV) is never stored anywhere
  AND the card number is replaced by a token before any persistence
  AND a scan of logs and database for the card number returns 0 occurrences
  AND in any display at most the last 4 digits appear

Related to: CA01, CA02, CA03, RNF-01, G-02
Story Points: 5
```

### US 2 — Idempotent charge

```
US Charge exactly once per attempt via an idempotency key

Description (BDD):
  Scenario 1: new key
  GIVEN that I send a charge with the key "k-123" for the first time
  WHEN I POST /api/v1/payments/charge with Idempotency-Key: k-123
  THEN the system returns HTTP 201
  AND the acquirer is charged exactly 1 time

  Scenario 2: re-send due to timeout (same key)
  GIVEN that the charge with the key "k-123" has already been processed
  WHEN I re-send the POST 50 times with Idempotency-Key: k-123
  THEN the system always returns the SAME result of the original charge
  AND the acquirer is NOT charged a second time

Related to: CA04, CA05, RNF-02
Story Points: 8
```

### US 3 — Charge is transactional

```
US Ensure the charge is atomic (rollback on failure)

Description (BDD):
  GIVEN that the charge makes two writes (movement + wallet balance)
  WHEN one of the writes fails (simulated via mock)
  THEN both operations are rolled back
  AND no partial movement is recorded
  AND the wallet balance stays consistent

Related to: CA06
Story Points: 3
```

### US 4 — Balance never negative, every movement traces to an order

```
US Refuse a debit that drops the balance below zero and link the movement to the order

Description (BDD):
  Scenario 1: balance never negative
  GIVEN that the wallet has a balance of R$ 30.00
  WHEN a debit of R$ 50.00 is attempted
  THEN the system refuses the debit
  AND the balance stays R$ 30.00
  AND no movement is created

  Scenario 2: traceability to the order
  GIVEN that an accepted charge generated a money movement
  WHEN I query that movement
  THEN it references exactly one source order
  AND from the order I can reconstruct all the movements it generated

Related to: CA07, CA08, G-01, G-03
Story Points: 5
```

### US 5 — Daily reconciliation

```
US Check the day's movements against the acquirer statement

Description (BDD):
  GIVEN that there were money movements during the day
  WHEN the reconciliation job runs
  THEN 100% of the movements match the acquirer statement
  AND any divergence raises an alert the same day

Related to: CA09, RNF-03
Story Points: 5
```

### US 6 — Anti-fraud limit and strong authentication

```
US Block the card after refusals and require a 2nd factor on a high value

Description (BDD):
  Scenario 1: anti-fraud block
  GIVEN that the same card had 5 refused charges within 10 minutes
  WHEN the 6th charge is attempted with that card
  THEN the system refuses by anti-fraud without calling the acquirer
  AND the card stays blocked for 30 minutes

  Scenario 2: second factor on a high value
  GIVEN that a charge is for R$ 2,500.00
  WHEN the payer does not satisfy the second factor
  THEN the charge is rejected
  AND no money moves

Related to: CA10, RNF-04, RNF-05
Story Points: 5
```

### US 7 — Immutable audit trail

```
US Record access to a financial datum immutably

Description (BDD):
  GIVEN that an operator reads a customer's tokenized card
  WHEN the access happens
  THEN an audit record is created with who, when, resource, and action
  AND an attempt to alter or erase that record fails

Related to: CA11, RNF-06, G-04
Story Points: 3
```

---

## 6. Applied validation (Sommerville 5 + Falbo 7)

Applying [06-validacao.md](../references/06-validacao.md):

| Check | Application |
|---|---|
| **Validity** (Sommerville) | Confirmed with the founder: "Yes — never bill twice, never store CVV, never go negative" |
| **Consistency** | CA04 (idempotency) and CA06 (transactional) are consistent — the result stored per key is that of the same atomic movement |
| **Completeness** | The initial set was missing CA07 (negative balance); discovered in review before coding, after a race-condition question |
| **Realism** | Implementable in Django 5 + DRF with a tokenization provider and the acquirer's idempotency support |
| **Verifiability** | Each AC has a corresponding pytest test in `tests/test_charge_idempotency.py` and `tests/test_card_protection.py` |
| **Complete (Falbo)** | ACs describe input (charge request + idempotency key), rule (resolution table), output (business result + balance state) |
| **Correct (Falbo)** | Validated with the founder and against the acquirer's *"PCI"* guidance |
| **Necessary (Falbo)** | Yes — two real incidents (double charge + CVV storage) motivated the change |
| **Prioritizable (Falbo)** | 🔴 Immediate for CA01/CA04 (legal + money risk); 🟠 High for reconciliation/audit |
| **Verifiable (Falbo)** | 17 specific tests passed (idempotency, masking, rollback, negative-balance, anti-fraud) |

---

## 7. Implemented traceability

Applying [07-mudanca-rastreabilidade.md](../references/07-mudanca-rastreabilidade.md):

```
Commit a7f31c0: feat(payments): idempotent charge on a tokenized card + audit trail
├─ apps/payments/models.py
│    ├─ CartaoTokenizado (stores token + last 4 digits; NEVER CVV/PAN)
│    ├─ Movimento (mandatory FK to Pedido — G-03/CA08)
│    └─ Carteira.debitar(valor) → refuses if balance - valor < 0 (G-01/CA07)
├─ apps/payments/services.py
│    ├─ cobrar(pedido, token, valor, idempotency_key) → ResultadoCobranca
│    │    ├─ resolves by idempotency_key (CA04/CA05 — table §4.3)
│    │    ├─ applies anti-fraud limit + 2nd factor (CA10/RNF-04/RNF-05)
│    │    └─ atomic transaction movement+balance (CA06)
│    └─ conciliar(dia) → DivergenciaConciliacao[] (CA09/RNF-03)
├─ apps/payments/tokenization.py
│    └─ tokenizar(cartao) → rejects storage of CVV/track/PIN (CA01/CA02/G-02)
├─ apps/payments/audit.py
│    └─ AuditLog append-only (UPDATE/DELETE blocked — CA11/RNF-06/G-04)
├─ apps/payments/serializers.py
│    └─ number always masked (last 4 digits — CA03/RNF-01)
├─ apps/payments/tests/test_charge_idempotency.py
│    ├─ test_chave_nova_cobra_uma_vez (CA04)
│    ├─ test_reenvio_mesma_chave_nao_cobra_de_novo (CA04/RNF-02)
│    ├─ test_tres_resultados_de_negocio (CA05 — 201/402/422)
│    └─ test_cobranca_rollback_em_falha (CA06)
├─ apps/payments/tests/test_card_protection.py
│    ├─ test_cvv_nunca_persistido (CA01/G-02)
│    ├─ test_numero_tokenizado_antes_de_persistir (CA02)
│    └─ test_numero_sempre_mascarado (CA03/RNF-01)
├─ apps/payments/tests/test_wallet.py
│    ├─ test_saldo_nunca_negativo (CA07/G-01)
│    └─ test_movimento_referencia_um_pedido (CA08/G-03)
└─ apps/payments/tests/test_fraud_audit.py
     ├─ test_bloqueio_apos_5_recusas (CA10/RNF-04)
     ├─ test_valor_alto_exige_segundo_fator (CA10/RNF-05)
     ├─ test_conciliacao_sinaliza_divergencia (CA09/RNF-03)
     └─ test_auditoria_append_only (CA11/RNF-06/G-04)
```

**Every AC and NFR has a traceable test**, every test describes a domain rule or invariant.

---

## 8. Ethical layer (*"SBC"* 002/2024)

Applying [09-etica-sbc.md](../references/09-etica-sbc.md):

| Principle | Application in the case |
|---|---|
| **§1.1 Well-being** | The customer is charged exactly once and keeps clear visibility of their balance and movements |
| **§1.2 Avoid harm** | A double charge and a card-data leak are concrete financial harms; idempotency + tokenization remove both |
| **§1.3 Honesty** | A "paid" status corresponds to real, reconciled money; the system does not overstate what was charged |
| **§1.4 Non-discrimination** | Anti-fraud limits apply by transaction behaviour, not by personal characteristics of the holder |
| **§2.5 Privacy** | Card secrets never persisted; PAN masked everywhere; access to financial data is audited (*"LGPD"*/*"PCI"* aligned) |
| **§2.9 Secure systems** | Defence in depth: tokenization (data) + idempotency (money) + atomic transaction + anti-fraud + immutable audit |
| **§3.6 Care when modifying** | Change preserved the happy path (single charge still works) and added the missing failure-path guarantees, all regression-tested |

**Ethical decision**: chose to **remove card secrets from the application database entirely** (tokenization provider) over **encrypting CVV in place**. Justification: storing CVV is forbidden by network rules regardless of encryption, and minimizing *"PCI"* scope is safer for customers than any in-house crypto. Trade-off (dependency on a tokenization provider) documented.

---

## 9. Lessons from the case (applicable to future *"PagLeve"* features)

1. **The happy-path spec hid two money-critical requirements** — "charge once per attempt" and "never store card secrets"; **making them explicit via ACs, NFRs and Goals** was the missing step
2. **Idempotency is a requirement, not an implementation detail** — it earns its own NFR (RNF-02), its own AC (CA04), and a resolution table; the original double-charge bug came from treating a re-try as "just retry"
3. **Goals (G) capture invariants** that no single AC owns — "balance never negative", "no card secret stored", "every charge traces to an order" — and every ≥2-write money operation inherits them
4. **NFRs must be quantitative** — "after 5 refusals in 10 minutes, block 30 minutes"; "value above R$ 2,000 requires 2nd factor" — a vague "be secure" is untestable
5. **Reconciliation is part of the requirement**, not an ops afterthought — if internal movements and the acquirer statement can diverge silently, "paid" means nothing
6. **Defence in depth** beats one barrier: tokenization + idempotency + atomic transaction + anti-fraud + immutable audit, each independent
7. **EARS phrasing on the riskiest NFRs** (RNF-02, RNF-05) removed ambiguity for the implementer without forcing the whole spec into EARS

---

## 10. Applying this template to next *"PagLeve"* features

For any new feature (e.g., "partial refund" or "withdrawal to a bank account"), reuse this structure:

1. **Stakeholders explicitly identified** — including the acquirer and the regulator/auditor
2. **AS-IS / TO-BE** documented with the **worst money/legal outcome** named (clear gap)
3. **Goals (G) as invariants** — what must never happen (no negative balance, no stored secret, no orphan movement)
4. **NFRs always quantitative** with a measurement method; EARS on the riskiest ones
5. **Declarative ACs with stable IDs** (`CA-ESTORNO-01`, ...), including a "behaviour-on-rejection" AC
6. **User Stories slicing ACs** into incremental slices with BDD in the description
7. **Validation against Falbo 7 + Sommerville 5** before coding
8. **Ethical layer**: concrete question — who can be financially harmed, and is any secret being stored?
9. **Defence in depth**: apply each money invariant in ≥2 independent layers (model + service + audit)
10. **Tests traceable to the ACs/NFRs/Goals** (not code-oriented tests); commit message reflects the requirement

In *"PagLeve"*-scale projects (small team handling real money), this level of RE ceremony **accelerates** delivery instead of slowing it down — because a silent double-charge or a stored CVV is far more expensive than the spec that prevents it.
