# OpenProject — backlog ↔ work packages (round-trip via API REST)

> **Quando usar esta referência**: quando o time controla o backlog no **OpenProject** e quer que a espinha
> `docs/backlog/` desta skill o *alimente*. O método **primário** é a **API REST v3 do OpenProject** (um pequeno
> adaptador Python que faz pull e push das work packages diretamente — roda em Linux/macOS/Windows). O template
> legado de **[Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)**
> `.xlsm` fica só como **fallback Windows-only** (§6). Esta skill é dona da **qualidade do item de backlog**
> (títulos em linguagem de negócio, BDD, prioridade, rastreabilidade); o OpenProject é dono do **acompanhamento da
> work package** (boards, sprints, responsáveis). Este arquivo é a ponte. **Opcional** — pule se o projeto não usa
> OpenProject.

> **Só `docs/backlog/` é projetado.** O lado `docs/requirements/` (`RF`/`RNF`) é o *porquê* — **não** é uma work
> package e **não** é exportado. As work packages são o backlog: **Epics → Features → User Stories** (e,
> opcionalmente, Tasks). A fonte de verdade fica em `docs/backlog/`; o projeto no OpenProject é uma *projeção*.

> ⚠️ **Por que a API é primária (e o `.xlsm` não).** O template Excel-sync do OpenProject dirige a API por meio de
> `winhttpcom.dll` — um componente COM **só do Windows**. No Linux/macOS (ou LibreOffice) a macro simplesmente não
> roda. Um projeto real (*"SIRA"*) bateu exatamente nessa parede e migrou para a API REST, que não precisa de nada
> além da stdlib do Python 3. Por isso esta skill usa a API por padrão e rebaixa a planilha a fallback.

---

## ✅ Para você usar — passo a passo simples (sem jargão)

Quer jogar o backlog inteiro no OpenProject sem digitar item por item? Este é o caminho simples — funciona em
**qualquer** computador (Windows, Mac ou Linux):

1. **Pegue seu código de acesso no OpenProject.** Entre → clique no seu nome (canto superior) → **My account**
   → **Access tokens** → crie um token **API**. Aparece um código — copie e guarde bem (trate como senha; nunca
   compartilhe nem comite no git).
2. **Conte três coisas à skill** (você define uma vez, como variáveis de ambiente — ou ponha o token num
   arquivinho `.env` que mantém privado):
   - o **endereço** do seu OpenProject (ex.: `https://openproject.sua-empresa.com`),
   - seu **código de acesso** (do passo 1),
   - seu **projeto** (o nome curto/slug, ou o número dele).
3. **Baixe o que já existe** (pra nada duplicar): peça pra mim (ou rode o adaptador) fazer **`pull`**. Ele salva
   uma foto das work packages atuais.
4. **Mande seu backlog.** Peça **`push`**. Primeiro ele mostra uma *prévia* (o que vai criar/atualizar, nada
   enviado ainda). Quando estiver certo, rode **de verdade** (`--apply`). O OpenProject cria seus Epics, Features e
   User Stories e **aninha um dentro do outro sozinho** (Epic no topo, Feature embaixo, e assim por diante) — você
   **não** liga nada na mão.
5. **Mudou o backlog depois?** É só `pull` e `push` de novo — ele **atualiza** o que já existe e só **cria** o que
   é novo (casa os itens pelo código `EP-NN`/`F-NN`/`USNN.M` no começo de cada título).

> **Servidor privado ou com certificado self-signed?** Se seu OpenProject roda num endereço interno com
> certificado "não confiável", há **um ajuste a mais** pra permitir (`OPENPROJECT_VERIFY_SSL=false`). Só faça isso
> num servidor que você controla e confia. Eu te guio.
>
> **Os "vínculos" entre tarefas que dependem umas das outras** (tipo "essa só depois daquela") são preenchidos num
> **segundo passo**, depois que os itens existem e têm número (§4). Eu te oriento na hora.

---

## 1. Autentique por ambiente (nunca chumbe um token)

O adaptador lê a configuração de variáveis de ambiente (o token pode, em vez disso, viver num `.env` como
`API_KEY=…`, mantido fora do git):

| Variável | O que é | Exemplo |
|---|---|---|
| `OPENPROJECT_URL` | URL base do seu OpenProject | `https://openproject.example.com` (ou `https://host:porta`) |
| `OPENPROJECT_TOKEN` | seu token de API (My account → Access tokens → **API**) | `a1b2c3…` *(ou `API_KEY=a1b2c3…` no `.env`)* |
| `OPENPROJECT_PROJECT` | identificador do projeto — **slug ou id numérico** | `meu-projeto` **ou** `163` |
| `OPENPROJECT_VERIFY_SSL` | `false` pra pular a checagem de TLS (self-signed/privado) — padrão `true` | `false` *(confiança proposital)* |

```bash
export OPENPROJECT_URL=https://openproject.example.com
export OPENPROJECT_TOKEN=xxxxxxxxxxxxxxxx     # ou API_KEY=... num .env fora do git
export OPENPROJECT_PROJECT=meu-projeto        # slug ou id numérico
# export OPENPROJECT_VERIFY_SSL=false         # só pra um cert self-signed que você confia
```

> **Esquema de auth**: HTTP Basic com o usuário literal `apikey` e o token como senha
> (`Authorization: Basic base64("apikey:<token>")`). É o esquema padrão de API-key do OpenProject.

---

## 2. O adaptador — pull / push (o caminho primário)

```bash
# 2.1 baixa as work packages atuais (a âncora do round-trip — carrega ids do OpenProject + lockVersion)
python3 assets/integrations/openproject-api.py pull --apply

# 2.2 projeta docs/backlog/ → OpenProject (DRY-RUN primeiro: imprime o plano CREATE/UPDATE, não envia nada)
python3 assets/integrations/openproject-api.py push
python3 assets/integrations/openproject-api.py push --apply            # executa
python3 assets/integrations/openproject-api.py push --with-tasks --apply  # também cria T/TX como Tasks
```

O que ele faz:

- **`pull`** — `GET /api/v3/projects/<projeto>/work_packages` paginado → grava
  `openproject/openproject_dump.json` (`{total, elements}`, as work packages cruas com `id`, `lockVersion`,
  `subject`, `description` e todos os `_links`). É isso que permite ao `push` **atualizar em vez de duplicar**.
- **`push`** — lê `docs/backlog/` com o **mesmo parser** do adaptador Excel (Epics → visão de produto; Features →
  descrição de negócio; os cabeçalhos `User story` dentro → seu **BDD** como descrição; Tasks só com
  `--with-tasks`), e para cada item:
  - **casa** uma work package existente pelo prefixo `<nosso-id>` do Subject (`EP-NN`/`F-NN`/`USNN.M`) →
    **UPDATE** (PATCH subject + descrição); senão **CREATE** (POST).
  - resolve o href do **tipo** via `GET /api/v3/types` (por nome — robusto mesmo quando nenhuma work package usa um
    tipo ainda; é a armadilha `KeyError: 'Task'` que o export do *"SIRA"* pegou) e o href da **prioridade** via
    `/api/v3/priorities`.
  - liga o **pai** por um link real de API (`_links.parent.href`) — §3.

Segurança embutida (lições do projeto real):

- **DRY-RUN por padrão** — o `push` imprime o plano e não envia nada até `--apply`.
- **Idempotente** — reexecutar `pull` e depois `push` atualiza o que existe e cria só o novo; seguro repetir.
- **Isolamento de erro por item** — uma work package que falha não aborta o lote (reporta `FAIL <id>` e segue;
  reexecute pra repetir só as que faltam).
- **Lock otimista** — relê o `lockVersion` de cada work package logo antes do PATCH e tenta de novo uma vez num
  conflito `409` (alguém editou no meio).
- **Retry/backoff** — em `429`/`5xx`, respeita `Retry-After` com backoff exponencial.

> **Regra do round-trip** (mesmo espírito de `references/integrations/sdd-interop.md`): a fonte de verdade do
> backlog fica em `docs/backlog/`. Quando algo muda no OpenProject durante a execução, reconcilie de volta nos
> arquivos do backlog primeiro, depois `push` de novo. O prefixo `<nosso-id>` no Subject é o que casa a work
> package de volta ao seu arquivo `docs/backlog/`.

---

## 3. A hierarquia é automática (links de pai reais)

O adaptador emite os itens em ordem de árvore (Epic → Feature → User story → Task) e define o
**`_links.parent.href`** de cada work package para o id OpenProject do seu pai (resolvido na hora: um pai criado
antes na mesma execução, ou já presente do `pull`). Assim o OpenProject **aninha a árvore por você** — você nunca
liga pai/filho na mão.

| Tipo | Profundidade | Pai |
|---|---|---|
| `Epic` | 0 | nenhum (raiz) |
| `Feature` | 1 | seu Epic |
| `User story` | 2 | sua Feature |
| `Task` | 3 | sua User Story (ou, para `TX` transversais, o Epic-filho *Apoio* sob a umbrella — §7) |

> **Nosso id vive no Subject, não numa coluna de id.** O OpenProject atribui seu **próprio** id numérico
> (diferente do nosso `EP-NN`/`F-NN`/`USNN.M`). Manter nosso id estável no **começo do Subject** mantém a
> rastreabilidade visível dentro do OpenProject e é exatamente o que o próximo `pull`/`push` usa pra recasar a work
> package.

---

## 4. Relations são um segundo passo (precisam dos ids do OpenProject)

**Relations** entre itens (`follows`, `blocks`, `precedes`, `relates`, `requires`, …) referenciam os **ids
numéricos** do OpenProject, que não existem até as work packages serem criadas. Então relations são um
**round-trip**, depois do primeiro `push`:

1. `push --apply` → hierarquia + descrições + prioridade criadas; o OpenProject atribui ids.
2. `pull --apply` → o dump agora tem todos os ids numéricos.
3. Crie as relations que quer com `POST /api/v3/work_packages/{id}/relations`
   (`{"_links": {"to": {"href": "/api/v3/work_packages/<outro-id>"}}, "type": "follows"}`).
4. Os **tipos de relation devem ser os termos em inglês da API**: `relates, duplicates, duplicated, blocks,
   blocked, precedes, follows, includes, partof, requires, required`.

> O backlog modela **hierarquia + rastreabilidade**, não dependências arbitrárias entre itens — então o adaptador
> não inventa relations; você adiciona as poucas que importam neste segundo passo.

---

## 5. Mapeamento de campos (o que a API carrega)

| Conceito | Campo da API | Origem em `docs/backlog/` |
|---|---|---|
| Tipo | `_links.type.href` (lookup por nome via `/types`) | o tipo do artefato (Epic/Feature/User story/Task) |
| Projeto | `_links.project.href = /api/v3/projects/<id>` | `OPENPROJECT_PROJECT` |
| Pai | `_links.parent.href = /api/v3/work_packages/<id>` | a hierarquia (§3) |
| Prioridade | `_links.priority.href` (lookup por nome via `/priorities`) | o emoji do item 🔴🟠🟡🟢 → `Immediate`/`High`/`Normal`/`Low` |
| Concorrência | `lockVersion` na raiz (obrigatório no PATCH) | do dump do `pull` (relido fresco antes de escrever) |
| Título | `subject` | o cabeçalho `# <nosso-id> — <título de negócio>` |
| Corpo | `description.raw` (markdown) | Epic = visão de produto · Feature = descrição de negócio · **User Story = seu BDD** |

---

## 6. Fallback Windows-only — o `.xlsm` da Excel-synchronization

Se você está no **Windows** e prefere uma planilha, o caminho legado ainda funciona. Há um segundo adaptador que
emite a tabela que o template Excel-sync do OpenProject espera:

```bash
python3 assets/integrations/project-to-openproject.py --apply           # CSV sempre; XLSX se openpyxl presente
python3 assets/integrations/project-to-openproject.py --with-tasks --apply
```

- Grava `openproject/openproject-backlog.csv` (+ `.xlsx` se `openpyxl` estiver instalado; `uv add openpyxl`).
- **Sete colunas**: `Type · ID · Subject · Priority · Description · Parent · Relations`. `ID`/`Parent`/`Relations`
  ficam em branco; o **Subject vem indentado 4 espaços por nível**, e no upload a macro lê a indentação, aninha a
  árvore e auto-preenche `Parent`.
- Receita: no OpenProject baixe o **template Excel-synchronization** (`.xlsm`), configure-o (URL, token, projeto),
  cole as colunas geradas, aperte **Ctrl + B** pra subir.

> ⚠️ **A macro é Windows-only** (`winhttpcom.dll`). No Linux/macOS/LibreOffice ela não envia. Lá, use o
> **adaptador da API REST** (§2). O `.xlsm` também é onde o token fica numa célula — mantenha esse arquivo
> **fora do git** (veja §7).

---

## 7. Segurança (lições do deploy real)

- **Token no ambiente ou num `.env` fora do git, nunca num arquivo comitado.** O `.xlsm` guarda o token numa
  célula — adicione `*.xlsm` (e `.env`, e qualquer pasta privada de scripts de API) ao `.gitignore`.
- **Espaço em branco no fim do `.env` → `401` silencioso.** Um espaço sobrando depois de `API_KEY=<token>` deixa o
  header de auth errado e o servidor responde `401 Unauthorized` sem causa óbvia. O adaptador **remove** espaços e
  aspas ao redor exatamente por isso; se levar um 401, cheque o espaço sobrando primeiro.
- **Servidor self-signed / privado**: `OPENPROJECT_VERIFY_SSL=false` desabilita a verificação de TLS — aceitável
  só num servidor que você controla. Prefira instalar a CA / usar um certificado de verdade quando puder.
- **Um token que já apareceu num terminal, log ou compartilhamento de tela está comprometido — rotacione.**
  Revogue em My account → Access tokens e emita um novo.

---

## 8. Os dois diretórios-bucket obrigatórios → Epics na raiz

O `docs/backlog/` da skill tem **diretórios-bucket estruturais**, irmãos de `epics/` e `features/`. O adaptador
os reconhece via `_BUCKETS` e mapeia cada **pasta en-CA** ao seu **título de Epic pt-BR**:

| Diretório-bucket (en-CA) | No export | Guarda (filhos) |
|---|---|---|
| `backlog/improvements/` | Epic-raiz **`Melhorias`** (*Improvements*) | cada `*.md` → filho Feature/User story |
| `backlog/bugs/` | **TYPE `Bug`**, parented à US/Feature violada (NÃO um Epic) | cada `BUG-NN-*.md` → um Bug sob sua Feature |
| `backlog/support-quality-investigation/` | Epic-raiz **`Atividades de Apoio, Qualidade e Investigação`** (umbrella) | três Epics filhos ↓ |
| &nbsp;&nbsp;`└ support/` | Epic-filho **`Apoio`** — **`TX`** transversal (Regra 6) | cada `TX-NN-*.md` → filho Task |
| &nbsp;&nbsp;`└ qa/` | Epic-filho **`Q&A`** — testes · reviews · quality gates | cada `QA-NN-*.md` → filho Task |
| &nbsp;&nbsp;`└ issues/` | Epic-filho **`Issues`** — inbox de triagem | cada `ISS-NN-*.md` → filho Task |
| &nbsp;&nbsp;&nbsp;&nbsp;`└ spikes/` | Epic-filho **`Spikes`** (sob Issues) — investigação time-boxed | cada `SPK-NN-*.md` → filho Task |

O **`README.md` de cada bucket é a descrição do Epic** (não exportado como item); todo arquivo ao lado é um
filho. A umbrella aninha Epics filhos (o emitter recursivo os percorre); o **Bug** é a exceção — um *type*
parented à Feature que viola (via a coluna `Parent` / um link de parent real), mantendo o defeito a um link do
`CA`. Os Subjects dos Epics umbrella/filhos não carregam `EP-NN` (o título *é* a identidade); o round-trip os
recasa por esse Subject exato. O scaffolder semeia cada bucket (idempotente, nunca sobrescreve), migra arquivos
pré-v1.21 `epics/EP-melhorias.md` / `EP-atividades-complementares.md`, **e migra um diretório v1.21
`atividades-complementares/` para `support-quality-investigation/support/`** (TX preservados). O usuário sempre
pode adaptar.

---

*Externo: [OpenProject API v3](https://www.openproject.org/docs/api/) ·
[Excel synchronization](https://www.openproject.org/docs/system-admin-guide/integrations/excel-synchronization/)
(fallback Windows-only; URLs podem mudar — busque "OpenProject API v3" / "OpenProject Excel synchronization").
Referências cruzadas: `05-convencoes-interpop.md` (ids, escala de prioridade, títulos em linguagem de negócio),
`04-bdd-criterios-aceitacao.md` (BDD = o conteúdo da User Story), `10-estrutura-projeto.md` (a espinha
`docs/backlog/`), `../integrations/README.md` (índice de integrações). Adotado aqui como ponte **opcional** de
acompanhamento de backlog — a fonte de verdade fica em `docs/backlog/`.*
