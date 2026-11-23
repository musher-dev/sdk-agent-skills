# Musher plugin

The `musher` plugin teaches a coding agent to deploy and operate apps, containers and self-hosted AI tools on
[Musher](https://musher.dev). Ask it to "host n8n for my team" or "deploy this container on Musher". It finds the app
in the Musher Catalog, tells you the hourly cost and waits for your yes. It then deploys the app, waits until it is
healthy, and gives you its HTTPS URL. It also reads status and logs when a deploy fails.

## Install

In Claude Code 2.1.275 or later:

```text
/plugin install musher --marketplace musher-dev/sdk-agent-skills
```

On an older Claude Code, run `/plugin marketplace add musher-dev/sdk-agent-skills`, then
`/plugin install musher@musher`. Other agents install the skill with
`npx skills add musher-dev/sdk-agent-skills`; see [docs.musher.dev/agents/skill](https://docs.musher.dev/agents/skill).

## What it contains

- `skills/musher/`: the `musher` Agent Skill, which is instructions and references only. It runs no code of its own.
- `.mcp.json`: Musher's remote MCP server, `https://mcp.musher.dev`, over Streamable HTTP.
- `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`: the manifests for Claude Code and Cursor.

## What it sends, and where

- **Musher's MCP server.** It carries no key. You sign in to `https://mcp.musher.dev` through your browser with OAuth
  (in Claude Code, run `/mcp`). You choose the organization and role it works under. Each tool call goes to Musher
  and acts as you, in that organization.
- **Without the MCP server,** the skill tells the agent to call the Musher API (`https://api.musher.dev`) or the
  `musher` CLI. Both use an API key you set as `MUSHER_API_KEY` in the agent's environment. The skill tells the agent
  never to ask for the key in chat, and never to put it on a command line.
- **Read anonymously:** the agent may look up public Catalog listings and cost estimates at
  [api.musher.dev](https://api.musher.dev). It may also read the published schemas at
  [specifications.musher.dev](https://specifications.musher.dev), and the docs at
  [docs.musher.dev](https://docs.musher.dev).
- **Nothing is sent anywhere else.** The plugin has no hooks, no commands and no telemetry. Anything that bills runs
  only after you confirm the cost.

Musher's privacy policy: [musher.dev/privacy](https://musher.dev/privacy). Source, issues and releases:
[musher-dev/sdk-agent-skills](https://github.com/musher-dev/sdk-agent-skills).

## License

MIT, for the plugin's code and text. The Musher name and logo, including `.claude-plugin/icon.png`, are Musher's own
marks and aren't licensed under it.
