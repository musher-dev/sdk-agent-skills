# Changelog

## 0.2.0 (unreleased)

- `references/mcp.md`: the route for a session that has Musher's MCP tools. It gives the order that deploys your own
  image, how to read a validation answer and a placement that waits for a host, what an update does to a running
  app, sign-in on an endpoint, a language model with no outside key, and a list of gotchas.
- A component and blueprint pair the API accepts, with components named by id and revision.
- Corrections: the component is published before the blueprint; `publicUrl` is a bare hostname; a deploy is done at
  `ACTIVE` and `READY`; `allowedActions` covers five actions; log severity is the stream; an MCP key is not an API
  key.

## 0.1.0 (unreleased)

- The `musher` skill. It deploys Catalog apps through the Musher API, deploys an image or a repository with
  `musher deploy`, writes v2 blueprints against the published schemas, operates deployments (status, URLs, logs,
  restart, rollback, suspend) and explains failures.
- The `musher` Claude Code plugin, and the marketplace that lists it.
