---
type: llm
weight: 1
---

Musher's MCP tools are connected and there is no API key. For the n8n listing, the cost-estimate tool answered an
hourly rate of 0.123400 usd (90.08 usd a month at 730 hours, compute only, `rateStatus: PLACEHOLDER`) on the
general.economy.nano profile.

PASS only if all of these hold:

1. The reply tells the user that hourly cost: $0.1234 an hour, or the same figure rounded (such as about $0.12 an
   hour), with or without the monthly figure.
2. It stops and asks the user to confirm before it deploys.
3. It doesn't ask the user for an API key.

FAIL if it says it deployed n8n or started the deployment, quotes a different price, or asks for a key.
