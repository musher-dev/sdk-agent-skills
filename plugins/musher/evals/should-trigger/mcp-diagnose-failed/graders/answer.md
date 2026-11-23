---
type: llm
weight: 1
---

Musher's MCP tools are connected. The deployment team-n8n is FAILED with the error IMAGE_PULL_FAILED. Its SYSTEM log
lines say that no registry credential in the organization matches ghcr.io, so ghcr.io/acme/n8n-custom:1.2.0 was pulled
anonymously, and every attempt failed with "unauthorized: authentication required".

PASS only if all of these hold:

1. It names the cause the logs show: the image ghcr.io/acme/n8n-custom:1.2.0 couldn't be pulled because the registry
   refused an unauthenticated pull, so the image is private and Musher has no credential for it.
2. It gives a fix for that cause before any retry: add a registry credential for ghcr.io in Musher, or make the image
   public.
3. It doesn't say it redeployed, retried or restarted the deployment.

FAIL if it gives a different cause, only suggests redeploying or retrying, or says it already did.
