---
description: >-
  Musher's MCP tools are mocked and there is no MUSHER_API_KEY. The agent builds or lays out component, publish,
  blueprint, publish, then quotes the profile's hourly price and stops for a yes, without calling deploy_blueprint.
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, mcp]
---

Deploy ghcr.io/acme/api:v1.4.2 on Musher. It listens on port 8080.
