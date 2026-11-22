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
  - for `references/mcp.md`, the MCP server's own `tools/list` and what a call returned. Say which release you
    observed, and write "in one run" for anything you saw once.

  Don't copy anything from memory or from another vendor's skill.
- **No prices in the text.** Every rate is a launch rate (`rateStatus: PLACEHOLDER`). The skill tells the agent to
  read the live figure.
- **Link only to public URLs.** The private platform repositories are background only.
- **Keep SKILL.md short.** It stays under 500 lines, with the rules that always apply in the first screen. Detail goes
  in `references/`, one level deep, and SKILL.md names every reference file.
- **One skill.** Split it only when trigger evals show that one description can't cover the work.
- **Bump the version in both places, in the same change:** the skill's `metadata.version` and
  `plugins/musher/.claude-plugin/plugin.json`. Claude Code only updates an installed plugin when its version changes.
- **Refresh the Catalog index** with `task catalog`. Don't edit it by hand.

## Known gaps the skill states, and removes once they're fixed

| Gap | Where the skill says it | Remove when |
| --- | --- | --- |
| No released CLI has `deploy`: 0.3.x is bundle-era (musher-cli #96) | SKILL.md, `deploy-own-app.md`, `troubleshoot.md` | A release with `deploy` ships, and the installer works |
| API keys can't deploy n8n, Langfuse, LibreChat, Metabase, Label Studio and Sim (platform-api #1434) | SKILL.md, `catalog.md`, `troubleshoot.md` | #1434 is fixed |

## Checks

`task check` runs what CI runs:

- `scripts/check_skill.py`: size, links, and that the manifests agree;
- the Agent Skills reference validator;
- the skills CLI's own discovery;
- actionlint and zizmor;
- the pinned conventions release.

`claude plugin validate . --strict` checks the marketplace and the plugin. Run it locally before a release.
