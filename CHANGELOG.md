# Changelog

## [0.3.2](https://github.com/musher-dev/sdk-agent-skills/compare/v0.3.1...v0.3.2) (2026-11-23)


### Features

* **plugin:** add the listing icon, a Cursor manifest and the plugin README ([#18](https://github.com/musher-dev/sdk-agent-skills/issues/18)) ([5bc74f2](https://github.com/musher-dev/sdk-agent-skills/commit/5bc74f23089e898f43483c6dbf48dc6697dca69a))

## [0.3.1](https://github.com/musher-dev/sdk-agent-skills/compare/v0.3.0...v0.3.1) (2026-11-23)


### Features

* **skill:** route Catalog deploys through MCP and close the backlog ([#15](https://github.com/musher-dev/sdk-agent-skills/issues/15)) ([9a9539a](https://github.com/musher-dev/sdk-agent-skills/commit/9a9539ae63ebaed4475a7f9ded6445543a5d29fb))

## 0.3.0 (2026-11-23)

- MCP first. A session with Musher's MCP tools uses them and needs no `MUSHER_API_KEY`; the key is for the API and
  CLI routes. With neither, the skill offers both, and `references/mcp.md` tells the user how to connect the server
  (`https://mcp.musher.dev`, OAuth in the browser).
- The Claude Code plugin bundles `.mcp.json`, so installing it also adds the server. The person signs in with `/mcp`.
- OpenClaw no longer hides the skill without a key: the `metadata.openclaw` block, whose `requires.env` gated it, is
  gone, and every `metadata` value is a string.
- `musher deploy` shipped in CLI 0.4.0. The skill asks for 0.4.1 or later, tells the user how to upgrade, and drops
  the advice to build the CLI from `main`.
- `references/mcp.md` drops its release pin and single-run figures, adds the toolsets, and says tool names may carry a
  client prefix. `scripts/check_mcp_tools.py` fails when the skill names a tool the server no longer has.
- `blueprints.md` has a Contents list, and every reference over 100 lines must have one.
- The curl examples send the key on standard input, so it never reaches a process list.

## 0.2.0 (not tagged; shipped in 0.3.0)

- `references/mcp.md`: the route for a session that has Musher's MCP tools. It gives the order that deploys your own
  image, how to read a validation answer and a placement that waits for a host, what an update does to a running
  app, sign-in on an endpoint, a language model with no outside key, and a list of gotchas.
- A component and blueprint pair the API accepts, with components named by id and revision.
- Corrections: the component is published before the blueprint; `publicUrl` is a bare hostname; a deploy is done at
  `ACTIVE` and `READY`; `allowedActions` covers five actions; log severity is the stream; an MCP key is not an API
  key.

## 0.1.0 (not tagged; shipped in 0.3.0)

- The `musher` skill. It deploys Catalog apps through the Musher API, deploys an image or a repository with
  `musher deploy`, writes v2 blueprints against the published schemas, operates deployments (status, URLs, logs,
  restart, rollback, suspend) and explains failures.
- The `musher` Claude Code plugin, and the marketplace that lists it.
