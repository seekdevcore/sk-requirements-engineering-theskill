---
name: engenharia-de-requisitos
description: Use when the user is doing requirements engineering, business analysis, or software engineering tasks that involve discovering, specifying, validating, or managing software requirements. Triggers include (EN): requirements elicitation, stakeholder interviews, writing user stories, defining acceptance criteria, writing BDD scenarios, Planning Poker estimation, prototype validation of requirements, building a backlog (Epic → Feature → US → AC → Task), refining FRs/NFRs, requirement↔code↔test traceability, requirements change management, business analysis (AS-IS / TO-BE), professional computing ethics. Triggers (PT-BR): levantar requisitos, entrevistar stakeholders, escrever user stories, definir critérios de aceitação, escrever cenários BDD, estimar com Planning Poker, validar requisitos com protótipos, montar backlog (Epic → Feature → US → CA → Task), refinar RFs/RNFs, rastreabilidade requisito↔código↔teste, gestão de mudança de requisitos, análise de negócios (AS-IS / TO-BE), ética profissional em computação. Applies to new projects (no requirements yet) and to evolutions (changes in existing requirements). Not the right skill for pure code implementation — it is for the STAGE BEFORE (discovering what to build) and AFTER (validating that what was built is correct). IMPORTANT: Current content is written in pt-BR (Brazilian Portuguese); en-CA translation is on the roadmap.
language: en-CA
available_translations:
  - pt-BR
content_status:
  en-CA: roadmap
  pt-BR: available (current default content)
source: https://github.com/seekdevcore/sk-requirements-engineering-skill
risk: safe
license: CC-BY-SA-4.0
date_added: 2026-06-01
version: 1.0.0
---

# Engenharia de Requisitos (ER) + Análise de Negócios + Ética Profissional

> Skill construída a partir de 11 aulas do curso ERS (Eng. de Requisitos de Software) do IFPB Campus João Pessoa (Profa. Juliana Dantas Ribeiro Viana de Medeiros), Sommerville 10e (Cap. 4), Pressman, Wiegers, Falbo, BABOK e Código de Ética SBC 002/2024. Vocabulário em pt-BR (DADO/QUANDO/ENTÃO ao invés de Given/When/Then), porque o curso-fonte é em português e o usuário trabalha primariamente no Brasil.

---

## 1. Quando esta skill se aplica (gatilhos)

Invoque **antes** de:

- Iniciar um produto novo sem requisitos escritos
- Adicionar feature substancial a um produto existente
- Discutir o que será entregue numa sprint
- Escrever ou refatorar user stories, critérios de aceitação, cenários BDD
- Estimar esforço de stories (Planning Poker, Story Points)
- Avaliar se um requisito proposto é completo / correto / consistente / realista / necessário / priorizável / verificável
- Decidir entre construir ou comprar (estudo de viabilidade)
- Levantar requisitos não funcionais (desempenho, segurança, usabilidade, acessibilidade, conformidade legal)
- Discutir rastreabilidade entre requisito ↔ teste ↔ código
- Apoiar análise de negócio (mapear AS-IS, projetar TO-BE)
- Decisões com componente ético: privacidade, ML/IA, descontinuação de sistema, falha em projetar inclusão

**Não invoque** para tarefas puramente de implementação (codar, debugar, refatorar código já especificado). Para essas, use skills de programação/debugging — ER vem antes (o quê / por quê) e depois (foi entregue o certo?), não no meio (como codar).

---

## 2. Premissa central (regra inegociável)

> **Requisito ruim = produto ruim.** Não importa quão boa seja a implementação: se o requisito está errado, ambíguo, incompleto ou inviável, o sistema entregue não resolve o problema real. Sommerville (4.5): "O custo de corrigir um problema nos requisitos com uma alteração no sistema normalmente é muito maior do que o de consertar erros de projeto ou de código."

Por isso, ER é a fase de maior alavancagem do ciclo de software. **Não pule.** Mesmo em projetos ágeis pequenos, todo cartão do backlog é um requisito — só muda o nível de formalismo e o ciclo de revisão.

### 2.1 O documento de requisitos é a fonte da verdade (regra zero)

**O backlog NUNCA muda sem que o documento de requisitos mude primeiro.** O backlog é uma materialização do documento — organiza, fatia, prioriza — mas não decide escopo sozinho.

Isso significa:

- 🔁 **Antes de mexer em qualquer Epic/Feature/CA/RNF do backlog, verifique se houve alteração no documento de requisitos.** O cliente pode pedir adicionar/alterar/remover requisitos durante o projeto — essas mudanças têm que se propagar primeiro para o documento, depois para o backlog.
- 📎 O backlog **referencia de volta** o documento (cada Epic/Feature/CA tem campo `Origem (requisitos)` apontando para `RF-NN`/`RNF-NN` correspondente).
- ⚠️ Mudança aparecendo direto no backlog sem origem documentada é **suspeita**: ou é *scope creep* (escopo crescendo sem aprovação), ou é refinamento puramente técnico (deve virar Task, não Feature). Em ambos os casos, registrar no documento antes.
- 📅 O documento de requisitos tem **histórico de revisões** (versão, data, autor, mudança, impacto no backlog). Sem isso, ninguém lembra o que foi combinado em conversa de WhatsApp três sprints atrás.

**Padrão prático**: o BACKLOG.md tem no topo o link para o REQUISITOS.md + a data da última conferência (`Última verificação de alteração no documento: DD/MM/AAAA — sem mudanças`).

Templates prontos em [examples/template-documento-requisitos.md](examples/template-documento-requisitos.md) e [examples/template-backlog-openproject.md](examples/template-backlog-openproject.md).

---

## 3. O processo (mapa do território)

Sommerville e o curso IFPB adotam o **processo iterativo em espiral** (Fig 4.6 do livro):

```
                ┌─────────────────────────┐
                ↓                         │
   ┌──────────────────┐         ┌──────────────────┐
   │  Elicitação e    │ ──────→ │  Especificação   │
   │  análise         │         │  de requisitos   │
   │  (descoberta)    │         │  (documentar)    │
   └──────────────────┘         └──────────────────┘
                ↑                         │
                │                         ↓
                │              ┌──────────────────┐
                └────────────  │  Validação de    │
                               │  requisitos      │
                               │  (conferir)      │
                               └──────────────────┘
                                         │
                                         ↓
                                 Documento de requisitos
```

Atravessando as 3 fases, **dois processos contínuos**:

- **Gestão de mudança** (Sommerville 4.6): requisitos mudam — sempre. Precisa de processo para avaliar impacto + custo antes de aceitar.
- **Rastreabilidade**: cada requisito tem ID; cada decisão de projeto, teste e linha de código deve poder ser ligada de volta ao requisito que justifica sua existência.

Sub-processo dentro de Elicitação (Sommerville Fig 4.7):
**Descoberta → Classificação/Organização → Priorização/Negociação → Documentação** (em loop, com feedback contínuo).

---

## 4. Conceitos que você precisa antes de qualquer ação

### 4.1 Requisito de usuário vs requisito de sistema

| Nível | Linguagem | Audiência | Exemplo |
|---|---|---|---|
| **Usuário** | Natural, alto nível | Cliente, gerente, usuário final | "O sistema deve gerar relatório mensal de prescrições por clínica." |
| **Sistema** | Detalhado, mensurável | Dev, arquiteto, tester | "1.1 No último dia útil do mês, gerar resumo com nome, qtde de prescrições, dose total e custo, com acesso restrito por lista de controle." |

Ambos coexistem no documento. Usuário entende o de cima; dev implementa o de baixo.

### 4.2 Requisito Funcional (RF) vs Não Funcional (RNF)

- **RF**: o que o sistema **faz**. Entradas, saídas, comportamento, exceções.
- **RNF**: restrições sobre **como** o sistema funciona. Classificação Sommerville (Fig 4.3):
  - **Produto** — desempenho, confiabilidade, segurança da informação (security), usabilidade, acessibilidade
  - **Organizacional** — processo operacional, padrão de desenvolvimento, ambiente
  - **Externo** — regulatório, legislativo (LGPD/GDPR), ético

> **RNFs frequentemente são MAIS CRÍTICOS que RFs.** Sommerville (4.1.2): "Descumprir um requisito não funcional pode significar a inutilização total do sistema." Sistema funciona mas é lento → ninguém usa. Sistema funciona mas vaza dados → multa LGPD + fechamento.

**Regra de ouro do RNF: deve ser quantitativo.** "Fácil de usar" ❌ → "Usuário deve completar tarefa X em ≤2min após 1h de treinamento, com ≤2 erros/h" ✅. Veja métricas em [references/01-fundamentos.md](references/01-fundamentos.md).

### 4.3 Stakeholders

Todas as pessoas afetadas pelo sistema. Não só usuários finais. Exemplo Mentcare (Sommerville): pacientes, familiares, médicos, enfermagem, recepcionistas, TI, gestor de ética, gestores administrativos, controle de prontuário. **Stakeholder esquecido = requisito esquecido = retrabalho garantido.**

### 4.4 Estudo de viabilidade (3 perguntas, ANTES de qualquer outra coisa)

1. O sistema contribui para os objetivos da organização?
2. Cabe no cronograma e orçamento usando tecnologia atual?
3. Integra com os outros sistemas em uso?

Qualquer "não" → questione se o projeto deve prosseguir.

---

## 5. Detalhamento por fase (entry points para references/)

### Fase A — ELICITAÇÃO (descobrir)
6 técnicas, escolha pelo contexto. Tabela completa + quando usar em [references/02-elicitacao.md](references/02-elicitacao.md):

| Técnica | Boa para | Limitação |
|---|---|---|
| Entrevistas | Profundidade qualitativa, "o porquê e o como" | Habilidade do entrevistador; vieses |
| Questionários | Largura quantitativa, stakeholders dispersos | Profundidade baixa; respostas superficiais |
| Workshops / Brainstorming | Consenso, inovação, conflitos | Groupthink, dominância de comunicativos |
| Etnografia | Requisitos implícitos, processos reais | Caro, ruim para inovação radical |
| Análise de documentos | Regras formais, sistemas legados | Doc desatualizada; "como deveria" ≠ "como é" |
| Histórias e cenários | Discussão exploratória com stakeholder leigo | Não é especificação executável |

**Combine sempre 2+ técnicas.** Entrevista → questionário (qualitativo gera quantitativo). Análise docs + observação (formal vs real).

### Fase B — ESPECIFICAÇÃO (documentar)

**Hierarquia do backlog** (curso IFPB, OpenProject — versão completa, refletindo múltiplos Epics-raiz, Epic aninhado e BDD no campo Descrição):

```
📄 Documento de Requisitos (FONTE DA VERDADE — sempre cheque antes de mexer)
    │
    ▼
PROJETO (= repositório/contexto no OpenProject — NÃO é um EPIC)
    │
    ├─ 🟦 EPIC raiz #1                              ← uma frente do projeto
    │   └─ 🟦 EPIC sub                              ← sub-domínio (módulo, área)
    │       └─ 🟦 EPIC sub-sub                      ← sub-sub-domínio
    │           └─ 🟦 EPIC sub-sub-sub              ← IFPB chega a 4 níveis
    │               └─ 🟩 FEATURE                   ← entregável ao cliente
    │                   ├─ 📋 CA grupo "CA - <Tema A>"   ← CAs sempre agrupados
    │                   │    ├─ ✅ CA01 - regra autossuficiente
    │                   │    ├─ ✅ CA02 - regra autossuficiente
    │                   │    └─ ✅ CA03 - regra com sub-regras [...]
    │                   ├─ 📋 CA grupo "CA - <Tema B>"
    │                   │    └─ ✅ CA04 - ...
    │                   └─ 🟦 USER STORY                ← fatia de 1 sprint
    │                       ├─ 🎬 BDD: Cenário 1 (feliz)   ┐
    │                       ├─ 🎬 BDD: Cenário 2 (erro)    │ ← conteúdo do
    │                       └─ 🎬 BDD: Cenário 3 (alt.)    ┘   campo "Descrição"
    │                                                          da US (não cards)
    │                       └─ 🔧 TASK                       ← unidade técnica
    │                                                          (termos técnicos OK)
    │
    ├─ 🟦 EPIC raiz #2                              ← outra frente (irmão)
    │   └─ ... (mesma estrutura interna)
    │
    └─ 🟦 EPIC raiz #N                              ← outras frentes (irmãs)
        └─ ...
```

> **🔴 Regra: múltiplos Epics-raiz, sem "Epic-projeto" único**. Um projeto tipicamente tem **vários Epics no nível mais alto, irmãos entre si**, sem um nó-pai comum. Cada Epic-raiz é uma **frente independente** (plataforma, área operacional, módulo transversal). O "produto" como um todo é o **contexto/repositório** do projeto no OpenProject — não um item da hierarquia. Forçar tudo embaixo de um único "Epic Produto" cria nó-pai vazio e atrapalha navegação. Exemplos reais: Controle Dopagem tem `EPIC APLICAÇÃO WEB` · `EPIC APLICAÇÃO MOBILE` · `EPIC ATIVIDADES DE APOIO` (3 irmãos); Interpop tem `EP-10 Busca` · `EP-09 Filtros` · `EP-15 Newsletter` · `EP-20 Moderação` (vários irmãos). Detalhamento em [`examples/template-backlog-openproject.md §3`](examples/template-backlog-openproject.md).

**Templates prontos para copiar:**
- 📋 [`examples/template-backlog-openproject.md`](examples/template-backlog-openproject.md) — backlog completo com Busca Editorial Interpop preenchida + Cadastro de Atletas mostrando 4 níveis de Epic
- 📋 [`examples/template-documento-requisitos.md`](examples/template-documento-requisitos.md) — documento de requisitos (IEEE 830 + Sommerville + Wiegers)
- 🎬 [`examples/template-user-story.feature`](examples/template-user-story.feature) — arquivo Gherkin pronto com 4 cenários + Esquema do Cenário + step definitions de exemplo (Python + TypeScript)

**Distinção crítica Feature ↔ User Story** (regra dura — anti-padrão "Feature com BDD" em [04-bdd-criterios-aceitacao.md §7.7](references/04-bdd-criterios-aceitacao.md)):
- **Feature** tem **descrição em pt-BR** (parágrafo de negócio explicando o entregável ao cliente) + **CAs**. NUNCA tem BDD.
- **User Story** tem **BDD em pt-BR** (`Dado/Quando/Então`, no próprio campo "Descrição" — não como cards filhos) + **CAs herdados** via rastreabilidade. Nunca tem CAs próprios.

**Regra ampliada: TODOS os artefatos têm descrição em linguagem de negócio.** Epic, Feature, User Story, CA, RNF, regra de negócio (G) — todos descritos em pt-BR sem termo técnico (sem URL, sem nome de método, sem nome de tabela, sem stack). Quem lê: cliente, PO, dev júnior, auditor — todos sem glossário técnico. Endpoints e libs só aparecem em **Tasks**.

**Convenção `[...]` para CAs com sub-regras** (regra dura — detalhamento em [04-bdd §2.x](references/04-bdd-criterios-aceitacao.md)):

Quando um CA precisa de sub-regras para ser totalmente testável, **encerre o título com `[...]`** e detalhe no corpo do item (campo "descrição" no OpenProject) abrindo com `Regras a serem aplicadas:` + bullets. CA sem `[...]` deve ser **autossuficiente no título**.

```
Exemplo CA com [...] (precisa abrir o item):
  CA09 - O combobox FEDERAÇÃO deve aplicar as regras de preenchimento
         e validação conforme detalhamento [...]
  Corpo:
    Regras a serem aplicadas:
    - Só deverá ser habilitado se tiver uma CONFEDERAÇÃO selecionada.
    - Só deve exibir as Federações ATIVAS.
    - Em ordem ALFABÉTICA.
    - ...

Exemplo CA autossuficiente (sem [...]):
  CA05 - O campo CPF não é obrigatório. Mas se preenchido, deverá ser no
         formato XXX.XXX.XXX-XX. Se o CPF for inválido, emitir mensagem de erro.
```

Quem lê o backlog em modo lista vê o `[...]` e sabe que precisa clicar. Sem ambiguidade.

**Regra do título da User Story**: no card, use **título curto descritivo** ("US Listagem Básica de Atletas"). NÃO escreva o template Connextra inteiro ("Como editor, eu quero …, para que …") no título — esse template existe para **conversa**, não para card. Detalhamento em [references/03-especificacao.md](references/03-especificacao.md).

---

#### 🔴 Convenções de naming Interpop/IFPB (regra dura — vale em todo projeto pt-BR deste autor)

Aplicam-se a TODOS os títulos de Epic, Feature, User Story, CA e RNF. **Tasks podem violar** (termos técnicos são permitidos lá).

1. **Sem infinitivo** nos títulos. Use substantivo/gerúndio descritivo.
   - ❌ `Listar reservas do usuário` → ✅ `Listagem de reservas do usuário`
   - ❌ `Buscar artigos` → ✅ `Busca de artigos`
   - ❌ `Cadastrar atleta` → ✅ `Cadastro de atleta`

2. **Sem termos técnicos** em títulos nem descrições de Epic/Feature/US/CA/**RF**/RNF/G. Termos técnicos só aparecem nas Tasks. Vale tanto para o **backlog** (Epic/Feature/US/CA) quanto para o **documento de requisitos** (RF/RNF/G) — ambos são lidos por stakeholders, não por dev.
   - ❌ `Endpoint REST de busca` → ✅ `Busca de artigos por texto`
   - ❌ `Hook useSearch com TanStack` → ✅ `Apresentação dos resultados em tempo real`
   - ❌ `Migration tabela search_index` → ✅ (não é Feature; vira Task técnica)
   - ❌ CA: `Endpoint POST /api/v1/bans/ retorna 400 se hierarquia violada` → ✅ `Quando um administrador tenta banir outro administrador, o sistema rejeita a operação com a mensagem "Operação não permitida".`

3. **Pt-BR explícito, simples, direto** — quem lê deve entender sem contexto técnico.

4. **Todos os artefatos têm descrição em linguagem de negócio.** Epic, Feature, US, CA, **RF**, RNF, regra de negócio (G). Lida por qualquer stakeholder (PO, cliente, dev júnior, auditor) sem precisar de glossário. Sem URLs, sem nomes de método, sem stack. Endpoints e libs só nas Tasks. **Relação RF ↔ Feature**: RF é o requisito declarado no documento; Feature é a materialização incremental dele no backlog (com rastreabilidade via campo `Origem (requisitos)`).

5. **CAs sempre agrupados** sob um título `CA - <Tema>`, mesmo Feature com 1 só CA. O agrupamento mantém consistência visual no OpenProject e facilita inserção futura (ver template em [examples/template-backlog-openproject.md](examples/template-backlog-openproject.md) §4).

6. **Configurações técnicas NÃO são Features** (ESLint, variáveis de ambiente, criação de pastas, arquivos JSON, Vite config, lint config, docker-compose). Vão como **Tasks transversais** (`TX-NN`), agrupadas para visibilidade do time técnico, fora da hierarquia de Features. A regra mestra: **Feature = entregável ao cliente**. Se não é entregável ao cliente final, não é Feature.

7. **Escala de prioridade Interpop** (aplicada em TODOS os níveis: Epic, Feature, US, CA, Task):
   - 🔴 **Immediate** — bloqueia outras coisas; sprint atual obrigatoriamente
   - 🟠 **High** — sprint atual ou próxima
   - 🟡 **Normal** — backlog priorizado
   - 🟢 **Low** — nice to have, sem deadline

   > MoSCoW (Must/Should/Could/Won't) é equivalente teórico mas a equipe Interpop usa Immediate/High/Normal/Low. Use essa escala em projetos brasileiros deste autor.

8. **IDs estáveis** (formato Interpop):
   - `EP-NN` (Epic, podendo ser aninhado: `EP-NN.M`, `EP-NN.M.K`) · `F-NN` (Feature) · `CANN` (Critério de Aceitação) · `USNN.M` (User Story) · `TNN.M.K` (Task) · `TX-NN` (Task transversal)
   - IDs são eternos (não renumeram em mudança); versão do artefato muda.

**Template completo de BACKLOG.md** + exemplos do projeto SIRA e Interpop em [references/05-convencoes-interpop.md](references/05-convencoes-interpop.md).

**Critérios de Aceitação + BDD são complementares, não competem:**

- **CA** é regra declarativa por feature: "CA05 — O campo CPF não é obrigatório. Se preenchido, deve estar no formato XXX.XXX.XXX-XX." Lista de regras testáveis.
- **BDD** é cenário executável por user story: "DADO que o usuário está logado e tem permissão / QUANDO acessa o menu administrativo > Atletas / ENTÃO o sistema exibe a lista básica de atletas."

CA define o **invariante**; BDD define a **interação**. Use os dois. Detalhamento em [references/04-bdd-criterios-aceitacao.md](references/04-bdd-criterios-aceitacao.md).

### Fase C — ESTIMATIVA (dimensionar)

Story Points (medida abstrata de complexidade) + Planning Poker (Fibonacci: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 + `?` + 100).

- `?` = falta entendimento → conversar com PO
- `100` = é épico disfarçado → fatiar em stories
- 0 e 1/2 não entram na 1ª rodada — reservados para itens triviais futuros (label, troca de cor)

Procedimento: escolher história-guia (mais simples = 1pt) → estimar restantes em proporção (não próximo número na escala). Detalhamento em [references/05-estimativa.md](references/05-estimativa.md).

### Fase D — VALIDAÇÃO (conferir que é o certo)

**5 conferências Sommerville:** validade · consistência · completude · realismo · verificabilidade.

**7 dimensões Falbo (por requisito):** completo · correto · consistente · realista · necessário · passível de priorização · verificável.

**3 técnicas:** revisões de requisitos (walkthrough), prototipação (lo-fi → hi-fi), geração de casos de teste a partir do requisito.

Protótipos são a ferramenta mais eficaz porque o usuário VÊ o resultado. Comece em papel/quadro, evolua para Figma quando necessário. Detalhamento em [references/06-validacao.md](references/06-validacao.md).

### Fase E — MUDANÇA + RASTREABILIDADE (manter coerência)

Requisitos **duradouros** (atividades centrais; mudam lentamente) vs **voláteis** (apoio; mudam frequentemente). Diferencie ao priorizar arquitetura.

Processo formal de mudança (Sommerville Fig 4.19):
**Problema identificado → análise/especificação → análise de impacto + custo → implementação** (com rollback no documento de requisitos sincronizado com código).

Rastreabilidade: cada requisito ID → projeto → código → teste. Sem isso, mudar 1 requisito vira "que módulos eu mexo?". Detalhamento em [references/07-mudanca-rastreabilidade.md](references/07-mudanca-rastreabilidade.md).

---

## 6. Camada transversal: o analista de negócios

Em times pequenos, dev + PO acumulam o papel. Em times maiores, há analista dedicado. O BABOK (Business Analysis Body of Knowledge) define 6 áreas de conhecimento: planejamento, elicitação, gerenciamento do ciclo de vida, análise de estratégia, análise de requisitos e design de solução, avaliação. Fluxo central: **AS-IS** (processo atual) → **TO-BE** (processo desejado) → análise GAP → requisitos do sistema que cobrem o GAP. Detalhamento em [references/08-analista-negocios.md](references/08-analista-negocios.md).

---

## 7. Camada transversal: ética profissional

> Esta é uma camada **inegociável**. Não está acima das outras — está embaixo de todas. Código SBC 002/2024 (versão pt-BR do IFIP, adaptação do ACM): "A profissão de Computação como um todo se beneficia quando o processo de tomada de decisão ética ocorre de forma responsável e transparente."

Princípios que mais incidem em ER:

- **1.1 Bem-estar humano** — "necessidades dos menos favorecidos devem receber maior atenção"
- **1.2 Evitar danos** — relatar riscos do sistema mesmo se isso atrasa entrega
- **1.6 Privacidade** — coleta mínima, consentimento, retenção definida (LGPD c/c)
- **2.5 Avaliação abrangente** — sistemas de **ML exigem reavaliação contínua de risco**
- **2.6 Trabalhar só em áreas de competência** — comunicar limitações ao cliente
- **2.9 Sistemas seguros** — "quando uso indevido ou danos são previstos ou inevitáveis, **a melhor opção pode ser não implementar o sistema**"
- **3.1 Bem público no centro** — cita explicitamente "análise de requisitos" como momento de avaliação ética

Detalhamento e aplicação em [references/09-etica-sbc.md](references/09-etica-sbc.md).

---

## 8. Anti-padrões frequentes (evite estes)

1. **Pular elicitação** — "já sei o que o cliente quer" → custo de retrabalho 10× a 200× o de fixar na fase certa
2. **Connextra no título** — "Como [X], eu quero [Y] para que [Z]" no título do card vira ilegível; use no campo de descrição/conversa, não no título
3. **RNF qualitativo** — "deve ser rápido" não é requisito, é desejo. Quantifique sempre
4. **CA e BDD competindo** — escrever só um dos dois. São camadas complementares (invariante × interação)
5. **Storyteller sem stakeholder** — escrever requisitos sozinho. Requisito sem dono = requisito que ninguém valida
6. **Aceitar tudo sem priorizar** — backlog de 200 itens sem ordem é o mesmo que backlog vazio
7. **Esquecer mudança** — desenhar arquitetura assumindo que os requisitos não mudam → reescrita total em 6 meses
8. **Ignorar rastreabilidade** — impossível analisar impacto de mudança sem ID/link entre artefatos
9. **Ética como afterthought** — questões éticas devem entrar nos critérios de aceitação, não num documento separado que ninguém lê
10. **Etnografia em projeto inovador** — etnografia ótima para sistema-substituto; péssima para produto que ainda não existe (Nokia × Apple)
11. **Feature com BDD em vez de descrição** — colar `DADO/QUANDO/ENTÃO` direto na Feature em vez do parágrafo em pt-BR de negócio. Resultado: stakeholder não-técnico não lê, CAs ficam órfãos, Sprint Planning trava. BDD vive na **User Story**. Detalhamento e exemplos ❌/✅ em [04-bdd-criterios-aceitacao.md §7.7](references/04-bdd-criterios-aceitacao.md)
12. **Backlog sem origem no documento de requisitos** — Epic/Feature/CA que aparece no backlog sem `Origem (requisitos)` apontando para `RF-NN`/`RNF-NN` é scope creep silencioso ou refinamento técnico mal colocado. Toda mudança nasce no documento; backlog só materializa (ver §2.1).
13. **Termo técnico em CA** — `CA: O endpoint POST /api/v1/bans/ retorna HTTP 400 se hierarquia violada` força o auditor/cliente a abrir glossário. Reescreva em linguagem de negócio: `CA: Quando um administrador tenta banir outro administrador, o sistema rejeita a operação com a mensagem "Operação não permitida".` Endpoint e HTTP status ficam na Task.

---

## 9. Checklist de aplicação (use a cada feature)

Antes de aceitar uma feature no backlog, valide os 7 pontos de Falbo:

- [ ] **Completo** — descreve a funcionalidade/regra/restrição inteira
- [ ] **Correto** — descreve exatamente o que deve ser construído
- [ ] **Consistente** — não ambíguo, não conflita com outro requisito
- [ ] **Realista** — implementável dado o que sabemos da plataforma
- [ ] **Necessário** — cliente precisa OU exigência externa/padrão
- [ ] **Passível de priorização** — tem ordem clara vs outros itens
- [ ] **Verificável** — dá para escrever teste que prove implementação

Falhou em ≥1 → não está pronto. Volte ao stakeholder.

### Checklist adicional de naming (regra dura — Interpop)

Antes de aceitar Epic/Feature/US no backlog:

- [ ] Título **NÃO começa com infinitivo** (sem `Listar`/`Criar`/`Buscar`/`Cadastrar`/`Configurar`/`Implementar`)
- [ ] Título **NÃO contém termos técnicos** (sem `endpoint`/`hook`/`migration`/`API`/`schema`/`config`)
- [ ] Título em **pt-BR explícito** legível por stakeholder não-técnico
- [ ] Item **é entregável ao cliente** (se é configuração técnica, mover para Task transversal `TX-NN`)
- [ ] Prioridade declarada (🔴 Immediate / 🟠 High / 🟡 Normal / 🟢 Low)
- [ ] **Feature** tem **descrição em parágrafo** · **User Story** tem **BDD `Dado/Quando/Então`** (não trocar)
- [ ] Cada User Story tem **CAs associados explicitamente** (relação rastreável)
- [ ] Cada Task tem **Task ID** (`TNN.M.K` ou `TX-NN`) para aparecer em commit/PR

Falhou em ≥1 → não está pronto. Corrija antes de descer para implementação.

---

## 10. Fonte primária e bibliografia canônica

### 10.1 Autora do material-fonte (corpus primário desta skill)

O corpus primário desta skill — todas as 11 aulas processadas (LECTURE 0 a 10, incluindo 09.2) — foi criado e ministrado pela **Profa. Dra. Juliana Dantas Ribeiro Viana de Medeiros** ([Lattes](http://lattes.cnpq.br/9730254173461923) · [ORCID 0000-0001-8387-4616](https://orcid.org/0000-0001-8387-4616)).

Por que isso importa para a confiabilidade do que a skill afirma:

- **Doutorado em Engenharia de Software** (UFPE 2017) com período sanduíche na **Universidade Nova de Lisboa** (2016, bolsa Erasmus Mundus BEMUNDUS), sob orientação de Alexandre Marcos Lins de Vasconcelos e co-orientação de Miguel Goulão (UNL) e Carla Schuenemann.
- **Tese de doutorado**: *"An approach to support the Requirements Specification in Agile Software Development"* — o **tema exato** que esta skill condensa.
- **Linha de pesquisa ativa**: "Engenharia de Requisitos em Projetos Ágeis" (desde 2014, IFPB).
- **Coordenadora do projeto CNPq DTI-A 487777/2013-1** — *Sistema de Informação Integrado para Controle de Dopagem* (2014–2015), que é a **origem do caso de estudo principal** em [`examples/caso-controle-dopagem.md`](examples/caso-controle-dopagem.md).
- **20+ anos de experiência industrial** em gerência e desenvolvimento de software: DATAPREV (Ministério do Trabalho, 2006–2013), CESAR (Recife, 2005–2006), CAGEPA, Ministério Público da Paraíba, Prefeitura de João Pessoa/PB (sistemas tributários IPTU/ITBI/Taxa de Lixo, 1997–2005), e colaborações com Multilaser e CPM Braxis.
- **Professor Efetivo, Dedicação Exclusiva** no IFPB Campus João Pessoa desde 2006 (ingresso por concurso público, **1º lugar**); pesquisadora ativa no polo **EMBRAPII** do IFPB; vinculada também à UFCG desde 2020.
- Mestrado em Ciência da Computação (UFPE 2001, bolsa CNPq, dissertação sobre ISO 9001:2000 em empresas de software) e Graduação em Ciência da Computação (UFPB 1997).

> **Citação acadêmica**: Medeiros, J. D. R. V. de. *Engenharia de Requisitos de Software* [material didático, aulas 0–10]. IFPB Campus João Pessoa, 2025. Lattes: http://lattes.cnpq.br/9730254173461923. ORCID: https://orcid.org/0000-0001-8387-4616.

### 10.2 Bibliografia canônica (complementa o corpus primário)

- **Sommerville, I.** Engenharia de Software, 10ª ed. Pearson, 2019 — base do curso (Cap. 4 é o pivô)
- **Pressman, R.** Engenharia de Software, 9ª ed. AMGH, 2021 — visão complementar (7 etapas de ER)
- **Wiegers, K. & Beatty, J.** Software Requirements, 3rd ed. Microsoft Press
- **Cohn, M.** User Stories Applied, 2004 — referência padrão de US
- **Robertson, S. & Robertson, J.** Mastering the Requirements Process (método VOLERE)
- **Hull, E., Jackson, K., Dick, J.** Requirements Engineering, 4th ed. Springer
- **IIBA.** BABOK Guide v3 — análise de negócios
- **Falbo, R. A.** Notas de Aula — Engenharia de Requisitos de Software (UFES)
- **SBC.** Resolução 002/2024 — Código de Ética e Conduta Profissional
- **Valente, M. T.** Engenharia de Software Moderna, 2020 ([engsoftmoderna.info](https://engsoftmoderna.info)) — cap. 3 (MVP + Testes A/B)

---

**Para detalhar qualquer ponto acima, vá direto ao arquivo de references/ correspondente.** Esta SKILL.md é o mapa; o detalhe vive lá. Não tente substituir as leituras canônicas: esta skill condensa para uso imediato, mas as decisões importantes merecem o livro inteiro.
