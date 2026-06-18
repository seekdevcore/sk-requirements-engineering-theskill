# Feature step-definition variants — one Gherkin, ten stacks

> **Write the `.feature` once, bind it anywhere.** The canonical
> [`../template-user-story.feature`](../template-user-story.feature) is a **pt-BR Gherkin** spec (`# language: pt`,
> `Funcionalidade/Cenário/Dado/Quando/Então`). Gherkin is the *contract* between the stakeholder who reads it and
> the test runner that executes it — and **every major BDD runner parses the same file natively**. These files
> are ready-to-copy **step-definition skeletons** that bind that one feature in ten ecosystems, so the choice of
> test stack never forces you to rewrite the requirement.

This composes with [`../../references/04-bdd-criterios-aceitacao.md`](../../references/04-bdd-criterios-aceitacao.md)
(BDD + AC) and the `e2e-testing-patterns` discipline. The Gherkin stays the source of truth; the step file is the
*glue* to the system under test — keep steps **UI-independent and deterministic** (Liz Keogh rules, see the
`.feature` header).

## The ten bindings

| Stack | Language | Binds via | Install | Run |
|---|---|---|---|---|
| [`pytest_bdd_steps.py`](pytest_bdd_steps.py) | Python | `@given/@when/@then` + `scenarios()` | `uv add --dev pytest-bdd` | `uv run pytest` |
| [`behave_steps.py`](behave_steps.py) | Python | `@given/@when/@then` + `environment.py` | `uv add --dev behave` | `uv run behave` |
| [`cucumber_js.steps.js`](cucumber_js.steps.js) | JS (API/unit) | `@cucumber/cucumber` World | `npm i -D @cucumber/cucumber` | `npx cucumber-js` |
| [`cucumber_playwright.steps.ts`](cucumber_playwright.steps.ts) | TS (browser E2E) | `@cucumber/cucumber` + `@playwright/test` | `npm i -D @cucumber/cucumber @playwright/test` | `npx cucumber-js` |
| [`specflow_Steps.cs`](specflow_Steps.cs) | C# / .NET | `[Binding]` + `[Given]/[When]/[Then]` | `dotnet add package Reqnroll.xUnit` | `dotnet test` |
| [`behat_FeatureContext.php`](behat_FeatureContext.php) | PHP | `FeatureContext` + `@Given/@When/@Then` | `composer require --dev behat/behat` | `vendor/bin/behat` |
| [`cucumber_jvm_Steps.java`](cucumber_jvm_Steps.java) | Java / JVM | `@Dado/@Quando/@Então` + JUnit `@Suite` | `io.cucumber:cucumber-java` (Maven/Gradle) | `mvn test` |
| [`godog_steps.go`](godog_steps.go) | Go | `ctx.Step(regexp, fn)` + `Before` hook | `go get github.com/cucumber/godog/cmd/godog` | `go test ./...` |
| [`cucumber_cpp.steps.cpp`](cucumber_cpp.steps.cpp) | C++ | `GIVEN/WHEN/THEN` macros + `ScenarioScope` | `cucumber-cpp` + GTest (CMake) | `cucumber` |
| [`cucumber_wire_steps.c`](cucumber_wire_steps.c) | **C (pure)** | Cucumber **wire protocol** (TCP step server) | a `.wire` config + tiny TCP loop | `./stepserver & cucumber` |

> **pt-BR Gherkin works out of the box** in nine of the ten — Cucumber/Behave/SpecFlow-Reqnroll/Behat/Cucumber-JVM/godog/cucumber-cpp
> read the `# language: pt` header and match `Dado/Quando/Então` to your steps. You do **not** translate the
> feature to bind it; you translate nothing. (pytest-bdd also honours the header.) The pure-C wire server is the
> one special case — see the note below.

> **C++ and pure C — the honest caveat.** **C++** has a first-class, maintained backend (**cucumber-cpp**), so
> its skeleton looks like the others. **Pure C has no native Gherkin runner**: the portable route is the Cucumber
> **wire protocol** — a TCP step server (written in C) that the `cucumber` runner connects to and asks to
> match/invoke steps. The `.c` skeleton is that server's step table + handlers; the thin TCP+JSON loop
> (`wire_server.*`) is the only stack-specific glue. If your project already builds with C++, the simpler path is
> to drive the C system-under-test from the `cucumber-cpp` harness via `extern "C"` — both options are noted in
> the file header.

> **SpecFlow → Reqnroll.** SpecFlow was discontinued in 2024; **[Reqnroll](https://reqnroll.net)** is its
> drop-in open-source successor (same `[Binding]`/`[Given]` API, same Gherkin). The `.cs` skeleton uses Reqnroll
> namespaces; for a legacy SpecFlow project, swap `using Reqnroll;` → `using TechTalk.SpecFlow;` — nothing else
> changes.

## Where the step files live in a real project (they do NOT stay here)

`examples/` is a *reference*; in the host project the glue lives next to the suite:

```
# Python (pytest-bdd / behave)
features/US30-1-busca-editorial.feature
features/steps/test_busca.py          # pytest-bdd
features/steps/busca_steps.py         # behave  (+ features/environment.py for hooks)

# JS/TS (cucumber-js / cucumber-playwright)
e2e/features/US30-1-busca-editorial.feature
e2e/features/step_definitions/busca.steps.ts
e2e/support/world.ts                  # custom World (holds the Playwright page)

# .NET (Reqnroll)            # PHP (Behat)
Features/BuscaEditorial.feature        features/US30-1-busca-editorial.feature
StepDefinitions/BuscaSteps.cs          features/bootstrap/FeatureContext.php

# Java (Cucumber-JVM)        # Go (godog)
src/test/resources/features/US30-1-busca-editorial.feature   features/US30-1-busca-editorial.feature
src/test/java/com/interpop/specs/BuscaEditorialSteps.java    features/busca_test.go   # InitializeScenario

# C++ (cucumber-cpp)         # C (wire protocol)
features/US30-1-busca-editorial.feature        features/US30-1-busca-editorial.feature
features/step_definitions/BuscaSteps.cpp       features/step_definitions/interpop.wire  # host/port → C stepserver
```

## Traceability stays intact

Every skeleton repeats the feature's traceability header (`@US`, `@F`, `@EP`, `@CAs`, `@Doc-Req`) as a comment,
so a reviewer reading the step file can still walk back to the `RF` in the requirements document
([`../../references/07-mudanca-rastreabilidade.md`](../../references/07-mudanca-rastreabilidade.md)). Binding a
feature in a new stack never severs the `RF ↔ CA ↔ Cenário ↔ test` chain.
