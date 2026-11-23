#!/usr/bin/env python3
"""Check what the skills validator does not: the skill's size, its links, and that every manifest agrees.

    python3 scripts/check_skill.py

- SKILL.md stays under 500 lines, and its description under 1024 characters.
- Every `references/<file>.md` the skill names exists, and every reference
  file is named by SKILL.md, so none is unreachable.
- The skill's metadata.version equals the plugin's version, and the plugin's
  and marketplace's names agree with the skill's.
- skills.sh.json points at the directory the skill is in.
- A reference over 100 lines opens with a `## Contents` list that links every
  other `##` section, so a model that stops partway knows what the rest holds.
- The skill, its references and its eval graders state no dollar amount in
  prose (AGENTS.md: no prices in the text). The skill tells the agent where to
  read the live figure.
- Every `metadata` value is a string, as the Agent Skills specification
  defines it: one `key: value` line, with no nested mapping or list, and no
  value YAML would read as a number, a boolean or null.

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


def metadata_problems(block: str) -> list[str]:
    """Every `metadata` entry that is not a string, as the specification requires."""
    match = re.search(r"^metadata:[ \t]*(.*)\n((?:[ \t]+.*\n?)*)", block, re.M)
    if not match:
        return []
    if match.group(1).strip():
        return ["metadata is written inline; give each key its own `key: value` line with a string value"]
    problems = []
    for line in match.group(2).splitlines():
        entry = re.match(r"^  ([A-Za-z0-9_.-]+):[ \t]*(.*)$", line)
        if not entry:
            problems.append(f"metadata holds a nested value ({line.strip()!r}); every value must be a string")
            continue
        key, value = entry.groups()
        if not value or value[0] in "{[|>&*":
            problems.append(f"metadata.{key} is not a one-line string")
        elif value[0] not in "'\"" and re.fullmatch(
            r"[-+]?(\d[\d_]*(\.\d*)?([eE][-+]?\d+)?|\.\d+|0x[0-9a-fA-F]+|\.inf|\.nan)"
            r"|true|false|yes|no|on|off|null|~",
            value,
            re.I,
        ):
            problems.append(f"metadata.{key} reads as a {value!r} that is not a string; quote it")
    return problems


def slug(heading: str) -> str:
    """The anchor GitHub gives a heading."""
    return re.sub(r"[^a-z0-9 _-]", "", heading.strip().lower()).replace(" ", "-")


def contents_problems(path: Path) -> list[str]:
    """A long reference must list each of its sections in a Contents block."""
    text = path.read_text(encoding="utf-8")
    if text.count("\n") <= 100:
        return []
    headings = re.findall(r"^## (.+)$", text, re.M)
    if "Contents" not in headings:
        return [f"references/{path.name} is over 100 lines and has no `## Contents` list"]
    linked = set(re.findall(r"\]\(#([a-z0-9_-]+)\)", text))
    return [
        f"references/{path.name}'s Contents list doesn't link `## {heading}`"
        for heading in headings
        if heading != "Contents" and slug(heading) not in linked
    ]


#: A dollar sign followed by a digit, outside code: a typed amount.
_AMOUNT = re.compile(r"\$\d")
_INLINE_CODE = re.compile(r"`[^`]*`")


def amount_problems(path: Path) -> list[str]:
    """Prose states no dollar amount; a shell `$1` inside code is not one."""
    problems = []
    fenced = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced and _AMOUNT.search(_INLINE_CODE.sub("", line)):
            problems.append(
                f"{path.relative_to(ROOT)}:{number} states a dollar amount; say where the live figure is read"
            )
    return problems


def main() -> int:
    problems: list[str] = []
    text = SKILL.read_text(encoding="utf-8")
    block = frontmatter(text)

    lines = text.count("\n")
    if lines >= 500:
        problems.append(f"SKILL.md is {lines} lines; keep it under 500 and move detail into references/")

    problems += metadata_problems(block)

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

    for path in sorted((SKILL_DIR / "references").glob("*.md")):
        problems += contents_problems(path)

    prose = [SKILL, *sorted((SKILL_DIR / "references").glob("*.md")), *sorted((PLUGIN / "evals").rglob("*.md"))]
    for path in prose:
        problems += amount_problems(path)

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
