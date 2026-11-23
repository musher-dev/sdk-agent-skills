# Deploying the user's own app

There are two routes:

- **The CLI.** One command, and it updates in place. It needs musher CLI 0.4.1 or later.
- **The API.** It works with any CLI, or none, but takes several calls.

Check which one you have with `musher deploy --help`.

## Contents

- [The CLI route](#the-cli-route)
- [Building from source](#building-from-source)
- [Private images](#private-images)
- [The API route](#the-api-route)

## The CLI route

`musher deploy`, `musher init` and `musher build` shipped in musher CLI 0.4.0. Use 0.4.1 or later: an older CLI can
wait out its timeout on a deploy that has already failed. `musher version` prints the version (there is no
`--version` flag).

If `musher deploy --help` fails, the installed CLI is a bundle-era 0.3.x release that cannot deploy. Tell the user
how to upgrade, and ask before you run it:

- macOS, Linux or WSL: `curl -fsSL https://get.musher.dev | sh`. Running it again replaces the binary with the
  latest release.
- Windows, in PowerShell: `irm https://get.musher.dev/install.ps1 | iex`.
- On 0.4.0 or later, `musher update` upgrades in place.
- The steps are at https://docs.musher.dev/guides/deploy/install-the-cli.

Or deploy without the CLI: through the MCP tools (`mcp.md`) or the API route below.

With an image that's already pushed, pin it by digest or by a version tag:

```bash
musher deploy api --image ghcr.io/acme/api:v1.4.2 --port 8080 --json --no-input
```

| Flag | Use |
| --- | --- |
| `--image` | The image to run. Don't use `latest` |
| `--port` | The port the container listens on, which becomes the endpoint's `targetPort` |
| `--kind` | `SERVICE` (the default, with an endpoint), `WORKER` (no endpoint) or `JOB` |
| `--size` | A compute profile, such as `general.standard.small` (`auth-and-billing.md` lists them) |
| `--replicas` | How many copies to run |
| `-e KEY=VALUE`, `--env-file` | Environment variables. Don't put secrets in `-e` on a shared machine; use `--env-file` |
| `--environment` | The environment to deploy into (default: the organization's standard one) |
| `--detach` | Return as soon as the deploy is submitted, instead of watching it |
| `--timeout`, `--wait-for ready\|url` | How long to watch, and what counts as done |
| `--json`, `--no-input` | Always pass both. With `--json`, stdout is one JSON object, and `.url` is the address |

The name identifies the deployment. Deploying the same name again updates it in place, keeping its id and URL. An
unchanged deployment does nothing; `--force` rolls it anyway. Exit code 8 means it reached `FAILED`
(`troubleshoot.md`).

## Building from source

`musher init` detects the project and writes `musher.yaml` with an explicit build recipe. Review that file with the
user before the first deploy. `musher deploy` then builds the image locally, pushes it to the user's own registry
and deploys that exact digest.

```yaml
apiVersion: musher.dev/v1
kind: App
metadata:
  name: web
spec:
  workload:
    kind: SERVICE
    build:
      repository: ghcr.io/acme/web   # where the image is pushed
      context: .
      dockerfile: Dockerfile
    endpoints:
      http: {targetPort: 8080}
```

- The build needs Docker (or a standalone BuildKit) on this machine, and push access to the registry (`docker login`).
  Musher doesn't host a registry.
- Images are built for `linux/amd64` by default, so a build on Apple Silicon still runs. Override with `--platform`.
- `musher.yaml` stays on this machine. The CLI compiles it into a component and a blueprint before it calls the API.

## Private images

A private image needs a pull credential for its registry, which the user adds in the Console under
**Configuration → Registry Credentials**. `musher deploy` warns when one is missing. If the user prefers not to add
one, make the image public.

## The API route

A deployment comes from a published blueprint revision, and a blueprint refers to components. To deploy your own
image through the API:

1. Write a component (`kind: COMPONENT`) for the image and check it with
   `POST /v1/organizations/{org}/components:validate`. Then create it with `POST /v1/organizations/{org}/components`.
   The response's `componentId` is what a blueprint names.
2. Publish the component revision: `POST /v1/components/{id}/versions/{revision}:publish`. A blueprint cannot
   publish while it names an unpublished component revision.
3. Write a blueprint that places the component on a compute profile (`blueprints.md`). Each node names its component
   by `componentRef`, the component's id, and `revision`. Check it with
   `POST /v1/organizations/{org}/blueprints:validate`, then create it with
   `POST /v1/organizations/{org}/blueprints`.
4. Publish the revision: `POST /v1/blueprints/{id}/versions/{revision}:publish`.
5. Deploy it with `POST /v1/organizations/{org}/deployments:deployBlueprint`, using the body
   `{"blueprintId": "…", "revision": 1, "name": "…"}` and an `Idempotency-Key` header.
6. Wait for `ACTIVE` and `READY`, and get the URL, as in SKILL.md.

A validation answer of `INCOMPLETE` with no `diagnostics` is the best one `:validate` gives: nothing wrong was found.
It does not check that the compute profile is offered or that a host has room. Take the profile from
`GET /v1/reference/compute-profiles`, and if the deployment sits in `WAITING_FOR_HOST`, see `troubleshoot.md`.

With Musher's MCP tools the same six steps are six tools: `mcp.md`.

The request and response shapes are in the OpenAPI document, https://api.musher.dev/openapi.json. Read the operation
before you call it, and don't guess field names. If the user can wait for a CLI with `deploy`, that route is much
shorter.
