# Operating a deployment

Every path below takes `Authorization: Bearer $MUSHER_API_KEY`. Send an `Idempotency-Key` header with every `POST`.
The deployment id is `metadata.id` in any deployment response. To look one up by name, use
`GET /v1/organizations/{org}/deployments:byName?name=<name>`.

## Status

- **API:** `GET /v1/deployments/{id}`. Read `status.phase`, which is one of `DRAFT`, `PROVISIONING`, `ACTIVE`,
  `DEGRADED`, `FAILED`, `SUSPENDED` or `DELETED`. `status.health` and `status.readiness` add detail, and
  `status.error` explains a failure. `status.progress` names the stage a deploy has reached and the node that
  blocks it. `status.allowedActions` covers suspend, resume, retry, cancel and terminate only: it says nothing about
  restart, redeploy, rollback or update.
- **Per node:** `GET /v1/deployments/{id}/replicas` gives each node's rollout stage and each replica's placement.
  `GET /v1/deployments/{id}/activity` is the timeline, newest first.
- **CLI:** `musher status <name> --json`. Add `--conditions` or `--replicas` for more detail, and `--watch` to follow it.
- **List:** `GET /v1/organizations/{org}/deployments`, or `musher list --json`.

## URLs

`GET /v1/organizations/{org}/deployments/{id}/endpoints`. Each entry's `publicUrl` holds the bare hostname: put
`publicScheme` and `://` in front of it before you give it to the user. `servingStatus` says whether it is serving
yet. An endpoint whose `access.mode` is `RESTRICTED` answers a script `401` and sends a browser to sign in.

## Logs

- **API:** `GET /v1/deployments/{id}/log-entries`, newest first. You can filter with `stream` (`RUNTIME`, the
  default; `BUILD`; or `SYSTEM`), `severity` (`DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`), `search`, `node`
  and `limit`. Page through with `cursor`. A cursor only works with the filters it came from; changing a filter
  returns `400 invalid-cursor`.
- **CLI:** `musher logs <name>`. Useful flags: `-n 200`, `--severity ERROR`, `--stream BUILD` and `-f` to follow.
- A deploy that fails before it runs usually explains itself in the `SYSTEM` or `BUILD` stream, not `RUNTIME`.
- `severity` is the stream, not the app's level: every line an app writes to standard error is `ERROR`. Read the
  line before you call it an error.

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
- **A blueprint you own, through the API:** create and publish the next revision, then
  `POST /v1/deployments/{id}:update` with `{"revision": <n>}`. An update gives every node a new replica, changed
  or not, and a node with a volume is down for three to four minutes while the volume moves. Put your changes in
  one revision, and tell the user before you send it.
- **A Catalog app:** change it in the Console. Copying it into the organization's library first
  (`POST /v1/organizations/{org}/blueprints:cloneFromListing`) makes it a blueprint you own (`blueprints.md`).
