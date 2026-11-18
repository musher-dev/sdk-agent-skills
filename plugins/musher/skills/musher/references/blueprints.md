# Components and blueprints

- A **component** describes one workload: an image, or a build that produces one, plus its endpoints, environment
  and the volumes it needs.
- A **blueprint** places one or more components on compute. It wires them together with bindings and declares the
  parameters someone fills in when they deploy it.
- A **deployment** runs one published revision of a blueprint.

Both are YAML with `specVersion: v2`. Validate every document against its published schema, and with the API's
`:validate` operations, before you create anything. Don't hand-write a field you haven't seen in a schema or an
example.

## Schemas

| Family | Schema (follows the latest v2 release) | Versions |
| --- | --- | --- |
| Component | https://specifications.musher.dev/component/v2/component.schema.json | https://specifications.musher.dev/component/versions.json |
| Blueprint | https://specifications.musher.dev/blueprint/v2/blueprint.schema.json | https://specifications.musher.dev/blueprint/versions.json |

To pin a release, use the exact path, for example `…/blueprint/v2.3.0/blueprint.schema.json`. The index of every
family is https://specifications.musher.dev/catalog.json.

## A minimal component

```yaml
specVersion: v2
kind: COMPONENT
metadata:
  revision: 1
  description: Static web server with one HTTP endpoint.
spec:
  type: SERVICE
  workload:
    source:
      image: nginx:1.29.4-alpine
    endpoints:
      web:
        targetPort: 8080
        protocol: HTTP
```

## A blueprint with a database

This is a web node and a PostgreSQL node. The database password is generated at deploy time and bound into both nodes:

```yaml
specVersion: v2
kind: BLUEPRINT
metadata:
  slug: web-and-database
  revision: 1
  description: A web application backed by PostgreSQL.
spec:
  parameters:
    postgresPassword:
      generator:
        byteLength: 32
        encoding: BASE64URL
  nodes:
    db:
      componentRef: ./components/postgres.yaml
      compute:
        profile: general.standard.small
      volumes:
        data:
          sizeGiB: 10
      bindings:
        postgresPassword:
          parameter: postgresPassword
    web:
      componentRef: ./components/web.yaml
      compute:
        profile: general.standard.small
      exposure:
        web: PUBLIC
      bindings:
        databaseAddress:
          node: db
          output: address
        databasePassword:
          parameter: postgresPassword
```

Notes:

- A secret belongs in a `generator` parameter, so it is generated at deploy time. Never write a secret's value into a
  document.
- `exposure` decides which endpoints are reachable from the internet; anything not listed stays private.
- A volume is billed for as long as it exists. Size it for what the app needs.
- For more examples (connections to an LLM, organization variables, external nodes, scheduled jobs and webhooks),
  see https://github.com/musher-dev/specifications/tree/main/specifications/blueprint/v2/examples and
  https://github.com/musher-dev/specifications/tree/main/specifications/component/v2/examples.

## A component and a blueprint the API accepts

The example above names its components by file (`./components/postgres.yaml`). Only a Catalog item does that. A
blueprint you create through the API or the MCP tools names a published component by its id and revision. This pair
is cut down from one that was deployed on release 27.0.1, and both documents pass `:validate`. Put your own
component's id in `componentRef`.

```yaml
specVersion: v2
kind: COMPONENT
metadata:
  revision: 1
  description: Grist, a shared board, with its data on a volume.
spec:
  type: SERVICE
  workload:
    source:
      image: gristlabs/grist:1.7.22
    endpoints:
      web:
        targetPort: 8484
        protocol: HTTP
    volumes:
      data:
        mountPath: /persist
        minSizeGiB: 1
    health:
      startup:
        http: {endpoint: web, path: /status}
        periodSeconds: 5
        failureThreshold: 60
      readiness:
        http: {endpoint: web, path: /status}
  contract:
    inputs:
      homeURL:
        description: Public URL people open the board at.
        schema: {type: string}
        target: {envVar: APP_HOME_URL}
      sessionSecret:
        description: Secret the app signs its sessions with.
        schema: {type: string}
        sensitive: true
        target: {envVar: GRIST_SESSION_SECRET}
      adminEmail:
        description: Email address of the first administrator.
        schema: {type: string}
        target: {envVar: GRIST_DEFAULT_EMAIL}
      forwardAuthHeader:
        description: Request header the app trusts for the signed-in viewer's email.
        schema: {type: string}
        required: false
        target: {envVar: GRIST_FORWARD_AUTH_HEADER}
    outputs:
      publicURL:
        description: Public URL of the board.
        schema: {type: string}
        from: {endpoint: web, property: publicURL}
      apiBaseURL:
        description: Private base URL of the board's API, for other nodes in the same deployment.
        schema: {type: string}
        from:
          template: "http://${{ self.endpoints.web.privateAddress }}/api"
```

```yaml
specVersion: v2
kind: BLUEPRINT
metadata:
  slug: team-board
  revision: 1
  description: A shared Grist board with a persistent volume, behind Musher sign-in.
spec:
  parameters:
    sessionSecret:
      generator:
        byteLength: 32
    adminEmail:
      ui:
        label: Administrator email
  nodes:
    board:
      componentRef: 00000000-0000-0000-0000-000000000000   # the component's id
      revision: 1                                          # a published revision of it
      compute:
        profile: general.economy.nano
      volumes:
        data:
          sizeGiB: 1
      exposure:
        web:
          visibility: PUBLIC
          access: RESTRICTED
          viewerIdentity: HEADER
          viewerClaims: [EMAIL]
      bindings:
        homeURL:                 # the node's own output, bound to its own input
          node: board
          output: publicURL
        sessionSecret:
          parameter: sessionSecret
        adminEmail:
          parameter: adminEmail
        forwardAuthHeader:
          value: Musher-Viewer-Email
```

What it shows:

- Each environment variable the container reads is an input with `target.envVar`. An input with no binding takes
  its `default`. Mark an input the app can run without `required: false`.
- An output can read an endpoint property (`publicURL`, `privateAddress`, …) or be a template over the
  component's own endpoints. A node may bind its own output to its own input, which is how an app learns its
  public URL.
- A binding is one whole value: a parameter, another node's output, or a literal. It cannot join two sources into
  one string.
- `access: RESTRICTED` puts Musher's sign-in in front of the endpoint; write `web: PUBLIC` for an open one. With
  `viewerIdentity: HEADER` and the `EMAIL` claim, the app receives the viewer's address in `Musher-Viewer-Email`.
  A script gets `401` from such an endpoint, so only a person can check the page.
- A parameter with only `ui` appears on the deploy form. One with `generator` or `from` never does.
- To give an app the organization's language model without a key, see "A language model without a key" in `mcp.md`.
  The documents are the same through the API.

## Starting from a Catalog app

To change a Catalog app before deploying it, copy it into the organization's library with
`POST /v1/organizations/{org}/blueprints:cloneFromListing`. A `COMPONENT` listing, such as `postgres`, `redis`,
`pgvector` or `valkey`, is copied with `POST /v1/organizations/{org}/components:cloneFromListing`, so a blueprint can
use it. Deploying a blueprint you own is the API route in `deploy-own-app.md`.
