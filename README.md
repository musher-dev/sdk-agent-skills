# Musher agent skills

Agent Skills and plugins that teach coding agents (Claude Code, Codex, Cursor, OpenClaw, Hermes Agent and others) to
deploy and operate apps, containers and self-hosted AI tools on [Musher](https://musher.dev).

Dependencies: [![engineering-conventions](https://github.com/musher-dev/sdk-agent-skills/raw/badges/engineering-conventions.svg)](https://github.com/musher-dev/sdk-agent-skills/tree/badges)

With the `musher` skill installed, you can ask your agent to "host n8n for my team", "put Open WebUI with Ollama
online" or "deploy this container on Musher". The agent then:

- finds the right app in the Musher Catalog and tells you what it will cost per hour before deploying;
- deploys it through Musher's MCP tools when they're connected, or else through the Musher API or the `musher` CLI;
- waits until the app is healthy, then hands you its HTTPS URL;
- reads logs and status when something goes wrong.

## Install

Any agent that supports [Agent Skills](https://agentskills.io), through the
[skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add musher-dev/sdk-agent-skills
```

Add `-g` to install it for your user rather than the current project, and `-a <agent>` (such as `-a codex` or
`-a cursor`) to choose the agent instead of letting the CLI detect it.

Claude Code 2.1.275 or later, as a plugin from this repository's marketplace:

```text
/plugin install musher --marketplace musher-dev/sdk-agent-skills
```

On an older Claude Code, add the marketplace first, then install the plugin from it:

```text
/plugin marketplace add musher-dev/sdk-agent-skills
/plugin install musher@musher
```

The plugin also adds Musher's MCP server (`https://mcp.musher.dev`). It carries no key: run `/mcp` in Claude Code,
choose the plugin's `musher` server and sign in through your browser. Claude Code names a plugin's tools with the
plugin and server names in front, such as `mcp__plugin_musher_musher__get_deployment`.

Claude Code doesn't update a plugin from a third-party marketplace on its own. Run `claude plugin update
musher@musher`, choose **Update now** on the plugin in `/plugin`, or turn on auto-update for the `musher` marketplace
in `/plugin`.

Every other agent, including Codex, Cursor, VS Code with Copilot, Gemini CLI, OpenCode, Devin, Pi, OpenClaw and
Hermes Agent, has its own install and sign-in steps at
[docs.musher.dev/agents/skill](https://docs.musher.dev/agents/skill).

## Try it

Start with a check that costs nothing but proves your agent can reach your organization:

> Check that you can reach my Musher organization: list my deployments, and tell me what n8n would cost per hour.
> Don't deploy anything.

Then deploy something:

> Host Open WebUI with Ollama on Musher for my team and give me the URL once it's healthy.

The agent looks the app up in the Catalog, tells you its hourly cost and waits for your yes. It then deploys the app,
waits until the deployment is `ACTIVE` and `READY`, and gives you its HTTPS URL. A new organization starts with a
balance of $0, so add funds first (below).

## What you need

- **A Musher account.** Sign up at [musher.dev](https://musher.dev).
- **Musher's MCP server, or an API key.** With the server (`https://mcp.musher.dev`) connected, the agent signs in
  through your browser and needs no key; [docs.musher.dev/agents](https://docs.musher.dev/agents) has the steps for
  each agent. The API and the CLI routes need an API key, set as `MUSHER_API_KEY` in the agent's environment.
  An Owner or Admin creates one at [console.musher.dev](https://console.musher.dev), under **Organization settings →
  API keys**, with **API** as its use. Don't paste it into the chat; the skill tells the agent never to ask for it.
- **A balance.** Usage is prepaid. An Owner or Admin adds funds in the Console under **Organization settings →
  Overview → Add funds**. Compute is billed only from the moment a deployment is healthy, and a deploy that fails
  first is never billed.
- **For building and deploying your own code with the CLI:** the `musher` CLI 0.4.1 or later
  ([install it](https://docs.musher.dev/guides/deploy/install-the-cli)), Docker or BuildKit, and a container registry
  to push to. An image that is already pushed also deploys through the MCP tools or the API.

## What the skill covers

| Task | How the agent does it |
| --- | --- |
| Deploy a Catalog app (n8n, Open WebUI, LiteLLM, Langfuse, OpenClaw, Hermes Agent, Flowise, Qdrant, …) | The MCP tools, or the API |
| Deploy your own container image | The MCP tools, `musher deploy --image`, or the API |
| Build and deploy a repository | `musher deploy` |
| Write and validate a blueprint for a multi-service app | The published v2 schemas, and the MCP tools' or the API's validation |
| Status, URLs, logs, restart, roll back, suspend | The MCP tools, the API or the CLI |
| Explain a failed deploy, a `402`, or another error | The skill's troubleshooting reference |

When the MCP tools are connected the agent uses them first and needs no key. It stays non-interactive, sends
idempotency keys with every write, and asks you before anything that bills.

## Repository layout

| Path | Holds |
| --- | --- |
| `plugins/musher/skills/musher/` | The skill: `SKILL.md` and its `references/` |
| `plugins/musher/.claude-plugin/plugin.json` | The Claude Code plugin |
| `plugins/musher/.mcp.json` | Musher's MCP server, which the plugin adds |
| `plugins/musher/evals/` | Trigger and behaviour evals for `claude plugin eval`, with mocked MCP tools |
| `plugins/musher/.cursor-plugin/plugin.json` | The same plugin, for Cursor |
| `plugins/musher/README.md` | The plugin's own README: what it contains, and what it sends and where |
| `.claude-plugin/marketplace.json` | The marketplace that lists the plugin |
| `.cursor-plugin/marketplace.json` | The same marketplace, for Cursor and cursor.directory |
| `skills.sh.json` | Where the skills CLI finds the skill |
| `.github/release-please/`, `version.txt` | The release configuration and the current version |
| `scripts/` | Repository tooling: the Catalog index generator and the skill checks. Not shipped to agents |

`SKILL.md` stays short, with the rules that always apply in its first screen. Detail lives in `references/`, which an
agent reads only when the task needs it.

## Developing

```bash
task setup    # install the pinned tools
task check    # every gate CI runs
task catalog  # refresh the skill's Catalog index from the live Catalog
```

See [AGENTS.md](AGENTS.md) for how to keep the skill accurate.

Releases are cut by release-please. Merging a change to `main` updates its release pull request. Merging that pull
request raises the version in `version.txt`, `plugin.json` and `SKILL.md`, writes `CHANGELOG.md`, and tags and
publishes `vX.Y.Z`.

## License

[MIT](LICENSE), for this repository's code and text. The Musher name and logo, including the plugin icon
(`plugins/musher/.claude-plugin/icon.png`), are Musher's own marks and aren't licensed under it.
