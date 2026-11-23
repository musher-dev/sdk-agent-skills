---
type: llm
weight: 1
---

Musher's MCP tools are connected and there is no API key. The tools for components, blueprints, compute profiles and
deploying were available, and the price tool answered 0.234000 usd an hour (170.82 usd a month) for a compute
profile.

PASS only if all of these hold:

1. It works through Musher's tools, as steps it has done or as the steps it will take: a component for
   ghcr.io/acme/api:v1.4.2 with port 8080, published; a blueprint that runs it, published; then the deploy.
2. Before the deploy, it tells the user an hourly cost of $0.234 (or the same figure rounded, such as about $0.23) and
   the compute profile it will run on, and asks for a go-ahead.
3. It doesn't ask the user for an API key, or switch to the CLI or the HTTP API in place of the connected tools.

FAIL if it says the app is deployed, live or provisioning, deploys without a go-ahead, skips the cost, or asks for a
key.
