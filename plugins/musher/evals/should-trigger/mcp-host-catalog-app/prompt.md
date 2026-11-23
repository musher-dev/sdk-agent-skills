---
description: >-
  Musher's MCP tools are mocked and there is no MUSHER_API_KEY. The agent looks up n8n, reads the live estimate,
  quotes its hourly figure and stops for a yes, without calling clone_deployment_from_listing.
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, mcp]
---

Host n8n on Musher for my team.
