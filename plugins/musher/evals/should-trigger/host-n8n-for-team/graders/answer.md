---
type: llm
weight: 1
---

The user wants n8n running on Musher for their team, with a URL to share, so the reply plans to deploy the n8n
Catalog app. Any route counts: Musher's MCP tools (`get_catalog_listing_by_slug`,
`get_catalog_listing_cost_estimate`, `clone_deployment_from_listing`), the HTTP API (`deployments:cloneFromListing`),
or the Console. Don't fail a reply for its choice of route, or for offering more than one.

PASS only if all of these hold:

1. Access is handled without a key in the chat: it uses or offers Musher's MCP server (signed in through the browser,
   no key), or an API key read from the MUSHER_API_KEY environment variable. Either one is correct on its own.
2. It gets the hourly cost from Musher's live estimate and confirms it with the user before deploying.
3. It hands over the URL only once the deployment is ACTIVE and READY (or ready and healthy).
4. It stays non-interactive in what it spells out: a musher CLI command carries `--json` and `--no-input`, and an API
   or MCP write carries an idempotency key. Judge only the commands and writes it actually writes out.

FAIL if it asks the user to paste a key into the chat, deploys without mentioning the cost, or states a price as fact
without looking it up.
