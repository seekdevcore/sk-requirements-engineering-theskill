# `requirements-engineering-mcp`

MCP server that exposes the [`engenharia-de-requisitos`](../) skill content to **any MCP-compatible client** — Claude Desktop, Cursor, Cline, Continue, Zed, OpenAI Responses API, custom agents — not only to Claude Code where the native Skill format is supported.

> **When to use this server vs. the native Skill**: if you are on **Claude Code**, the native skill (root of this repo) is simpler and zero-overhead. Use this MCP server when you want the same methodology corpus available **outside Claude Code** — IDEs, chat clients, custom LLM apps.

---

## What it exposes

### Resources (read-only documents)

| URI | Content |
|---|---|
| `requirements://skill` | `SKILL.md` — 10-section entry-point map |
| `requirements://reference/{name}` | One of the 15 `references/` docs, scanned recursively (e.g., `01-fundamentos`, `04-bdd-criterios-aceitacao`, `10-estrutura-projeto`, `11-ears`, `13-confiabilidade-seguranca`, `sdd-interop`, `openproject` — the last two under `references/integrations/`) |
| `requirements://example/{name}` | One of the 5 `examples/` files (cases + templates + ready-to-copy Gherkin) |
| `requirements://catalog` | JSON catalog of every available document — useful for enumerating without parsing markdown |

### Tools (executable functions)

| Tool | Purpose |
|---|---|
| `list_references()` | Returns titles + 1-paragraph summaries of every reference |
| `list_examples()` | Returns titles + 1-paragraph summaries of every example |
| `list_hard_rules()` | Returns the 10 *"Interpop"* hard rules (non-negotiable backlog conventions) |
| `validate_user_story(title, bdd?)` | INVEST + naming-convention check; optional BDD structural check |
| `validate_acceptance_criterion(text)` | AC convention check: `[...]` rule, imperative wording, no qualitative adjectives, no technical terms; hints EARS phrasing when relevant |
| `validate_ears(text)` | EARS check (reference 11, optional layer): exactly one `SHALL`/`DEVE`, no weak modals, measurable response, EARS structural keyword present (EN + pt-BR) |
| `check_projection_drift(requirements_dir, projection_dir)` | SDD-interop drift report (reference 12, advisory): compares `docs/requirements` ↔ an OpenSpec/Spec Kit projection by `RF-NN` tag. Findings: missing / duplicated / orphan / `ca_without_scenario` (coarse) / `ears_weakened`. Never blocks (EN + pt-BR) |

---

## Install

### Prerequisite

Python 3.10+ and [`uv`](https://docs.astral.sh/uv/) recommended.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if you don't have uv
```

### Local install (developer mode)

Clone the repo, install dependencies, and the entry point is available as a uv-managed command:

```bash
git clone https://github.com/seekdevcore/sk-requirements-engineering-theskill.git
cd sk-requirements-engineering/mcp-server
uv sync                                  # installs mcp[cli] in .venv
uv run requirements-engineering-mcp      # boots on stdio
```

### From `uvx` (no clone, single command)

Once the package is published to PyPI (planned for v1.5.0):

```bash
uvx requirements-engineering-mcp
```

---

## Wire it into your client

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "engenharia-de-requisitos": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/sk-requirements-engineering/mcp-server",
        "run",
        "requirements-engineering-mcp"
      ]
    }
  }
}
```

Restart Claude Desktop.

### Claude Code (CLI — alternative to the native skill)

```bash
cd sk-requirements-engineering/mcp-server
claude mcp add engenharia-de-requisitos -- uv run requirements-engineering-mcp
```

You can then ask Claude Code:

- *"Use the tool `list_references` to map the methodology corpus."*
- *"Read `requirements://reference/03-especificacao` and propose a backlog hierarchy."*
- *"Validate this User Story using `validate_user_story`: `Listar reservas do usuário`."*

### Cursor / Cline / Continue / Zed

These clients read a workspace `.cursor/mcp.json` (or equivalent). Add an entry pointing to the same command/args block as the Claude Desktop example above.

### OpenAI Responses API (custom apps)

Use the official `openai-mcp` bridge (or LangChain's MCP adapter) to expose this server to GPT-4o/o1/o3. The methodology then becomes consumable from any custom agent.

---

## Why this server exists

The native Claude Code skill format (Markdown files in `~/.claude/skills/`) is the canonical, simplest way to consume this methodology — **when you are on Claude Code**.

This MCP server is the **bridge** for everyone else. It does not duplicate content: it reads the same `references/` and `examples/` files at the root of this repository at runtime. Editing those files updates both the skill (for Claude Code users) and the MCP server (for everyone else) automatically.

---

## Smoke test

```bash
uv run python -c "from requirements_engineering_mcp.server import mcp; print('OK:', mcp.name)"
```

Expected output: `OK: engenharia-de-requisitos`.

---

## License

This MCP server inherits the [CC BY-SA 4.0](../LICENSE) license of the parent skill. Attribution to **Prof. Dr. *"Juliana Dantas Ribeiro Viana de Medeiros"*** (IFPB) — the author of the primary source corpus — must be preserved in any redistribution. See the [parent README About-the-source-instructor section](../README.md#-about-the-source-instructor) for the academic citation format.
