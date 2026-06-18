// Step definitions — cucumber-cpp (C++; the official Cucumber C++ backend)
// Binds: ../template-user-story.feature  (pt-BR Gherkin, `# language: pt`)
//
// @US: US30.1 · @F: F-30 · @EP: EP-10 · @CAs: CA01..CA11 · @Doc-Req: docs/specs/busca-editorial/REQUISITOS.md
//
// Setup:  cucumber-cpp + GTest (CMake: find_package(cucumber-cpp))   Build:  cmake --build .   Run:  cucumber
// cucumber-cpp reads `# language: pt`; the GIVEN/WHEN/THEN macros take a regex matching Dado/Quando/Então.
// REGEX_PARAM extracts each capture; ScenarioScope<> holds per-scenario state (fresh per scenario, isolated).
// Tip: this same harness tests *pure C* code — declare the C API with `extern "C"` and link the .c objects in.

#include <cucumber-cpp/autodetect.hpp>
#include <gtest/gtest.h>
#include <algorithm>
#include <chrono>
#include <string>
#include "api_client.hpp"   // ApiClient, SearchResponse, Article (system under test)

using cucumber::ScenarioScope;

struct BuscaCtx {
    ApiClient api;
    SearchResponse response;
    double elapsedMs = 0;
};

// --- DADO ----------------------------------------------------------------------
GIVEN("^que o sistema Interpop está acessível ao público$") {
    ScenarioScope<BuscaCtx> ctx;
    ASSERT_TRUE(ctx->api.isReady());
}

GIVEN("^existem (\\d+) artigos publicados que contêm a palavra \"(.*)\"$") {
    REGEX_PARAM(int, n);
    REGEX_PARAM(std::string, termo);
    ScenarioScope<BuscaCtx> ctx;
    ctx->api.seedArticles(n, "Sobre " + termo, "publicado");
}

// --- QUANDO --------------------------------------------------------------------
WHEN("^o leitor busca por \"(.*)\"$") {   // Scenario Outline binding
    REGEX_PARAM(std::string, termo);
    ScenarioScope<BuscaCtx> ctx;
    const auto start = std::chrono::steady_clock::now();
    ctx->response = ctx->api.get("/api/v1/search/articles?q=" + termo);
    ctx->elapsedMs = std::chrono::duration<double, std::milli>(
        std::chrono::steady_clock::now() - start).count();
}

// --- ENTÃO ---------------------------------------------------------------------
THEN("^o sistema apresenta uma lista de cards de artigos$") {
    ScenarioScope<BuscaCtx> ctx;
    ASSERT_EQ(200, ctx->response.status);
    ASSERT_FALSE(ctx->response.results.empty());
}

THEN("^o resultado deve conter o artigo \"(.*)\"$") {   // Scenario Outline
    REGEX_PARAM(std::string, titulo);
    ScenarioScope<BuscaCtx> ctx;
    const auto& r = ctx->response.results;
    ASSERT_NE(std::find_if(r.begin(), r.end(),
        [&](const Article& a) { return a.title == titulo; }), r.end());
}

THEN("^a primeira tela completa carrega em menos de 800ms$") {
    ScenarioScope<BuscaCtx> ctx;
    ASSERT_LT(ctx->elapsedMs, 800);
}
