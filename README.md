# Musher agent skills

Agent Skills and plugins that teach coding agents (Claude Code, Codex, Cursor, OpenClaw, Hermes Agent and others) to
deploy and operate apps, containers and self-hosted AI tools on [Musher](https://musher.dev).

With the `musher` skill installed, you can ask your agent to "host n8n for my team", "put Open WebUI with Ollama
online" or "deploy this container on Musher". The agent then:

- finds the right app in the Musher Catalog and tells you what it will cost per hour before deploying;
- deploys it through the Musher API or the `musher` CLI;
- waits until the app is healthy, then hands you its HTTPS URL;
- reads logs and status when something goes wrong.

## Install

Any agent that supports [Agent Skills](https://agentskills.io), through the
[skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add musher-dev/sdk-agent-skills
```

Claude Code, as a plugin from this repository's marketplace:

```text
/plugin install musher --marketplace musher-dev/sdk-agent-skills
```

The plugin also adds Musher's MCP server (`https://mcp.musher.dev`). It carries no key: run `/mcp` in Claude Code,
choose the plugin's `musher` server and sign in through your browser. Claude Code names a plugin's tools with the
plugin and server names in front, such as `mcp__plugin_musher_musher__get_deployment`.

## What you need

- **A Musher account.** Sign up at [musher.dev](https://musher.dev).
- **Musher's MCP server, or an API key.** With the server (`https://mcp.musher.dev`) connected, the agent signs in
  through your browser and needs no key; [docs.musher.dev/agents](https://docs.musher.dev/agents) has the steps for
  each agent. The API and the CLI routes need an API key, set as `MUSHER_API_KEY` in the agent's environment.
  Create one at [console.musher.dev](https://console.musher.dev): your organization's **Settings → API Keys**. Don't
  paste it into the chat; the skill tells the agent never to ask for it.
- **A balance.** Usage is prepaid. An Owner or Admin adds funds in the Console under **Organization settings →
  Overview → Add funds**. Compute is billed only from the moment a deployment is healthy, and a deploy that fails
  first is never billed.
- **For deploying your own code:** the `musher` CLI with its `deploy` command, Docker or BuildKit, and a container
  registry to push to.

## What the skill covers

| Task | How the agent does it |
| --- | --- |
| Deploy a Catalog app (n8n, Open WebUI, LiteLLM, Langfuse, OpenClaw, Hermes Agent, Flowise, Qdrant, …) | Musher API |
| Deploy your own container image, or build and deploy a repository | `musher deploy`, or the API |
| Write and validate a blueprint for a multi-service app | The published v2 schemas |
| Status, URLs, logs, restart, roll back, suspend | The API or the CLI |
| Explain a failed deploy, a `402`, or another error | The skill's troubleshooting reference |

The agent stays non-interactive, sends idempotency keys with every write, and asks you before anything that bills.

## Repository layout

| Path | Holds |
| --- | --- |
| `plugins/musher/skills/musher/` | The skill: `SKILL.md` and its `references/` |
| `plugins/musher/.claude-plugin/plugin.json` | The Claude Code plugin |
| `.claude-plugin/marketplace.json` | The marketplace that lists the plugin |
| `skills.sh.json` | Where the skills CLI finds the skill |
| `scripts/` | Repository tooling: the Catalog index generator and the skill checks. Not shipped to agents |

## Developing

```bash
task setup    # install the pinned tools
task check    # every gate CI runs
task catalog  # refresh the skill's Catalog index from the live Catalog
```

See [AGENTS.md](AGENTS.md) for how to keep the skill accurate.

## License

[MIT](LICENSE).
