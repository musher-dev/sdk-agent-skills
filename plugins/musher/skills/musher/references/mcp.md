# Working through Musher's MCP tools

Use this page when the session already has Musher's MCP server connected: tools named `create_component`,
`deploy_blueprint`, `get_deployment` and so on. If the session has no such tools, use the API or the CLI; don't try
to connect the server yourself.

Everything here was observed on release 27.0.1 of the server (231 tools). The server changes. Where a tool's own
description disagrees with this page, believe the tool.

## Contents

- [What the server is](#what-the-server-is)
- [Deploy your own image, in order](#deploy-your-own-image-in-order)
- [Read a validation answer](#read-a-validation-answer)
- [Choose a compute profile that places](#choose-a-compute-profile-that-places)
- [Updates roll every node](#updates-roll-every-node)
- [Parameters and the deploy form](#parameters-and-the-deploy-form)
- [Sign-in on an endpoint](#sign-in-on-an-endpoint)
- [A language model without a key](#a-language-model-without-a-key)
- [Gotchas](#gotchas)

## What the server is

- Every tool acts as the person who connected it, in one organization, and a write runs the moment you call it. Rule 2
  in SKILL.md still applies: confirm before anything that bills.
- An **MCP key is not an API key**, though both start with `mush_`. The MCP server answers an API key
  `401 invalid_token`, exactly as it answers a wrong key. The API answers an MCP key `401` with the detail "API key is
  not valid for this API surface". A person chooses the use, API or MCP, when they create the key in the Console.
- `tools/list` is paged, 100 tools a page, with `nextCursor`. A few tools are marked to load first; a client with no
  tool search has to read every page to see the rest.
- A refused call comes back as the tool's result with `isError: true`. The text is the problem's `detail`, and the
  whole problem document (`type`, `status`, `traceId`) is in the result's `_meta` under `dev.musher/problem`.
- Past the rate limit the server answers `429` with a `Retry-After` header. Wait that many seconds.

## Deploy your own image, in order

1. `list_organizations`, then `list_deployments`, `list_components` and `list_blueprints`, so you know what exists.
2. `get_schema` with `schema_id: "component-create"` returns the whole component document schema. Read it before you
   write a component. There is no blueprint document schema to fetch: `blueprint-create` types the document as any
   object. Start from the example in `blueprints.md`.
3. `validate_component` with `scope: "PUBLICATION"`, then `create_component` (`body.slug`, `body.document`), then
   `publish_component_version`. A blueprint cannot publish while it names an unpublished component revision.
4. `validate_blueprint`, then `create_blueprint` with the whole document in `body.document`, then
   `publish_blueprint_version`. Each node names its component by `componentRef`, the component's id, and `revision`.
5. `get_blueprint_version_deploy_form`, then `deploy_blueprint` (`body.blueprintId`, `body.revision`, `body.name`).
6. Poll `get_deployment` until `status.phase` is `ACTIVE` and `status.readiness` is `READY`. While you wait,
   `status.progress` names the stage and the node that blocks it, and `list_deployment_replicas` shows each node.
7. Build the URL from `status.endpoints[]`: `publicScheme`, then `://`, then `publicHostname`. The field `publicUrl`
   holds the bare hostname.

To change a running app, send the whole document again with `metadata.revision` raised by one
(`create_component_version`, `create_blueprint_version`), publish, then call `update_deployment` with
`body.revision`.

## Read a validation answer

- `INCOMPLETE` with an empty `diagnostics` list is the best answer `validate_component` and `validate_blueprint`
  give. It means nothing wrong was found. Each `deferred` row is a rule the validator did not judge.
- `INVALID` lists every problem with a JSON pointer to the member to fix.
- Validation does not check that a compute profile is offered, or that anything can be placed, even at
  `scope: "DEPLOYMENT"`. Take profile slugs from `list_compute_profiles`.

## Choose a compute profile that places

- `get_deploy_readiness` answering `deployable: true` says a region is online. It does not say a given profile fits.
- A node that cannot be placed reads `WAITING_FOR_HOST` in `status.progress.stage`, and its replica reads
  `placementReason: no_eligible_host` in `list_deployment_replicas`. The message says it starts "as soon as a host is
  ready". No host may be on its way: in one run a 2 GiB profile waited ten minutes and never placed, while the 1 GiB
  profile placed in six seconds.
- If the stage has not moved in three minutes, tell the user. Offer a smaller profile (a new blueprint revision, then
  `update_deployment`) or `cancel_deployment`. Don't wait in silence.
- `placementReason` can still read `no_eligible_host` after `placementStatus` reads `DECIDED`. Read the status.

## Updates roll every node

`update_deployment` gave every node a new replica, including nodes the new revision did not change. A node with a
volume is down while the volume detaches and attaches again: three to four minutes in each of four updates. So:

- put every change you can into one revision;
- tell the user the whole app goes down before each update;
- for a few seconds after an update `status.health` can still read `HEALTHY`. Wait for `readiness: READY`.

## Parameters and the deploy form

- A blueprint parameter takes one of `default` (a submitted value replaces it), `generator` (the platform makes a
  secret at deploy) or `from` (an organization variable, a connection, or a fact about the deployer).
- The form can mark a parameter `required: true` when every input it feeds is `required: false`. A deploy that left
  such a parameter out was accepted. Ask the user for it, but don't invent a value to satisfy the form.
- You are never shown a secret or a deployment's resolved environment. To confirm what a container received, read
  the app's own start-up lines with `list_deployment_log_entries`.
- A binding is one whole value: a parameter, another node's output, or a literal. It cannot join two sources into
  one string. A component output can be a template over its own endpoints, such as
  `http://${{ self.endpoints.web.privateAddress }}/api`, and a node may bind its own output to its own input. That
  is how an app learns its own public URL.

## Sign-in on an endpoint

An exposure of `visibility: PUBLIC`, `access: RESTRICTED` puts Musher's sign-in in front of an endpoint. With
`viewerIdentity: HEADER` and `viewerClaims: [EMAIL, NAME]`, the app receives `musher-viewer-id`,
`musher-viewer-email` and `musher-viewer-name` on each request (`get_endpoint` lists them under `forwardedHeaders`).

- A browser is redirected to sign in. A script gets `401`. So you cannot fetch the page to prove it works: report
  the deployment's readiness and the endpoint's `servingStatus`, and say that a person has to open it.
- The endpoint admits `DEPLOYMENT_MANAGERS` by default. `set_endpoint_access_policy` widens it to
  `ORGANIZATION_MEMBERS`.
- Many apps make the first person to sign in their administrator. Tell the user to open the app first.
- Where sign-in is not enforced yet, such a deploy is refused with `VIEWER_ACCESS_NOT_ENFORCED` and nothing starts.

## A language model without a key

`list_llm_connections` shows the organization's connections. One with `kind: MANAGED` is served by Musher and paid
from the organization's balance, so an app can have a model with no outside key. Inference is billed by use: confirm
with the user first.

1. Write an `EXTERNAL` component whose one input is a connection
   (`connection: {protocol: OPENAI_CHAT_COMPLETIONS, capabilities: [STREAMING, TOOL_CALLS]}`) and whose outputs
   forward its members: `from: {input: llm, member: baseURL}`, and the same for `apiKey` (with `sensitive: true`)
   and `model`.
2. In the blueprint, declare `llm: {from: "${{ connections.llm.default }}"}` under `parameters`, add a node for the
   component with `bindings: {llm: {parameter: llm}}` and no compute, and bind the app's inputs to
   `{node: llm, output: baseURL}`, `apiKey` and `model`.
3. After the deploy, `list_deployment_connections` shows the selection with `provisioning: GRANTED`.

The Catalog's own Open WebUI listing is wired this way. Read any listing's blueprint with
`get_blueprint_version_document` and its components with `list_blueprint_version_item_components`, using the
listing's `blueprintId` and `blueprintVersion`, and copy its conventions.

## Gotchas

- **Three spellings in one call.** Ids and filters at the top level are snake_case (`blueprint_id`, `deployment_id`,
  `event_kind`). Everything inside `body` is camelCase (`blueprintId`, `componentRef`). `idempotencyKey` is
  camelCase at the top level. `publish_blueprint_version` takes `blueprint_id`; `deploy_blueprint` takes
  `body.blueprintId`.
- **`idempotencyKey`** is 16 to 128 letters, digits, `_` or `-`. A UUID fits. Send one with every write.
- **List answers differ.** Most are `{"data": […], "meta": {"nextCursor", "hasMore"}}`. Some name the list instead:
  `regions`, `computeProfiles`, `connections`, `models`, `components` (in `list_deployment_replicas`). Check the keys
  before you conclude a list is empty or has no more pages.
- **A cursor only fits the sort and filters it came from.** Change either and start again from the first page.
- **Log severity is the stream.** A line an app writes to standard error is `ERROR`, whatever it says. Don't report
  errors from the label alone; read the line.
- **`list_deployment_activity` kinds** look like `deployment.release_applied`. An unknown kind returns an empty page,
  not an error.
- **`status.allowedActions`** covers suspend, resume, retry, cancel and terminate only. Its silence about update,
  restart, redeploy and rollback says nothing.
- **`search_catalog_listings`** matches a listing's title and tagline only. Search for the app's name, then browse
  with `list_catalog_listings`, before you decide an app is not in the Catalog.
- **No tool looks up an image's tags.** Ask the user for the tag, or read the registry yourself, before you pin one.
- **Many writes are marked destructive** that destroy nothing, such as `publish_component_version` and
  `deploy_blueprint`. Don't spend the user's patience confirming each one; confirm what bills or deletes.
