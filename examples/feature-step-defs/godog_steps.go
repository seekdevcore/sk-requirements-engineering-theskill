// Step definitions — godog (Go; the official Cucumber for Go)
// Binds: ../template-user-story.feature  (pt-BR Gherkin, `# language: pt`)
//
// @US: US30.1 · @F: F-30 · @EP: EP-10 · @CAs: CA01..CA11 · @Doc-Req: docs/specs/busca-editorial/REQUISITOS.md
//
// Setup:  go get github.com/cucumber/godog/cmd/godog@latest    Run:  go test ./...   (or: godog run)
// godog reads `# language: pt`; steps bind by regexp against Dado/Quando/Então. Per-scenario state lives on a
// struct re-created in a Before hook (no shared globals → deterministic & non-coupling, per the Liz Keogh rules).

package specs

import (
	"context"
	"fmt"
	"time"

	"github.com/cucumber/godog"
)

type buscaWorld struct {
	api       *APIClient // system under test
	response  *SearchResponse
	elapsedMs float64
}

// --- DADO ----------------------------------------------------------------------
func (w *buscaWorld) sistemaAcessivel() error {
	if w.api == nil {
		return fmt.Errorf("api client não inicializado")
	}
	return nil
}

func (w *buscaWorld) semearArtigos(n int, termo string) error {
	return w.api.SeedArticles(n, "Sobre "+termo, "publicado")
}

// --- QUANDO --------------------------------------------------------------------
func (w *buscaWorld) leitorBusca(termo string) error { // Scenario Outline binding
	start := time.Now()
	resp, err := w.api.Get("/api/v1/search/articles?q=" + termo)
	w.response, w.elapsedMs = resp, float64(time.Since(start).Microseconds())/1000.0
	return err
}

// --- ENTÃO ---------------------------------------------------------------------
func (w *buscaWorld) listaPresente() error {
	if w.response.Status != 200 {
		return fmt.Errorf("status esperado 200, obtido %d", w.response.Status)
	}
	if len(w.response.Results) == 0 {
		return fmt.Errorf("lista de resultados vazia")
	}
	return nil
}

func (w *buscaWorld) resultadoContem(titulo string) error { // Scenario Outline
	for _, a := range w.response.Results {
		if a.Title == titulo {
			return nil
		}
	}
	return fmt.Errorf("artigo %q não encontrado nos resultados", titulo)
}

func (w *buscaWorld) dentroDoOrcamento() error {
	if w.elapsedMs >= 800 {
		return fmt.Errorf("orçamento de 800ms estourado: %.0fms", w.elapsedMs)
	}
	return nil
}

// --- registry: regexp → handler (godog matches against the pt-BR step text) ----
func InitializeScenario(ctx *godog.ScenarioContext) {
	w := &buscaWorld{}
	ctx.Before(func(ctx context.Context, _ *godog.Scenario) (context.Context, error) {
		*w = buscaWorld{api: NewAPIClient()} // fresh state per scenario
		return ctx, nil
	})
	ctx.Step(`^que o sistema Interpop está acessível ao público$`, w.sistemaAcessivel)
	ctx.Step(`^existem (\d+) artigos publicados que contêm a palavra "([^"]*)"$`, w.semearArtigos)
	ctx.Step(`^o leitor busca por "([^"]*)"$`, w.leitorBusca)
	ctx.Step(`^o sistema apresenta uma lista de cards de artigos$`, w.listaPresente)
	ctx.Step(`^o resultado deve conter o artigo "([^"]*)"$`, w.resultadoContem)
	ctx.Step(`^a primeira tela completa carrega em menos de 800ms$`, w.dentroDoOrcamento)
}
