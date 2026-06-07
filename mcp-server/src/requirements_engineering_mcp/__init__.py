"""MCP server exposing the engenharia-de-requisitos skill content.

Wraps the static `references/`, `examples/`, and `SKILL.md` corpus as MCP
Resources (read-only documents) and Tools (small validators) so the
methodology is reachable from any MCP-compatible client — Claude Desktop,
Cursor, Cline, Continue, Zed, OpenAI's Responses API, etc. — not only from
Claude Code where the Skill format is native.
"""

__version__ = "0.1.0"
