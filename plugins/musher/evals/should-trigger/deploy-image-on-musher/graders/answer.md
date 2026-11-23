---
type: llm
weight: 1
---

The user asked to deploy the image ghcr.io/acme/api:v1.4.2, which listens on port 8080, on Musher. Any route counts:
the musher CLI (`musher deploy … --image … --port 8080`), the Musher HTTP API (a component and a blueprint, each
published, then a deploy), or Musher's MCP tools (`create_component`, `publish_component_version`, `create_blueprint`,
`publish_blueprint_version`, `deploy_blueprint`). Don't fail a reply for its choice of route, or for offering more
than one.

PASS only if all of these hold:

1. It deploys that image, with container port 8080, by one of those routes.
2. It gets the hourly cost and confirms it with the user before the deploy, the step that bills.
3. It reports success only once the deployment is ACTIVE and READY (or ready and healthy) and it has the URL.
4. It stays non-interactive in what it spells out: a musher CLI command carries `--json` and `--no-input`, and an API
   or MCP write carries an idempotency key. Judge only the commands and writes it actually writes out.
5. It never asks the user to paste an API key into the chat.

FAIL if it invents flags, endpoints or tools, claims success without checking the deployment's status, deploys
without mentioning the cost, or asks for a key in the chat.
