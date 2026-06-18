// Step definitions — Cucumber-JVM (Java)
// Binds: ../template-user-story.feature  (pt-BR Gherkin, `# language: pt`)
//
// @US: US30.1 · @F: F-30 · @EP: EP-10 · @CAs: CA01..CA11 · @Doc-Req: docs/specs/busca-editorial/REQUISITOS.md
//
// Setup (Maven):  io.cucumber:cucumber-java + io.cucumber:cucumber-junit-platform-engine   Run:  mvn test
// A @Suite runner with @SelectClasspathResource("features") + @ConfigurationParameter(GLUE) discovers the .feature.
// Cucumber-JVM reads `# language: pt`: the pt-BR annotations @Dado/@Quando/@Então (io.cucumber.java.pt) match
// Dado/Quando/Então natively — no need to translate the feature. {int}/{string} are built-in parameter types.

package com.interpop.specs;

import io.cucumber.java.pt.Dado;
import io.cucumber.java.pt.Quando;
import io.cucumber.java.pt.Então;
import static org.junit.jupiter.api.Assertions.*;

public class BuscaEditorialSteps {

    private final ApiClient api = new ApiClient();   // or inject a test double via PicoContainer
    private SearchResponse response;
    private double elapsedMs;

    // --- DADO -------------------------------------------------------------------
    @Dado("que o sistema Interpop está acessível ao público")
    public void sistemaAcessivel() {
        assertNotNull(api);
    }

    @Dado("existem {int} artigos publicados que contêm a palavra {string}")
    public void semearArtigos(int n, String termo) {
        api.seedArticles(n, "Sobre " + termo, "publicado");
    }

    // --- QUANDO -----------------------------------------------------------------
    @Quando("o leitor busca por {string}")   // Scenario Outline binding
    public void leitorBusca(String termo) {
        long start = System.nanoTime();
        response = api.get("/api/v1/search/articles?q=" + termo);
        elapsedMs = (System.nanoTime() - start) / 1_000_000.0;
    }

    // --- ENTÃO ------------------------------------------------------------------
    @Então("o sistema apresenta uma lista de cards de artigos")
    public void listaPresente() {
        assertEquals(200, response.status());
        assertFalse(response.results().isEmpty());
    }

    @Então("o resultado deve conter o artigo {string}")   // Scenario Outline
    public void resultadoContem(String titulo) {
        assertTrue(response.results().stream().anyMatch(a -> a.title().equals(titulo)));
    }

    @Então("a primeira tela completa carrega em menos de 800ms")
    public void dentroDoOrcamento() {
        assertTrue(elapsedMs < 800, () -> "orçamento de 800ms estourado: " + elapsedMs + "ms");
    }
}
