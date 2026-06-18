/* Step definitions — Cucumber wire protocol (pure C)
 * Binds: ../template-user-story.feature  (pt-BR Gherkin, `# language: pt`)
 *
 * @US: US30.1 · @F: F-30 · @EP: EP-10 · @CAs: CA01..CA11 · @Doc-Req: docs/specs/busca-editorial/REQUISITOS.md
 *
 * WHY THE WIRE PROTOCOL: there is no native Gherkin runner for pure C. The honest, portable route is the
 * Cucumber *wire protocol* — the `cucumber` runner connects over TCP to a step server you write in any
 * language (here, C) and asks it to match/invoke steps. Point it at the server with a
 * `features/step_definitions/interpop.wire` file:
 *       host: 127.0.0.1
 *       port: 3902
 * Then `cucumber` matches Dado/Quando/Então against the table in main() and invokes the C handlers below.
 * (Alternative: if the project already builds with C++, drive the C system-under-test from the cucumber-cpp
 *  harness via `extern "C"` — see cucumber_cpp.steps.cpp. Pick whichever your toolchain already has.)
 *
 * Build:  cc -o stepserver cucumber_wire_steps.c wire_server.c   Run:  ./stepserver & cucumber
 * wire_server.* (the thin TCP+JSON loop: step_matches → invoke → success/fail) is intentionally not shown —
 * this file is the step glue, kept UI-independent and deterministic. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "api_client.h"    /* ApiClient, SearchResponse, api_is_ready/seed_articles/get — system under test */
#include "wire_server.h"   /* WireResult, WIRE_OK, WIRE_FAIL(msg), register_step(), run_wire_server() */

/* per-scenario state — reset by a BeforeScenario hook the wire loop fires */
static ApiClient      api;
static SearchResponse response;
static double         elapsed_ms;

/* --- DADO ------------------------------------------------------------------- */
static WireResult sistema_acessivel(char **args, int argc) {
    (void) args; (void) argc;
    return api_is_ready(&api) ? WIRE_OK : WIRE_FAIL("api client não inicializado");
}

static WireResult semear_artigos(char **args, int argc) {       /* args[0]=n, args[1]=termo */
    (void) argc;
    char titulo[128];
    snprintf(titulo, sizeof titulo, "Sobre %s", args[1]);
    api_seed_articles(&api, atoi(args[0]), titulo, "publicado");
    return WIRE_OK;
}

/* --- QUANDO ----------------------------------------------------------------- */
static WireResult leitor_busca(char **args, int argc) {         /* Scenario Outline; args[0]=termo */
    (void) argc;
    char url[256];
    snprintf(url, sizeof url, "/api/v1/search/articles?q=%s", args[0]);
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    response = api_get(&api, url);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    elapsed_ms = (t1.tv_sec - t0.tv_sec) * 1000.0 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
    return WIRE_OK;
}

/* --- ENTÃO ------------------------------------------------------------------ */
static WireResult lista_presente(char **args, int argc) {
    (void) args; (void) argc;
    if (response.status != 200)    return WIRE_FAIL("status esperado 200");
    if (response.results_len == 0) return WIRE_FAIL("lista de resultados vazia");
    return WIRE_OK;
}

static WireResult resultado_contem(char **args, int argc) {     /* Scenario Outline; args[0]=titulo */
    (void) argc;
    for (size_t i = 0; i < response.results_len; i++)
        if (strcmp(response.results[i].title, args[0]) == 0) return WIRE_OK;
    return WIRE_FAIL("artigo não encontrado nos resultados");
}

static WireResult dentro_do_orcamento(char **args, int argc) {
    (void) args; (void) argc;
    return elapsed_ms < 800 ? WIRE_OK : WIRE_FAIL("orçamento de 800ms estourado");
}

/* --- registry: regex → handler (wire_server matches the pt-BR step text) ----- */
int main(void) {
    register_step("^que o sistema Interpop está acessível ao público$",                sistema_acessivel);
    register_step("^existem (\\d+) artigos publicados que contêm a palavra \"(.*)\"$", semear_artigos);
    register_step("^o leitor busca por \"(.*)\"$",                                     leitor_busca);
    register_step("^o sistema apresenta uma lista de cards de artigos$",               lista_presente);
    register_step("^o resultado deve conter o artigo \"(.*)\"$",                       resultado_contem);
    register_step("^a primeira tela completa carrega em menos de 800ms$",              dentro_do_orcamento);
    return run_wire_server(3902);   /* TCP loop: step_matches → invoke → success/fail */
}
