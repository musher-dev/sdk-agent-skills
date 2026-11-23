---
description: >-
  Musher's MCP tools are mocked. team-n8n is FAILED with IMAGE_PULL_FAILED, and only its SYSTEM log lines say why: the
  private image was pulled without a registry credential. The agent reads them and doesn't redeploy, retry or restart.
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, mcp]
---

My Musher deployment team-n8n went FAILED, why?
