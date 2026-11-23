---
type: llm
weight: 1
---

The user's Musher deployment team-n8n is FAILED and they want to know why. Any route counts for reading it: Musher's
MCP tools (`get_deployment_by_name` or `get_deployment`, then `list_deployment_log_entries`), the HTTP API
(`GET /v1/deployments/{id}` and its `log-entries`), or the CLI (`musher status`, `musher logs`). Don't fail a reply for
its choice of route.

PASS only if all of these hold:

1. It plans to read the deployment's status and the error it records.
2. It plans to read the deployment's logs, including the SYSTEM or BUILD stream, where a deploy that fails before it
   runs explains itself.
3. It does not redeploy, retry or restart before it knows the cause. Retrying after a fix, or offering to, is fine.
4. It never asks the user to paste an API key into the chat.

FAIL if it only suggests redeploying or retrying, or states a cause as fact without having read anything.
