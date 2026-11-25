#!/usr/bin/env python3
"""Check that every MCP tool and toolset the skill names still exists on Musher's MCP server.

    python3 scripts/check_mcp_tools.py

The source is the public tool reference, https://docs.musher.dev/agents/tools,
which is built from the server's tool list: one page per toolset, one section
per tool. The private contract (platform-api's contracts/mcp/tools.json) holds
the same names, but CI can't read it.

- A backticked snake_case name in SKILL.md or references/ is taken as a tool
  name when it starts with a verb some live tool starts with (`get_`, `list_`,
  `deploy_`, ...). Each must be a live tool. Field names such as `blueprint_id`
  start with no tool verb and are skipped.
- Every toolset slug listed in references/mcp.md's Toolsets section must be a
  live toolset, and every live toolset must be listed there.
- The evals' mocks of the server (`plugins/musher/evals/**/mocks/musher/`)
  stand in for live tools: each `<tool>.md` mock, each tool `_tools.json`
  describes, and each `mcp__plugin_musher_musher__<tool>` a grader names must
  be a live tool, and every mock must have its description in `_tools.json`.
  A renamed tool would otherwise leave a case testing a tool that is gone.

Standard library only. It needs network access to docs.musher.dev.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "plugins/musher/skills/musher"
EVALS = ROOT / "plugins/musher/evals"
# How Claude Code names the tools of the server the plugin's .mcp.json calls `musher`.
PREFIX = "mcp__plugin_musher_musher__"
DOCS = "https://docs.musher.dev"


def fetch(path: str) -> str:
    request = urllib.request.Request(DOCS + path, headers={"User-Agent": "sdk-agent-skills-check"})
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 (a fixed https URL)
        return response.read().decode("utf-8")


def live() -> tuple[set[str], set[str]]:
    """The toolset slugs and tool names the public tool reference lists."""
    toolsets = set(re.findall(r'href="/agents/tools/([a-z0-9-]+)"', fetch("/agents/tools")))
    tools: set[str] = set()
    for slug in sorted(toolsets):
        page = fetch(f"/agents/tools/{slug}")
        found = set(re.findall(r'data-testid="mcp-tool"[^>]*>\s*<h2 id="([a-z0-9_]+)"', page))
        if not found:
            raise SystemExit(f"check_mcp_tools: found no tools on {DOCS}/agents/tools/{slug}; has the page changed?")
        tools |= found
    return toolsets, tools


def eval_problems(tools: set[str]) -> list[str]:
    """Every tool the evals mock, describe or grade must be a live tool."""
    problems: list[str] = []
    for mocks in sorted(EVALS.glob("**/mocks/musher")):
        where = mocks.relative_to(ROOT)
        mocked = {path.stem for path in mocks.glob("*.md") if not path.name.startswith("_")}
        problems += [f"{where}/{name}.md mocks `{name}`, which the MCP server no longer has"
                     for name in sorted(mocked - tools)]
        described_file = mocks / "_tools.json"
        if not described_file.exists():
            continue
        described = {tool["name"] for tool in json.loads(described_file.read_text(encoding="utf-8"))["tools"]}
        problems += [f"{where}/_tools.json describes `{name}`, which the MCP server no longer has"
                     for name in sorted(described - tools)]
        problems += [f"{where}/_tools.json has no description of the mocked `{name}`"
                     for name in sorted(mocked - described)]
    for grader in sorted(EVALS.glob("**/graders/*.md")):
        for name in sorted(set(re.findall(rf"{PREFIX}([a-z0-9_]+)", grader.read_text(encoding="utf-8")))):
            if name not in tools:
                problems.append(f"{grader.relative_to(ROOT)} grades `{name}`, which the MCP server no longer has")
    return problems


def main() -> int:
    toolsets, tools = live()
    if len(toolsets) < 10 or len(tools) < 100:
        print(f"check_mcp_tools: read {len(toolsets)} toolsets and {len(tools)} tools; has the reference changed?",
              file=sys.stderr)
        return 1

    verbs = {name.split("_", 1)[0] for name in tools}
    problems: list[str] = []
    for path in sorted([SKILL_DIR / "SKILL.md", *(SKILL_DIR / "references").glob("*.md")]):
        text = path.read_text(encoding="utf-8")
        for name in sorted(set(re.findall(r"`([a-z]+(?:_[a-z0-9]+)+)`", text))):
            if name.split("_", 1)[0] in verbs and name not in tools:
                problems.append(f"{path.relative_to(ROOT)} names `{name}`, which the MCP server no longer has")

    mcp = (SKILL_DIR / "references/mcp.md").read_text(encoding="utf-8")
    section = re.search(r"^## Toolsets\n(.*?)^## ", mcp, re.S | re.M)
    if not section:
        problems.append("references/mcp.md has no Toolsets section")
    else:
        listed = set(re.findall(r"`([a-z0-9-]+)`", section.group(1).split("\n\n")[1]))
        problems += [f"references/mcp.md lists toolset `{slug}`, which the server no longer has"
                     for slug in sorted(listed - toolsets)]
        problems += [f"references/mcp.md's Toolsets section is missing `{slug}`" for slug in sorted(toolsets - listed)]

    problems += eval_problems(tools)

    for problem in problems:
        print(f"check_mcp_tools: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
