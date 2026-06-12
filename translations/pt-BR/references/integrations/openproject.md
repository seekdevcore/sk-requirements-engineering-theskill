# OpenProject — sincronização backlog → Excel (integração opcional)

> **Quando usar esta referência**: quando o time rastreia o backlog no **OpenProject** e quer que a espinha
> `docs/backlog/` desta skill o *alimente* através da **[sincronização Excel do OpenProject](https://www.openproject.org/pt/docs/system-admin-guide/integrations/excel-synchronization/)**
> (um template `.xlsm` fornecido pelo OpenProject que envia/recebe work packages via API). Esta skill é dona da
> **qualidade do item de backlog** (títulos em linguagem de negócio, prioridade, rastreabilidade); o OpenProject é dono do
> **rastreamento do work package** (boards, sprints, responsáveis). Este arquivo é a ponte. **Opcional** — pule se o
> projeto não usar OpenProject.

> **Apenas `docs/backlog/` é projetado.** O lado `docs/requirements/` (`RF`/`RNF`) é o *porquê* — **não** é
> um work package e **não** é exportado. Os work packages são o backlog: **Epics → Features → User Stories**
> (e, opcionalmente, Tasks). A fonte de verdade permanece em `docs/backlog/`; o projeto no OpenProject é uma *projeção*.

---

## 1. O padrão de colunas (o default da skill — adaptável)

A tabela exportada tem exatamente **quatro colunas**, nomeadas como o OpenProject as mostra na tabela de work packages:

| Column | O que carrega | Regra |
|---|---|---|
| **Type** | o tipo do work package | `Epic` · `Feature` · `User story` · `Task` (combine com os nomes de tipo configurados no seu OpenProject) |
| **ID** | o id numérico próprio do OpenProject | **deixado em branco** na exportação — o OpenProject **atribui** na importação (o id dele ≠ o nosso) |
| **Subject** | o título legível | **`<nosso-id> <título em linguagem de negócio>`** — ex.: `EP-10 Gestão de Salas (Admin)`, `F-26 Aprovação de reserva`, `US25.2 Recursos de Filtragem…` |
| **Priority** | a prioridade do work package | a escala *"Interpop"* mapeada para o OpenProject: 🔴 → `Immediate` · 🟠 → `High` · 🟡 → `Normal` · 🟢 → `Low` |

> **Por que nosso id mora no Subject, e não na coluna ID** — o `ID` do OpenProject é atribuído automaticamente e é *dele*
> (um número diferente do nosso `EP-NN`/`F-NN`/`USNN.M`). Colocar nosso id estável no **início do Subject**
> mantém a rastreabilidade visível dentro do OpenProject (e sobrevive à reimportação), exatamente como a UI do OpenProject
> renderiza. A coluna `ID` fica em branco para que o OpenProject crie + numere o work package.

> **Hierarquia**: as quatro colunas acima são o default da skill (é o que o usuário especificou, e o que a
> tabela de work packages não-Enterprise mostra). A exportação emite linhas em **ordem hierárquica** (cada Epic, depois suas
> Features, depois suas User Stories); defina o relacionamento de **parent** do OpenProject após a importação, ou adicione uma coluna `Parent`
> se o seu template Excel do OpenProject usar uma. A coluna "relations" é um add-on Enterprise.

---

## 2. O adaptador (gerar a tabela)

```bash
# dry-run (imprime a tabela de work packages, não escreve nada)
python3 assets/integrations/project-to-openproject.py

# escreve (CSV sempre; XLSX também quando openpyxl está instalado)
python3 assets/integrations/project-to-openproject.py --apply
python3 assets/integrations/project-to-openproject.py --with-tasks --apply   # também emite T/TX como Tasks
```

- Lê `docs/backlog/epics/*.md` (→ `Epic`) e `docs/backlog/features/*.md` (→ `Feature` + os cabeçalhos `User story`
  internos; `Task` apenas com `--with-tasks`).
- Escreve `openproject/openproject-backlog.csv` (stdlib, sempre) e `openproject/openproject-backlog.xlsx`
  (apenas se `openpyxl` estiver disponível — `uv add openpyxl` / `pip install openpyxl`; somente CSV caso contrário).
- **Dry-run por padrão**, `--apply` para escrever, **nunca sobrescreve** um arquivo existente (espírito `set`-strict).
- O título é tirado do cabeçalho `# <id> — <título>`; a prioridade do emoji do item (🔴🟠🟡🟢) ou de uma
  linha `Prioridade`/`Priority`; prioridade ausente assume `Normal` por padrão.

---

## 3. A receita de sincronização Excel

1. No OpenProject, abra a visão de work packages do seu projeto → **baixe o template de sincronização Excel**
   (`.xlsm`) conforme a [documentação do OpenProject](https://www.openproject.org/pt/docs/system-admin-guide/integrations/excel-synchronization/).
2. Rode o adaptador (`--apply`) → abra `openproject/openproject-backlog.xlsx` (ou `.csv`).
3. **Cole as linhas** (`Type` · `ID` · `Subject` · `Priority`) no template de sincronização (deixe a coluna `ID`
   vazia para novos work packages — o OpenProject a preenche no primeiro push).
4. Faça o push pelo template → o OpenProject cria os Epics/Features/User Stories e atribui seus ids numéricos.
5. Em execuções posteriores, os ids do OpenProject voltam no template; reconcilie títulos/prioridade e refaça o push.

> **Regra de round-trip** (mesmo espírito da ponte SDD, `references/integrations/sdd-interop.md`): a fonte de verdade do
> backlog permanece em `docs/backlog/`. Quando algo muda no OpenProject durante a execução, reconcilie-o
> de volta nos arquivos do backlog primeiro, depois reexporte. Nunca deixe a cópia do OpenProject divergir silenciosamente — o
> prefixo `<nosso-id>` no Subject é o que permite casar um work package de volta com seu arquivo `docs/backlog/`.

---

## 4. Os dois Epics raiz obrigatórios (default da skill)

A hierarquia de backlog padrão da skill (do curso *"IFPB"*) sempre termina com **dois Epics raiz obrigatórios**,
irmãos dos Epics feature-front do projeto:

- **`Improvements`** (pt-BR *"Melhorias"*)
- **`Complementary Activities`** (pt-BR *"Atividades complementares"*)

Eles são gerados pelo scaffolder com a mesma lógica idempotente *create-if-missing / never-overwrite* do
resto da espinha, e o usuário sempre pode adaptar. *(A função detalhada deles é documentada junto ao scaffolder.)*

---

*Externo: [sincronização Excel do OpenProject](https://www.openproject.org/pt/docs/system-admin-guide/integrations/excel-synchronization/)
(repos/URLs podem mudar de lugar — busque "OpenProject Excel synchronization"). Referências cruzadas:
`05-convencoes-interpop.md` (ids, escala de prioridade, títulos em linguagem de negócio), `10-estrutura-projeto.md` (a
espinha `docs/backlog/`), `../integrations/README.md` (índice de integrações). Adotado aqui como uma ponte **opcional**
de rastreamento de backlog — a fonte de verdade permanece em `docs/backlog/`.*
