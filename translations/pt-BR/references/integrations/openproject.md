# OpenProject — sincronização backlog → Excel (integração opcional)

> **Quando usar esta referência**: quando o time rastreia o backlog no **OpenProject** e quer que a espinha
> `docs/backlog/` desta skill o *alimente* através da **[sincronização Excel do OpenProject](https://www.openproject.org/pt/docs/system-admin-guide/integrations/excel-synchronization/)**
> (um template `.xlsm` fornecido pelo OpenProject que envia/recebe work packages via API). Esta skill é dona da
> **qualidade do item de backlog** (títulos em linguagem de negócio, BDD, prioridade, rastreabilidade); o OpenProject é dono do
> **rastreamento do work package** (boards, sprints, responsáveis). Este arquivo é a ponte. **Opcional** — pule se o
> projeto não usar OpenProject.

> **Apenas `docs/backlog/` é projetado.** O lado `docs/requirements/` (`RF`/`RNF`) é o *porquê* — **não** é
> um work package e **não** é exportado. Os work packages são o backlog: **Epics → Features → User Stories**
> (e, opcionalmente, Tasks). A fonte de verdade permanece em `docs/backlog/`; o projeto no OpenProject é uma *projeção*.

---

## ✅ Para você usar — passo a passo (sem jargão)

Quer jogar todo o seu backlog dentro do OpenProject sem digitar item por item? É assim:

1. **Pegue sua chave de acesso no OpenProject.** Entre na sua conta → clique no seu nome (canto) → **Minha conta** → **Tokens de acesso** → criar. Vai aparecer um código — copie e guarde bem (trate como senha; não compartilhe).
2. **Baixe a planilha do OpenProject.** Na página de sincronização por Excel do OpenProject, baixe a planilha que eles oferecem e abra. Quando perguntar, **permita os macros** (é o que faz a planilha conversar com o OpenProject). Nela, cole o endereço do seu OpenProject, a sua chave de acesso (do passo 1) e o nome do seu projeto.
3. **Gere a sua lista com a skill.** Peça pra mim (ou rode a skill) "gerar o backlog pro OpenProject". Eu crio um arquivo (uma planilha) com seus Epics, Features e User Stories já na ordem certa.
4. **Cole na planilha do OpenProject.** Copie as colunas do arquivo que eu gerei e cole na planilha do OpenProject.
5. **Envie.** Aperte o botão de enviar (Ctrl + B). Pronto — o OpenProject cria tudo e **encaixa um item dentro do outro sozinho** (Epic em cima, Feature embaixo, e assim por diante). Você **não precisa** ligar um no outro na mão.

> **Preciso de chave/token?** Sim — só a da sua própria conta (passo 1). É de graça e leva 1 minuto.
>
> **As "ligações" entre tarefas que dependem uma da outra** (tipo "essa só depois daquela") só dá pra preencher **depois** que o OpenProject criou tudo: você baixa a lista de volta do OpenProject (que agora tem um número pra cada item), preenche essas ligações e envia de novo. Eu te explico na hora.

---

## 1. O padrão de colunas (o default da skill — adaptável)

A exportação tem **sete colunas**, nomeadas como o template de sincronização Excel do OpenProject as usa:

| Column | O que carrega | Regra |
|---|---|---|
| **Type** | o tipo do work package | `Epic` · `Feature` · `User story` · `Task` (combine com os nomes de tipo configurados no seu OpenProject) |
| **ID** | o id numérico próprio do OpenProject | **deixado em branco** numa exportação nova — o OpenProject **atribui** na importação (o id dele ≠ o nosso) |
| **Subject** | o título legível, **indentado** | `<nosso-id> <título em linguagem de negócio>` (`EP-10 Gestão de Salas`, `F-26 Aprovação de reserva`, `US25.2 …`), **prefixado com 4 espaços por nível de hierarquia** (ver §2) |
| **Priority** | a prioridade do work package | escala *"Interpop"* → OpenProject: 🔴 `Immediate` · 🟠 `High` · 🟡 `Normal` · 🟢 `Low` |
| **Description** | o campo Description do OpenProject | **a description de uma User Story É o seu BDD** (os cenários Gherkin); uma **Feature** carrega sua description em linguagem de negócio; um **Epic**, sua visão de produto |
| **Parent** | o work package pai | **deixado em branco** — auto-preenchido pelo OpenProject a partir da indentação do Subject (§2) |
| **Relations** | dependências (follows/blocks/…) | **deixado em branco** — uma segunda passada (§3); precisa dos ids do OpenProject |

> **Por que nosso id mora no Subject, e não na coluna ID** — o `ID` do OpenProject é atribuído automaticamente e é *dele*
> (um número diferente do nosso `EP-NN`/`F-NN`/`USNN.M`). Colocar nosso id estável no **início do Subject**
> mantém a rastreabilidade visível dentro do OpenProject (e sobrevive à reimportação), exatamente como a UI do OpenProject
> renderiza. A coluna `ID` fica em branco para que o OpenProject crie + numere o work package.

---

## 2. A hierarquia é automática (sem parent/child manual)

O template de sincronização Excel do OpenProject constrói a hierarquia parent/child a partir da **indentação**: **4 espaços
vazios antes do Subject** marcam um work package como filho. O adaptador emite o Subject já indentado conforme a profundidade, então,
no upload, o OpenProject **aninha a árvore e auto-preenche a coluna `Parent` para você** — você nunca conecta as
relações na mão.

| Type | Profundidade | Indentação do Subject |
|---|---|---|
| `Epic` | 0 | `EP-10 Gestão de Salas (Admin)` |
| `Feature` | 1 | `····F-26 Aprovação de reserva` |
| `User story` | 2 | `········US25.2 Recursos de Filtragem…` |
| `Task` | 3 | `············T-26.1.1` |

(`·` = um espaço. O marcador de 4 espaços é o default do OpenProject; as linhas são emitidas em ordem hierárquica para que a
indentação aninhe corretamente.)

---

## 3. As Relations são uma segunda passada (precisam dos ids do OpenProject)

As **Relations** entre itens (`follows`, `blocks`, `precedes`, `relates`, `requires`, …) usam a coluna `Relations`
com a sintaxe `"<type> <id>, <type> <id>"` (ex.: `follows 12345, precedes 45678`) — e o **id é
do OpenProject**, que **não existe até a primeira importação**. Então as relations são um **round-trip**:

1. Rode o adaptador → importe a tabela (hierarquia + descriptions + prioridade criadas; o OpenProject atribui ids).
2. **Exporte os work packages de volta do OpenProject** (*download* da sincronização Excel) — agora cada linha tem seu id numérico.
3. Preencha a coluna `Relations` com `"<type> <id-do-openproject>"` para as dependências que você quer.
4. Reimporte (upload) → o OpenProject conecta as relations.

> O adaptador emite `Relations` como uma coluna **vazia** (o backlog modela hierarquia + rastreabilidade, não
> dependências arbitrárias entre itens). Os **tipos de relação devem ser os termos da API em inglês**: `relates, duplicates,
> duplicated, blocks, blocked, precedes, follows, includes, partof, requires, required`.

---

## 4. O adaptador

```bash
# dry-run (imprime a tabela de work packages, não escreve nada)
python3 assets/integrations/project-to-openproject.py

# escreve (CSV sempre; XLSX também quando openpyxl está instalado)
python3 assets/integrations/project-to-openproject.py --apply
python3 assets/integrations/project-to-openproject.py --with-tasks --apply   # também emite T/TX como Tasks
```

- Lê `docs/backlog/epics/*.md` (→ `Epic`, description = visão de produto) e `docs/backlog/features/*.md`
  (→ `Feature`, description = parágrafo de negócio; os cabeçalhos `User story` internos, description = o BDD deles;
  `Task` apenas com `--with-tasks`).
- Escreve `openproject/openproject-backlog.csv` (stdlib, sempre) e `openproject/openproject-backlog.xlsx`
  (apenas se `openpyxl` estiver disponível — `uv add openpyxl` / `pip install openpyxl`; somente CSV caso contrário; o XLSX
  faz wrap da coluna Description).
- **Dry-run por padrão**, `--apply` para escrever, **nunca sobrescreve** um arquivo existente.
- O título vem do cabeçalho `# <id> — <título>`; a prioridade do emoji do item (🔴🟠🟡🟢) ou de uma
  linha `Prioridade`/`Priority`; prioridade ausente assume `Normal` por padrão.

### A receita de sincronização Excel

1. No OpenProject, baixe o **template de sincronização Excel** (`.xlsm`) conforme a
   [documentação do OpenProject](https://www.openproject.org/pt/docs/system-admin-guide/integrations/excel-synchronization/)
   e configure-o (URL, token de API, projeto).
2. Rode o adaptador (`--apply`) → abra `openproject/openproject-backlog.xlsx` (ou `.csv`).
3. **Cole as colunas** no template de sincronização (deixe `ID`/`Parent`/`Relations` vazios para novos work packages).
4. Faça o upload (`Ctrl + B`) → o OpenProject cria os Epics/Features/User Stories, **aninha-os a partir da indentação**,
   atribui ids e preenche `Parent`. Para as relations, faça o round-trip da §3.

> **Regra de round-trip** (mesmo espírito de `references/integrations/sdd-interop.md`): a fonte de verdade do backlog
> permanece em `docs/backlog/`. Quando algo muda no OpenProject durante a execução, reconcilie-o de volta nos
> arquivos do backlog primeiro, depois reexporte. O prefixo `<nosso-id>` no Subject é o que permite casar um work package
> de volta com seu arquivo `docs/backlog/`.

---

## 5. Os dois Epics raiz obrigatórios (default da skill)

A hierarquia de backlog padrão da skill (do curso *"IFPB"*) sempre termina com **dois Epics raiz obrigatórios**,
irmãos dos Epics feature-front do projeto:

- **`Improvements`** (pt-BR *"Melhorias"*)
- **`Complementary Activities`** (pt-BR *"Atividades complementares"*)

Eles são gerados pelo scaffolder com a mesma lógica idempotente *create-if-missing / never-overwrite* do
resto da espinha, e o usuário sempre pode adaptar. *(A função detalhada deles é documentada junto ao scaffolder.)*

---

*Externo: [sincronização Excel do OpenProject](https://www.openproject.org/pt/docs/system-admin-guide/integrations/excel-synchronization/)
(URLs podem mudar de lugar — busque "OpenProject Excel synchronization"). Referências cruzadas:
`05-convencoes-interpop.md` (ids, escala de prioridade, títulos em linguagem de negócio), `04-bdd-criterios-aceitacao.md`
(BDD = o conteúdo da User Story), `10-estrutura-projeto.md` (a espinha `docs/backlog/`),
`../integrations/README.md` (índice de integrações). Adotado aqui como uma ponte **opcional** de rastreamento de backlog — a
fonte de verdade permanece em `docs/backlog/`.*
