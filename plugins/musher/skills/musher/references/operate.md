# Operating a deployment

Every path below takes `Authorization: Bearer $MUSHER_API_KEY`. Send an `Idempotency-Key` header with every `POST`.
The deployment id is `metadata.id` in any deployment response. To look one up by name, use
`GET /v1/organizations/{org}/deployments:byName?name=<name>`.

## Status

- **API:** `GET /v1/deployments/{id}`. Read `status.phase`, which is one of `DRAFT`, `PROVISIONING`, `ACTIVE`,
  `DEGRADED`, `FAILED`, `SUSPENDED` or `DELETED`. `status.health` and `status.readiness` add detail, and
  `status.error` explains a failure. `status.allowedActions` says which of the actions below the deployment accepts
  right now, so check it before you call one.
- **CLI:** `musher status <name> --json`. Add `--conditions` or `--replicas` for more detail, and `--watch` to follow it.
- **List:** `GET /v1/organizations/{org}/deployments`, or `musher list --json`.

## URLs

`GET /v1/organizations/{org}/deployments/{id}/endpoints`. Each entry's `publicUrl` is the address to give the user,
and `servingStatus` says whether it is serving yet.

## Logs

- **API:** `GET /v1/deployments/{id}/log-entries`, newest first. You can filter with `stream` (`RUNTIME`, the
  default; `BUILD`; or `SYSTEM`), `severity` (`DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`), `search`, `node`
  and `limit`. Page through with `cursor`. A cursor only works with the filters it came from; changing a filter
  returns `400 invalid-cursor`.
- **CLI:** `musher logs <name>`. Useful flags: `-n 200`, `--severity ERROR`, `--stream BUILD` and `-f` to follow.
- A deploy that fails before it runs usually explains itself in the `SYSTEM` or `BUILD` stream, not `RUNTIME`.

## Actions

| Action | API | Body | Note |
| --- | --- | --- | --- |
| Restart replicas | `POST /v1/deployments/{id}:restart` | `{}` or `{"nodeNames": ["web"]}` | Same image and config |
| Redeploy | `POST /v1/deployments/{id}:redeploy` | `{}` | A fresh placement on the same configuration |
| Roll back | `POST /v1/deployments/{id}:rollback` | `{"recordId": "…"}` | `recordId` from `GET /v1/deployments/{id}/releases`, an entry with `isRollbackEligible` |
| Suspend | `POST /v1/deployments/{id}:suspend` | `{"reason": "…"}` | Stops replicas and compute billing; volumes are kept and still billed |
| Resume | `POST /v1/deployments/{id}:resume` | | Goes back to `PROVISIONING` |

Confirm with the user before suspending, rolling back or redeploying: each one interrupts the running app. The CLI has
no commands for these actions; use the API, or the deployment's page in the Console.

## Updating

- **Your own app:** run `musher deploy` again with the same name. It updates the deployment in place and keeps its
  URL. An unchanged file does nothing; `--force` rolls it anyway.
- **A Catalog app:** change it in the Console. Copying it into the organization's library first
  (`POST /v1/organizations/{org}/blueprints:cloneFromListing`) makes it a blueprint you own (`blueprints.md`).
