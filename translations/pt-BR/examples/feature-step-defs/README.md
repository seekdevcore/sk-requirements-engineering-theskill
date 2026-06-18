# Variantes de step-definition de feature — um Gherkin, dez stacks

> **Escreva o `.feature` uma vez, ligue-o a qualquer stack.** O feature canônico
> [`../template-user-story.feature`](../template-user-story.feature) é uma spec **Gherkin pt-BR** (`# language: pt`,
> `Funcionalidade/Cenário/Dado/Quando/Então`). O Gherkin é o *contrato* entre o stakeholder que o lê e o runner
> de teste que o executa — e **todo runner BDD relevante parseia o mesmo arquivo nativamente**. Os esqueletos de
> step-definition prontos para 10 ecossistemas ligam esse único feature, de modo que a escolha da stack de teste
> nunca obriga a reescrever o requisito.

> 🟡 **O código dos step-defs é neutro de idioma e não se traduz** — ele liga os passos do Gherkin pt-BR
> independentemente do idioma da documentação. Por isso os arquivos `.py/.js/.ts/.cs/.php/.java/.go/.cpp/.c` vivem **uma única vez**
> na raiz autoritativa em [`../../../examples/feature-step-defs/`](../../../examples/feature-step-defs/); este
> README é a tradução pt-BR do guia. Compõe com
> [`../../references/04-bdd-criterios-aceitacao.md`](../../references/04-bdd-criterios-aceitacao.md) (BDD + CA) e a
> disciplina `e2e-testing-patterns`.

## As dez ligações

| Stack | Linguagem | Liga via | Instalar | Rodar |
|---|---|---|---|---|
| [`pytest_bdd_steps.py`](../../../examples/feature-step-defs/pytest_bdd_steps.py) | Python | `@given/@when/@then` + `scenarios()` | `uv add --dev pytest-bdd` | `uv run pytest` |
| [`behave_steps.py`](../../../examples/feature-step-defs/behave_steps.py) | Python | `@given/@when/@then` + `environment.py` | `uv add --dev behave` | `uv run behave` |
| [`cucumber_js.steps.js`](../../../examples/feature-step-defs/cucumber_js.steps.js) | JS (API/unit) | World do `@cucumber/cucumber` | `npm i -D @cucumber/cucumber` | `npx cucumber-js` |
| [`cucumber_playwright.steps.ts`](../../../examples/feature-step-defs/cucumber_playwright.steps.ts) | TS (E2E browser) | `@cucumber/cucumber` + `@playwright/test` | `npm i -D @cucumber/cucumber @playwright/test` | `npx cucumber-js` |
| [`specflow_Steps.cs`](../../../examples/feature-step-defs/specflow_Steps.cs) | C# / .NET | `[Binding]` + `[Given]/[When]/[Then]` | `dotnet add package Reqnroll.xUnit` | `dotnet test` |
| [`behat_FeatureContext.php`](../../../examples/feature-step-defs/behat_FeatureContext.php) | PHP | `FeatureContext` + `@Given/@When/@Then` | `composer require --dev behat/behat` | `vendor/bin/behat` |
| [`cucumber_jvm_Steps.java`](../../../examples/feature-step-defs/cucumber_jvm_Steps.java) | Java / JVM | `@Dado/@Quando/@Então` + JUnit `@Suite` | `io.cucumber:cucumber-java` (Maven/Gradle) | `mvn test` |
| [`godog_steps.go`](../../../examples/feature-step-defs/godog_steps.go) | Go | `ctx.Step(regexp, fn)` + hook `Before` | `go get github.com/cucumber/godog/cmd/godog` | `go test ./...` |
| [`cucumber_cpp.steps.cpp`](../../../examples/feature-step-defs/cucumber_cpp.steps.cpp) | C++ | macros `GIVEN/WHEN/THEN` + `ScenarioScope` | `cucumber-cpp` + GTest (CMake) | `cucumber` |
| [`cucumber_wire_steps.c`](../../../examples/feature-step-defs/cucumber_wire_steps.c) | **C (puro)** | **protocolo wire** do Cucumber (servidor TCP) | um `.wire` + um loop TCP enxuto | `./stepserver & cucumber` |

> **Gherkin pt-BR funciona de imediato** em nove das dez — Cucumber/Behave/SpecFlow-Reqnroll/Behat/Cucumber-JVM/godog/cucumber-cpp
> leem o cabeçalho `# language: pt` e casam `Dado/Quando/Então` com seus passos. Você **não** traduz o feature
> para ligá-lo; não traduz nada. (O pytest-bdd também honra o cabeçalho.) O servidor wire em C puro é o único caso
> especial — veja a nota abaixo.

> **C++ e C puro — a ressalva honesta.** **C++** tem um backend de primeira classe e mantido (**cucumber-cpp**),
> então seu esqueleto se parece com os demais. **C puro não tem runner Gherkin nativo**: a rota portável é o
> **protocolo wire** do Cucumber — um servidor de steps por TCP (escrito em C) ao qual o runner `cucumber` se
> conecta para casar/invocar passos. O esqueleto `.c` é a tabela de steps + handlers desse servidor; o loop
> TCP+JSON enxuto (`wire_server.*`) é a única cola específica da stack. Se o projeto já compila com C++, o caminho
> mais simples é dirigir o sistema-sob-teste em C a partir do harness `cucumber-cpp` via `extern "C"` — ambas as
> opções estão no cabeçalho do arquivo.

> **SpecFlow → Reqnroll.** O SpecFlow foi descontinuado em 2024; **[Reqnroll](https://reqnroll.net)** é o sucessor
> open-source drop-in (mesma API `[Binding]`/`[Given]`, mesmo Gherkin). O esqueleto `.cs` usa namespaces do
> Reqnroll; num projeto SpecFlow legado, troque `using Reqnroll;` → `using TechTalk.SpecFlow;` — nada mais muda.

## Onde os arquivos de step ficam num projeto real (eles NÃO ficam aqui)

`examples/` é uma *referência*; no projeto hospedeiro a cola vive ao lado da suíte:

```
# Python (pytest-bdd / behave)
features/US30-1-busca-editorial.feature
features/steps/test_busca.py          # pytest-bdd
features/steps/busca_steps.py         # behave  (+ features/environment.py para hooks)

# JS/TS (cucumber-js / cucumber-playwright)
e2e/features/US30-1-busca-editorial.feature
e2e/features/step_definitions/busca.steps.ts
e2e/support/world.ts                  # World customizado (guarda a page do Playwright)

# .NET (Reqnroll)            # PHP (Behat)
Features/BuscaEditorial.feature        features/US30-1-busca-editorial.feature
StepDefinitions/BuscaSteps.cs          features/bootstrap/FeatureContext.php

# Java (Cucumber-JVM)        # Go (godog)
src/test/resources/features/US30-1-busca-editorial.feature   features/US30-1-busca-editorial.feature
src/test/java/com/interpop/specs/BuscaEditorialSteps.java    features/busca_test.go   # InitializeScenario

# C++ (cucumber-cpp)         # C (protocolo wire)
features/US30-1-busca-editorial.feature        features/US30-1-busca-editorial.feature
features/step_definitions/BuscaSteps.cpp       features/step_definitions/interpop.wire  # host/port → stepserver C
```

## A rastreabilidade permanece intacta

Cada esqueleto repete o cabeçalho de rastreabilidade do feature (`@US`, `@F`, `@EP`, `@CAs`, `@Doc-Req`) como
comentário, de modo que um revisor lendo o arquivo de step ainda consegue voltar até o `RF` no documento de
requisitos ([`../../references/07-mudanca-rastreabilidade.md`](../../references/07-mudanca-rastreabilidade.md)).
Ligar um feature a uma nova stack nunca rompe a cadeia `RF ↔ CA ↔ Cenário ↔ teste`.
