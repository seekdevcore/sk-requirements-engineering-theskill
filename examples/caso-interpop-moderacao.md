# Worked Example — Ban Hierarchy in the *"Interpop"* Project

> Real case from the *"Interpop"* project (Brazilian editorial of *"Soft Power"*; Django 5 + DRF + React 19). Shows how an **already implemented** feature maps to the skill's RE framework — useful for auditing pre-existing specifications or as a template for new features in the same project. Reference commit: `1e0241e` — its pt-BR subject `feat(moderation): dev é superadmin — único que bane/desbane admins` translates as "dev is superadmin — the only one who bans/unbans admins" (the subject is kept verbatim as it is the real identifier in git history).
>
> **Note on language preservation**: the Feature, User Story, AC, FR, NFR, and business-rule titles, as well as the BDD content, were authored in pt-BR in the *"Interpop"* repository, commits, OpenProject cards, and `CLAUDE.md` instructions. This en-CA edition translates the artifact content for an English-reading audience; the original commit hash and any pt-BR identifier load-bearing for traceability are glossed in place. **Explanations, tables, analysis, and artifact content are all in en-CA.**

---

## 1. Context and problem

**Editorial-political problem**: *"Interpop"* has the editorial hierarchy `dev > admin > editor > user`. The initial moderation version let any admin ban another admin. This created real risk: in an editorial team with ≥2 admins, an abusive admin could administratively "decapitate" another admin before being confronted. Or worse: an admin under external coercion banning the dev.

**Diagnosis**: the power relation for banning did NOT mirror the declared editorial hierarchy. **It was an implicit, undocumented requirement** — the kind ethnography reveals (see [02-elicitacao.md §7](../references/02-elicitacao.md)). Once the case was discussed, it became explicit.

---

## 2. Stakeholders

Applying Wiegers 2003 (see [01-fundamentos.md §5](../references/01-fundamentos.md)):

| Stakeholder | Interest |
|---|---|
| **Dev (project owner/creator)** | Ensure no admin can decapitate the hierarchy |
| **Editorial admin** | Be able to ban editors/users who abuse, while protected from banning by another admin |
| **Editor** | Be able to request bans via BanRequest, without the ability to execute directly |
| **User (reader)** | Not be unjustly banned; have a review channel |
| **Banned** | Have clarity on what happened; potential contestation channel |
| **External auditor** (hypothetical) | Complete logs of who banned whom, when, and why |

---

## 3. AS-IS → TO-BE analysis

Applying the analysis from [08-analista-negocios.md §3](../references/08-analista-negocios.md):

### AS-IS (before commit 1e0241e)

```
Admin1 → POST /moderation/bans/ { user: Admin2, reason: "..." }
  → System accepts
  → Admin2 banned (loses access, loses power)
  → Dev finds out later (via monitoring or complaint)
```

**Pains**:

- Declared editorial hierarchy did not match the technical hierarchy
- Admin under external pressure could ban other admins / the dev
- No formal process for "how an admin is banned"

### TO-BE

```
Admin1 → POST /moderation/bans/ { user: Admin2 }
  → System REJECTS (400)
  → Hierarchy: only dev bans admin

Admin1 → POST /moderation/bans/ { user: Editor1 }
  → System accepts
  → Editor1 banned
```

### GAP analysis

| Gap | Solution |
|---|---|
| `is_banned` lives in one place; `Ban` in another; they could diverge | NFR: atomic transaction in `ban_user` (ADR-012) |
| Idempotency: re-banning after unban broke the UNIQUE constraint | FR: `update_or_create` reactivates the existing Ban |
| Hierarchy is not expressed in code | FR: relational method `can_be_banned_by(actor)` on the User model |
| No regression test | NFR: ≥90% coverage in `apps.moderation` |

---

## 4. Feature: Ban Hierarchy

**Feature description (client-deliverable):**

Defines who can ban and unban whom within the *"Interpop"* editorial team. Implements the `dev > admin > editor > user` hierarchy as a permission matrix applied consistently across all ban and unban operations — whether they are carried out through the public interface (direct moderation), through the approval of a ban request opened by an editor, or through the equivalent actions in the administrative interface. The client deliverable (*"Gabriel"*, dev/owner of the project) is the guarantee that no administrator can "decapitate" another administrator or the dev themselves — even under external coercion or in the event of compromised credentials. The rule holds symmetrically for banning and unbanning, with idempotency preserved when a user is re-banned after being unbanned (it reactivates the existing record instead of creating a duplicate).

> This description is what goes on the OpenProject Feature card (or equivalent). It is **written in business language**, readable by any stakeholder. The ACs below formalize the testable rules; BDD appears only in the User Stories (§5).

### 4.1 Acceptance Criteria (declarative style)

9 ACs, **grouped by theme** (Rule 7 of [05-convencoes-interpop.md](../references/05-convencoes-interpop.md)). ACs with **`[...]`** at the end of the title must be read together with the detail in §4.2.

#### 📋 CA - Ban hierarchy

| ID | Description | Detail? |
|---|---|---|
| `CA01` | Dev is immune to banning by any other user, including another dev. | — |
| `CA02` | An administrator can only be banned by a dev **[...]** | ✅ |
| `CA03` | Editor and regular user can be banned by an administrator or by a dev **[...]** | ✅ |
| `CA04` | No user can ban themselves, in any role. | — |

#### 📋 CA - Behaviour of the ban operation

| ID | Description | Detail? |
|---|---|---|
| `CA05` | The ban-hierarchy rule also applies to unbanning **[...]** | ✅ |
| `CA06` | On receiving the ban operation, the system responds with one of three business results **[...]** | ✅ |
| `CA07` | Banning is idempotent with respect to the user's history **[...]** | ✅ |
| `CA08` | Banning is transactional. If a failure occurs between recording the ban and updating the "banned" flag on the user's profile, both operations must be rolled back — the user cannot end up in an inconsistent state. | — |

#### 📋 CA - Approval flow via request (BanRequest)

| ID | Description | Detail? |
|---|---|---|
| `CA09` | The ban-request flow (BanRequest) remains intact: editors can open requests that an admin/dev approves or rejects, with idempotency preserved **[...]** | ✅ |

### 4.2 Detail of ACs with `[...]`

Each block below is what appears in the **item body** in OpenProject (AC Description field), following the `Rules to be applied:` + bullets convention.

#### CA02 — Detail

```
Rules to be applied:
- Another administrator cannot ban an administrator (same role; the horizontal hierarchy does not allow it).
- An administrator cannot ban themselves (general rule CA04 prevails).
- An editor does not have permission to moderate administrators; the attempt is rejected.
- Only a dev (highest role in the hierarchy) may apply a ban to an administrator.
```

#### CA03 — Detail

```
Rules to be applied:
- An editor can be banned by an administrator or by a dev.
- A regular user can be banned by an administrator or by a dev.
- An editor does NOT ban another editor (the horizontal hierarchy does not allow it).
- A regular user does NOT ban anyone (lowest role in the hierarchy).
```

#### CA05 — Detail

```
Rules to be applied:
- The who-can-ban-whom rule (CA01..CA04) applies equally to unbanning.
- If a dev applied a ban to an administrator, only another dev (or the same one) may unban.
- A regular administrator CANNOT undo a ban that was applied by a dev to another administrator.
- The policy exists to prevent a subordinate from reversing the superior's decision.
```

#### CA06 — Detail

```
Rules to be applied:
- When the user has permission and the hierarchy is respected, the system confirms the ban (operation accepted).
- When the hierarchy is violated (for example, an administrator trying to ban another administrator), the system rejects it with the message "Operation not permitted by the editorial hierarchy".
- When the user does not have moderation permission (is neither administrator nor dev), the system rejects it with the message "You do not have permission to moderate".
- In all rejection cases, no ban record is created and no user profile is changed.
```

> **Technical note (does not go on the CA06 card)**: the 3 business results above are implemented respectively as HTTP 201, 400, and 403 on the `POST /api/v1/moderation/bans/` endpoint. This technical mapping is the responsibility of the Tasks (see §7 Traceability), not the AC.

#### CA07 — Detail

```
Rules to be applied:
- Re-banning a user who was previously banned and then unbanned does NOT create a duplicate ban: the existing record is reactivated.
- On reactivation, the record inherits the new reason given and the new administrator who applied it.
- The user's history stays consistent: 1 ban record per user↔administrator relation, with an active/inactive sequence over time.
```

#### CA09 — Detail

```
Rules to be applied:
- An editor can open a ban request (the BanRequest stays in a pending state).
- An administrator or dev can APPROVE the request. Approval creates the real ban following the same hierarchy (CA01..CA04). If the hierarchy is violated at approval, the approval fails.
- An administrator or dev can REJECT the request. In that case, the request is marked as rejected and no ban is created.
- Approving a request that was already approved previously returns the existing ban, without creating a duplicate (idempotency).
```

### 4.3 Technical annex — Exhaustive matrix of the `can_be_banned_by` method

> **Note**: this annex is a **technical derivation** of CA02 + CA04 for whoever implements the `User.can_be_banned_by(actor)` method. It is not AC detail in the "Rules to be applied:" style — it is an exhaustive truth table. In a real project, this becomes a comment in the code or a test table (`pytest.mark.parametrize`).

```
Exhaustive matrix can_be_banned_by(actor) → bool

       • dev_user.can_be_banned_by(admin_user)   → False
       • dev_user.can_be_banned_by(dev2)         → False  (dev immune even to another dev)
       • dev_user.can_be_banned_by(dev_user)     → False  (no one bans themselves)
       • admin_user.can_be_banned_by(dev_user)   → True
       • admin_user.can_be_banned_by(admin2)     → False
       • admin_user.can_be_banned_by(admin_user) → False
       • admin_user.can_be_banned_by(editor)     → False
       • editor.can_be_banned_by(admin_user)     → True
       • editor.can_be_banned_by(dev_user)       → True
       • editor.can_be_banned_by(other_editor)   → False
       • editor.can_be_banned_by(None)           → False
```

---

## 5. User Stories (with BDD)

### US 1 — Apply the hierarchy in the model

```
US Implement can_be_banned_by on User as the single authority for hierarchy

Description (BDD):
  Given the system has users with different roles
  When the method user.can_be_banned_by(actor) is called
  Then the result follows the hierarchy matrix (CA01..CA04)

Related to: CA01, CA02, CA03, CA04
Story Points: 3
```

### US 2 — Apply the hierarchy in the endpoint

```
US Endpoint POST /bans/ validates hierarchy before creating Ban

Description (BDD):
  Given the authenticated user is admin
  And the target user is also admin
  When I POST /api/v1/moderation/bans/ with {user_id: target, reason: "x"}
  Then the system returns HTTP 400
  And no Ban is created
  And target.is_banned remains False

  Scenario 2: Dev banning admin
  Given the authenticated user is dev
  And the target user is admin
  When I POST /api/v1/moderation/bans/ with {user_id: target}
  Then the system returns HTTP 201
  And target.is_banned becomes True

  Scenario 3: Admin banning editor (regression — old behaviour preserved)
  Given the authenticated user is admin
  And the target user is editor
  When I POST /api/v1/moderation/bans/ with {user_id: target}
  Then the system returns HTTP 201
  And target.is_banned becomes True

Related to: CA02, CA03, CA06
Story Points: 5
```

### US 3 — Ensure transactional atomicity

```
US Ensure ban_user is atomic (rollback on failure)

Description (BDD):
  Given ban_user makes two writes (Ban + User.is_banned)
  When one of the writes fails (simulated via mock)
  Then both operations are rolled back
  And the user does NOT end up in an inconsistent state

Related to: CA08
Story Points: 2
```

### US 4 — Idempotency (re-ban after unban)

```
US ban_user reactivates existing Ban instead of creating a duplicate

Description (BDD):
  Given a user was banned (Ban record X)
  And was unbanned (X.is_active = False)
  When the user is banned again
  Then the same Ban X is reactivated (no new one created)
  And X.reason is updated to the new reason
  And X.banned_by is updated to the new admin
  And X.unbanned_by is cleared
  And the UNIQUE constraint is not violated

Related to: CA07
Story Points: 3
```

### US 5 — Unban follows the same hierarchy

```
US Apply relational can_be_unbanned_by

Description (BDD):
  Given a dev banned an admin (Ban Y)
  When a regular admin tries DELETE /bans/Y/
  Then the system returns HTTP 403
  And the admin remains banned

  Given a dev banned an admin (Ban Y)
  When the same dev (or another dev) does DELETE /bans/Y/
  Then the system returns HTTP 200 or 204
  And the admin is unbanned

Related to: CA05
Story Points: 3
```

---

## 6. Applied validation (Sommerville 5 + Falbo 7)

Applying [06-validacao.md](../references/06-validacao.md):

| Check | Application |
|---|---|
| **Validity** (Sommerville) | Confirmed in discussion with the dev: "Yes, we want exactly that an admin does not ban an admin" |
| **Consistency** | CA02 and CA09 are consistent — approve_ban_request reuses ban_user |
| **Completeness** | The initial set was missing CA04 (self-ban); discovered in review before coding |
| **Realism** | Implementable in Django 5 + DRF without external dependency |
| **Verifiability** | Each AC has a corresponding pytest test in `tests/test_ban_hierarchy.py` |
| **Complete (Falbo)** | ACs describe input (HTTP request), rule (matrix), output (HTTP status + User state) |
| **Correct (Falbo)** | Validated in conversation with the dev (sole stakeholder of the project) |
| **Necessary (Falbo)** | Yes — real risk of internal abuse |
| **Prioritizable (Falbo)** | High priority (commit was made immediately after the decision) |
| **Verifiable (Falbo)** | 13 specific tests passed (`test_ban_hierarchy.py`) |

---

## 7. Implemented traceability

Applying [07-mudanca-rastreabilidade.md](../references/07-mudanca-rastreabilidade.md):

```
Commit 1e0241e: feat(moderation): dev é superadmin — único que bane/desbane admins
                 ("dev is superadmin — the only one who bans/unbans admins")
├─ apps/users/models.py
│    ├─ can_be_banned_by(actor: User|None) → bool
│    └─ can_be_unbanned_by(actor: User|None) → bool
├─ apps/moderation/services.py
│    ├─ ban_user(target, admin, reason, trigger_message) → Ban
│    │    └─ raise PermissionDenied if not target.can_be_banned_by(admin)
│    ├─ unban_user(ban, admin) → Ban
│    │    └─ raise PermissionDenied if not ban.user.can_be_unbanned_by(admin)
│    └─ approve_ban_request(request_obj, admin, decision_note) → Ban
│         └─ calls ban_user (inherits hierarchy)
├─ apps/users/admin.py
│    └─ is_banned readonly (do not bypass the hierarchy via Django Admin)
├─ apps/moderation/tests/test_ban_hierarchy.py
│    ├─ test_can_be_banned_by_matrix (exhaustive model matrix)
│    ├─ test_dev_can_ban_admin (endpoint)
│    ├─ test_admin_cannot_ban_another_admin
│    ├─ test_admin_cannot_ban_dev
│    ├─ test_dev_cannot_ban_another_dev
│    ├─ test_admin_can_still_ban_editor (regression)
│    ├─ test_editor_cannot_reach_ban_endpoint (403)
│    ├─ test_admin_cannot_unban_dev_placed_ban_on_admin
│    ├─ test_dev_can_unban_admin
│    └─ test_admin_can_unban_editor
└─ apps/moderation/tests/test_services.py
     ├─ test_ban_user_creates_ban_and_flags_user
     ├─ test_ban_user_idempotent_reactivates_existing (CA07)
     └─ test_ban_user_rollback_on_failure (CA08)
```

**Every AC has a traceable test**, every test describes a domain rule.

---

## 8. Ethical layer (*"SBC"* 002/2024)

Applying [09-etica-sbc.md](../references/09-etica-sbc.md):

| Principle | Application in the case |
|---|---|
| **§1.1 Well-being** | The hierarchy protects the editorial team from internal abuse; protects readers from receiving inconsistent moderation |
| **§1.2 Avoid harm** | Unjust banning is grave reputational harm; strict hierarchy reduces the risk |
| **§1.3 Honesty** | The declared hierarchy (`dev > admin > editor > user`) now matches the implementation |
| **§1.4 Non-discrimination** | The hierarchy does not privilege anyone by personal characteristics; only by role |
| **§2.9 Secure systems** | Defence in depth: model (matrix) + endpoint (permission classes) + service (atomic transaction + hierarchy repeated as a last barrier) |
| **§3.6 Care when modifying** | Change preserved old behaviour: admin still bans editor/user (regression tested) |

**Ethical decision**: chose **rigid** hierarchy (admin never bans admin) over **flexible** hierarchy (admin quorum). Justification: small team (1 dev + 2 admins), quorum is not viable. Trade-off documented.

---

## 9. Lessons from the case (applicable to future *"Interpop"* features)

1. **Editorial hierarchy declared in CLAUDE.md** had become an implicit requirement; **making it explicit via ACs** was the missing step
2. **Defence in depth** beats isolated pre-conditions: model + endpoint + service, all validate
3. **A BDD-style rule in the commit message** helps future review ("Rule: dev is immune; admin only by dev")
4. **Regression testing is part of the requirement** — the AC "admin still bans editor" must be explicit; otherwise a refactor may break it
5. **ADR-012 (atomic transaction)** became a cross-cutting architectural standard — every ≥2-write operation inherits from it
6. **Idempotency** came from a requirement (CA07) discovered in production (the original bug); recovering via rewriting ban_user was cheaper than handling the UNIQUE constraint at the caller

---

## 10. Applying this template to next *"Interpop"* features

For any new feature (e.g., "community-moderated comments"), reuse this structure:

1. **Stakeholders explicitly identified** (list of who is affected)
2. **AS-IS / TO-BE** documented (clear gap)
3. **Declarative ACs with stable IDs** (`CA-COMMENT-01`, `CA-COMMENT-02`, ...)
4. **User Stories slicing ACs into incremental slices** with BDD in the description
5. **Story Points via Planning Poker** (even solo, comparing with previous features)
6. **Validation against Falbo 7 + Sommerville 5** before coding
7. **Ethical layer**: concrete question — who can be harmed by this feature?
8. **Defence in depth**: apply invariant in ≥2 independent layers
9. **Tests traceable to the ACs** (not code-oriented tests)
10. **Commit message reflects the requirement**, not only the technical change

In *"Interpop"*-scale projects (solo + part-time + AI contribution), this level of RE ceremony **accelerates** delivery instead of slowing it down — because it eliminates silent rework at review.
