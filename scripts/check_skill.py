#!/usr/bin/env python3
"""Check what the skills validator does not: the skill's size, its links, and that every manifest agrees.

    python3 scripts/check_skill.py

- SKILL.md stays under 500 lines, and its description under 1024 characters.
- Every `references/<file>.md` the skill names exists, and every reference
  file is named by SKILL.md, so none is unreachable.
- The skill's metadata.version equals the plugin's version, and the plugin's
  and marketplace's names agree with the skill's.
- skills.sh.json points at the directory the skill is in.

Standard library only. `uvx skills-ref validate` checks the frontmatter itself.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins/musher"
SKILL_DIR = PLUGIN / "skills/musher"
SKILL = SKILL_DIR / "SKILL.md"


def frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise SystemExit("SKILL.md has no frontmatter")
    return match.group(1)


def folded(block: str, key: str) -> str:
    """The value of a top-level `key: >-` folded scalar, joined as YAML folds it."""
    match = re.search(rf"^{key}: >-\n((?:  .*\n?)+)", block, re.M)
    return " ".join(line.strip() for line in match.group(1).splitlines()) if match else ""


def main() -> int:
    problems: list[str] = []
    text = SKILL.read_text(encoding="utf-8")
    block = frontmatter(text)

    lines = text.count("\n")
    if lines >= 500:
        problems.append(f"SKILL.md is {lines} lines; keep it under 500 and move detail into references/")

    description = folded(block, "description")
    if not description:
        problems.append("SKILL.md's description is missing or is not a `>-` folded scalar")
    elif len(description) > 1024:
        problems.append(f"the description is {len(description)} characters; the limit is 1024")

    named = set(re.findall(r"references/([a-z0-9-]+\.md)", text))
    present = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    problems += [f"SKILL.md names references/{name}, which does not exist" for name in sorted(named - present)]
    problems += [f"references/{name} is never named in SKILL.md" for name in sorted(present - named)]

    for path in (SKILL_DIR / "references").glob("*.md"):
        for name in re.findall(r"`([a-z0-9-]+\.md)`", path.read_text(encoding="utf-8")):
            if name != "SKILL.md" and name not in present:
                problems.append(f"references/{path.name} names {name}, which does not exist")

    version = re.search(r'^\s+version: "([^"]+)"$', block, re.M)
    plugin = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    if not version or version.group(1) != plugin.get("version"):
        problems.append("the skill's metadata.version and plugins/musher/.claude-plugin/plugin.json's version differ")
    if [entry["name"] for entry in marketplace["plugins"]] != [plugin["name"]]:
        problems.append("the marketplace does not list exactly the plugin in plugins/musher")

    paths = json.loads((ROOT / "skills.sh.json").read_text(encoding="utf-8")).get("paths", [])
    if "./plugins/musher/skills" not in paths:
        problems.append("skills.sh.json does not point at ./plugins/musher/skills")

    for problem in problems:
        print(f"check_skill: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
