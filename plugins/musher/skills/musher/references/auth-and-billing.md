# Keys, organizations and billing

## The API key

- A person creates it at https://console.musher.dev: the organization's **Settings → API Keys → Create API Key**.
  The key carries the permissions of the role chosen for it, and it is shown only once. An agent can't create or
  reveal keys.
- Keys look like `mush_…`, and each one is bound to one organization.
- A key is made for one use, the API or the MCP server, and the other refuses it. The API answers an MCP key `401`
  with "API key is not valid for this API surface". Both kinds start with `mush_`, so the prefix does not tell
  them apart.
- **The key goes in the environment, never in the chat or on a command line.** Read it from `MUSHER_API_KEY`. Send
  it as `Authorization: Bearer <key>` on curl's standard input, so it never appears in curl's arguments, where
  other local processes can read it: `printf 'Authorization: Bearer %s\n' "$MUSHER_API_KEY" | curl -H @- …`.
  `printf` is a shell builtin, so it starts no process of its own.
- **CLI precedence:** `--api-key`, then `MUSHER_API_KEY`, then the OS keyring, then the credentials file. Use the
  environment variable rather than `--api-key`: a flag ends up in shell history and process lists.
- **Check the key:** `musher auth status --json`, or `GET /v1/organizations`. A `401` means the key is wrong or
  revoked.

What to tell a user who has no key:

> Create an API key at https://console.musher.dev (your organization's Settings → API Keys → Create API Key), then set
> it in this environment as `MUSHER_API_KEY` (for example, `export MUSHER_API_KEY=…` in your shell, not in this chat). Tell me when it's set.

## The organization

`GET /v1/organizations` lists the organizations the caller belongs to under `data`. The deploy paths take the
organization's `id`.

## Billing

- **Usage is prepaid.** A new organization starts with no balance. Musher may grant promotional credits, which
  are spent first.
- **A deploy the balance can't cover is refused with `402 payment-required`, and nothing is created.** Only an Owner
  or Admin can add funds, in the Console: open the organization selector, then **Organization settings → Overview →
  Add funds**. The dialog states the minimum top-up, and payment is by card. Auto-recharge can be turned on in the
  same dialog. An agent can't pay.
- **Compute** is billed per hour per replica. Billing starts when the deployment first reaches `ACTIVE`, and covers
  only the hours it runs. A refused deploy creates nothing, and a deployment that fails before it first runs is never
  billed.
- **Storage** is billed while a volume exists, including while the deployment is suspended.
- **Estimates**, all anonymous:
  - `GET /v1/catalog/listings/{id}/cost-estimate` for a Catalog app: `hourlyRate`, `estimatedMonthlyRate`, and
    `rateStatus`, which is `PLACEHOLDER` while the rates are launch figures that may still change. Say so when you
    quote one.
  - `GET /v1/reference/compute-profiles` lists every profile (`computeProfiles`, with vCPU and memory; the
    recommended one has `isRecommended`).
  - `GET /v1/reference/compute-profiles/{slug}/pricing` gives one profile's `effectiveHourlyRate`.
- **Balance:** `GET /v1/organizations/{org}/balance`.

Pricing page: https://musher.dev/pricing.
