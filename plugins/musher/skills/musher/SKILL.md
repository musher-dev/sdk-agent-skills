---
name: musher
description: >-
  Deploys and operates apps, containers and self-hosted AI tools on Musher
  (musher.dev): installs Catalog tools such as n8n, Open WebUI, LiteLLM,
  Langfuse, OpenClaw, Hermes Agent and Ollama, runs databases such as Postgres
  and Qdrant, deploys a container image or a Dockerfile, writes and validates blueprints, and checks status,
  logs, cost and failed deploys, through the musher CLI or the Musher HTTP API.
  Use when the user mentions Musher, musher.dev, the musher CLI or a Musher
  blueprint, or wants an always-on host for one of these tools or for their own
  container. Not for running these tools locally or for using them, such as
  writing n8n workflows.
license: MIT
compatibility: >-
  Needs network access to api.musher.dev and a Musher API key in
  MUSHER_API_KEY. Deploying the user's own code also needs the musher CLI with
  the deploy command, Docker or BuildKit, and a container registry to push to.
metadata:
  author: musher-dev
  version: "0.1.0"
  homepage: https://docs.musher.dev/
  openclaw:
    primaryEnv: MUSHER_API_KEY
    requires:
      env:
        - MUSHER_API_KEY
---

# Musher

Musher runs containers and open-source apps as **deployments** with HTTPS URLs, persistent volumes and logs. You can
reach it three ways: the `musher` CLI, the HTTP API at `https://api.musher.dev`, and the Console at
`https://console.musher.dev`, where a person signs in.

## Rules that always apply

1. **Never ask the user to paste an API key into the chat, and never put a key on a command line.** Read it from
   `MUSHER_API_KEY`. If it is unset, tell the user how to create one (below) and stop.
2. **Confirm before anything that bills.** Before a deploy, get the cost estimate (`references/catalog.md`), tell the
   user the hourly figure and the compute profile, and wait for a yes. Every rate is a launch rate that may change, so
   quote the live figure, never one from memory.
3. **Never report success before you see it.** A deploy is done when the deployment's `status.phase` is `ACTIVE` and
   you have its URL. `PROVISIONING` is not done. `FAILED` or `DEGRADED` means read the logs
   (`references/troubleshoot.md`).
4. **Stay non-interactive.** Pass `--json --no-input` to the CLI. Send an `Idempotency-Key` header (a fresh UUID per
   intended action) with every API write, so a retry cannot create a second deployment.
5. **You cannot pay, create keys, or invite people.** Those need a person in the Console. Say exactly what to click,
   then wait.

## Pick the route

| The user wants | Route | Read |
| --- | --- | --- |
| An app from the Catalog (n8n, Open WebUI, LiteLLM, OpenClaw, …) | API `deployments:cloneFromListing` | `references/catalog.md` |
| Their own image (`ghcr.io/…:tag`) | CLI `musher deploy --image`, or the API with a blueprint | `references/deploy-own-app.md` |
| Their own repository or Dockerfile, built and deployed | CLI `musher init` + `musher deploy` | `references/deploy-own-app.md` |
| A multi-service app, or a change to a Catalog app | A blueprint | `references/blueprints.md` |
| Status, logs, restart, rollback, suspend | CLI or API | `references/operate.md` |
| A deploy that failed or a `4xx` error | Read the problem document | `references/troubleshoot.md` |
| Keys, organizations, balance, `402` | — | `references/auth-and-billing.md` |

**Check the CLI before you rely on it.** Run `musher deploy --help`. If the command is missing, the installed CLI is
an older bundle-era release (0.3.x) that cannot deploy. Use the API instead; don't try to upgrade it mid-task.

## Preflight, in this order

1. **Key.** `MUSHER_API_KEY` is set. If it isn't, tell the user: "Create an API key at
   https://console.musher.dev (your organization's **Settings → API Keys → Create API Key**) and set it as
   `MUSHER_API_KEY` in this environment."
   A key is bound to one organization.
2. **Organization.** `GET /v1/organizations` lists the caller's organizations in `data`; take the
   `id` the deploy paths need.
3. **Balance.** Usage is prepaid. A new organization starts at $0, and a deploy it cannot cover returns
   `402 payment-required`. Then tell the user that an Owner or Admin must add funds in the Console: the organization
   selector, **Organization settings → Overview → Add funds** (minimum $10, by card). You cannot do it for them.

```bash
curl -fsS https://api.musher.dev/v1/organizations \
  -H "Authorization: Bearer $MUSHER_API_KEY"
```

## Deploy a Catalog app (the common case)

1. **Find the listing.** If the user named an app, look it up by slug:
   `GET /v1/catalog/listings:bySlug?slug=n8n`. If the name is approximate, search:
   `GET /v1/catalog/listings:search?q=…`. Both are anonymous. Only a `BLUEPRINT` listing deploys on its own; a
   `COMPONENT` listing (Postgres, Redis, pgvector, …) is a part you add to a blueprint.
2. **Price it:** `GET /v1/catalog/listings/{id}/cost-estimate`. This is anonymous and covers compute only. Storage is
   billed separately for as long as a volume exists. Confirm the cost with the user (rule 2).
3. **Read its parameters:**
   `GET /v1/blueprints/{blueprintId}/versions/{blueprintVersion}/deploy-form`, with the ids from the listing.
   Generated credentials are filled in for you. Ask the user only for required fields that have no default.
4. **Deploy:**

```bash
curl -fsS -X POST \
  "https://api.musher.dev/v1/organizations/$ORG_ID/deployments:cloneFromListing" \
  -H "Authorization: Bearer $MUSHER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"listingId": "<listing id>", "name": "team-n8n"}'
```

   `name` is lowercase letters, digits and hyphens, starting with a letter. The response is the deployment, already
   in `PROVISIONING`. A `422` lists every problem in `errors`, and nothing is created.
5. **Wait for it:** poll `GET /v1/deployments/{id}` (the id is `metadata.id`) until `status.phase` is
   `ACTIVE`. Then `GET /v1/organizations/{org}/deployments/{id}/endpoints` lists each endpoint's `publicUrl`. Report the URL and the hourly cost.

**Known limit:** with an API key, `n8n`, `langfuse`, `librechat`, `metabase`, `label-studio` and `sim` can fail with
`ERR_DEPLOYMENT_FACT_UNAVAILABLE`, because they need facts about a signed-in person. If that happens, give the user
the Console route: **Catalog → Blueprints →** the app's card **→ Deploy**, then Configure, Review, Deploy.

## Deploy the user's own container

With an image that already exists, and a CLI that has `deploy`:

```bash
musher deploy api --image ghcr.io/acme/api:v1.4.2 --port 8080 --json --no-input
```

Deploying the same name again updates that deployment in place, keeping its URL. Building from source, private
images and the blueprint route are in `references/deploy-own-app.md`.

## Billing facts to state plainly

- Compute is billed per hour, starting when the deployment first reaches `ACTIVE`. A deploy that is refused, or that
  fails before it first runs, is never billed.
- Storage is billed while a volume exists, even when the deployment is suspended.
- The cost estimate covers compute only. Storage, egress and inference are billed separately.

## When something goes wrong

Every API error is an RFC 9457 problem document (`application/problem+json`) with `type`, `title`, `status`,
`detail` and `traceId`. Quote `detail` to the user. The CLI exits with a specific code, such as 2 for auth, 8 for a
failed deploy, 11 for an invalid spec and 12 for an entitlement problem. See `references/troubleshoot.md`.
