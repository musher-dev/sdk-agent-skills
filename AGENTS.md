# sdk-agent-skills: notes for agents and maintainers

@README.md

This repository publishes the `musher` Agent Skill and the Claude Code plugin that carries it. Other agents read every
word of it literally, so an error here becomes their error, made confidently.

## Rules for changing the skill

- **Every fact needs a source you checked.** That covers commands, flags, endpoints, field names, prices, limits and
  Console paths. The sources:
  - the live OpenAPI document, https://api.musher.dev/openapi.json;
  - the CLI's source on the branch its release carries (`musher-dev/musher-cli`);
  - the specifications (https://specifications.musher.dev);
  - the public docs (https://docs.musher.dev);
  - for `references/mcp.md`, the MCP server's own `tools/list` and what a call returned. Don't pin the page to a
    release; state the behaviour, and write "in one run" for anything you saw once.

  Don't copy anything from memory or from another vendor's skill.
- **No prices in the text.** Every rate is a launch rate (`rateStatus: PLACEHOLDER`). The skill tells the agent to
  read the live figure.
- **Link only to public URLs.** The private platform repositories are background only.
- **Keep SKILL.md short.** It stays under 500 lines, with the rules that always apply in the first screen. Detail goes
  in `references/`, one level deep, and SKILL.md names every reference file.
- **One skill.** Split it only when trigger evals show that one description can't cover the work.
- **Never bump the version by hand.** release-please's release pull request raises `version.txt`,
  `plugins/musher/.claude-plugin/plugin.json`, the skill's `metadata.version` and `CHANGELOG.md` together, and merging
  it tags `vX.Y.Z` and publishes the release. Claude Code only updates an installed plugin when its version changes, so
  a skill change reaches Claude Code users when the release pull request merges. Only a `feat` or `fix` commit cuts a
  release; a `docs` commit doesn't, so type a change to what the skill tells agents as one of those. The release
  workflow mints its token from the musher-release App, which needs the `RELEASE_APP_CLIENT_ID` variable and the
  `RELEASE_APP_PRIVATE_KEY` secret on this repository.
- **Refresh the Catalog index** with `task catalog`. Don't edit it by hand.

## Known gaps the skill states, and removes once they're fixed

None today. When the platform has a gap the skill must state, add a row here with where the skill says it and
what removes it:

| Gap | Where the skill says it | Remove when |
| --- | --- | --- |

## Checks

`task check` runs what CI runs:

- `scripts/check_skill.py`: size, links, that the manifests agree, and that `version.txt`, `plugin.json` and the
  skill's `metadata.version` carry one version;
- `scripts/check_mcp_tools.py`: that every MCP tool and toolset the skill names is still on the server, read from
  the public tool reference at https://docs.musher.dev/agents/tools;
- the Agent Skills reference validator;
- the skills CLI's own discovery;
- actionlint and zizmor;
- the pinned conventions release.

`claude plugin validate . --strict` checks the marketplace and the plugin. Run it locally before a release.
