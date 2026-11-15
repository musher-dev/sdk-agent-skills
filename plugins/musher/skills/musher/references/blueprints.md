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

## Starting from a Catalog app

To change a Catalog app before deploying it, copy it into the organization's library with
`POST /v1/organizations/{org}/blueprints:cloneFromListing`. A `COMPONENT` listing, such as `postgres`, `redis`,
`pgvector` or `valkey`, is copied with `POST /v1/organizations/{org}/components:cloneFromListing`, so a blueprint can
use it. Deploying a blueprint you own is the API route in `deploy-own-app.md`.
