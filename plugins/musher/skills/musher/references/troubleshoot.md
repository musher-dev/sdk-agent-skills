# Troubleshooting

## Reading an API error

Every API error is an RFC 9457 problem document (`application/problem+json`):

```json
{"type": "/errors/payment-required", "title": "…", "status": 402, "detail": "…", "instance": "…", "traceId": "…"}
```

Quote `detail` to the user. Keep `traceId`: Musher support needs it.

| Status | Usually means | Do |
| --- | --- | --- |
| `401` | The key is missing, wrong or revoked, or it is an MCP key ("not valid for this API surface") | Ask the user to check `MUSHER_API_KEY`. Never ask them to paste it |
| `402` | The balance can't cover the deploy | An Owner or Admin adds funds (`auth-and-billing.md`). Don't retry until then |
| `403` | The key lacks a permission, or the plan lacks a feature (`entitlement-required`) | Tell the user what `detail` says. Don't work around it |
| `404` | The id is wrong, or the resource belongs to another organization | Re-read the id from a list call |
| `409` | A name is already taken, a revision conflicts, or a `COMPONENT` listing was sent to a deploy path | Choose another name, re-read and retry, or use a blueprint |
| `422` | The request or the blueprint doesn't resolve | Every problem is in `errors`; nothing was created. Fix them all, then send it again |

Retrying a write with the **same** `Idempotency-Key` within 24 hours returns the original response, with
`Idempotent-Replayed: true`, rather than acting twice.

## CLI exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 2 | Authentication |
| 3 | Network |
| 4 | Configuration |
| 5 | Timed out waiting |
| 8 | The deployment reached `FAILED` |
| 9 | Permission (`403`) |
| 10 | Conflict (`409`) |
| 11 | Invalid request or spec (`400` / `422`) |
| 12 | The plan does not include this (entitlement) |
| 13 | Rate limited |
| 64 | Bad command-line usage |

## A deployment that won't come up

1. **`FAILED` before it ever ran.** Read the `SYSTEM` and `BUILD` logs (`operate.md`). Common causes:
   - the image can't be pulled: a private image with no registry credential, or a tag that doesn't exist;
   - a required parameter is missing;
   - no region could place the deployment. `GET /v1/deploy-readiness` shows whether any region is accepting new
     deployments.
2. **`PROVISIONING` that does not move, with `status.progress.stage` at `WAITING_FOR_HOST`.** No running host has
   room for that node's compute profile; its replica reads `placementReason: no_eligible_host`
   (`GET /v1/deployments/{id}/replicas`). The message says it starts as soon as a host is ready, but no host may be
   on its way, and `deploy-readiness` still reads deployable. After three minutes, tell the user and offer a
   smaller profile (publish a revision that names it, then `:update`) or `POST /v1/deployments/{id}:cancel`.
3. **`DEGRADED`, or `ACTIVE` with an endpoint that isn't serving.** Read the `RUNTIME` logs at `ERROR`. The most common
   cause is an app listening on a port other than the endpoint's `targetPort`, or only on `127.0.0.1`. It must listen
   on `0.0.0.0`.
4. **`ERR_DEPLOYMENT_FACT_UNAVAILABLE` on a Catalog app.** Some apps need facts about a signed-in person, which an API
   key doesn't carry. Give the user the Console route: Catalog → Blueprints → the app's card → Deploy.
5. **`musher deploy` isn't a command.** The CLI is an older 0.3.x release. Use the API (`deploy-own-app.md`).

Don't loop on redeploys. If two attempts fail the same way, stop. Show the user the `detail`, the last error log lines
and the `traceId`.
