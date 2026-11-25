---
expect:
  deployment_id: "6d2f8a4c-1e3b-4c5d-9f7a-2b4c6d8e0f1a"
---

{
  "data": [
    {
      "id": "0b00c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c00",
      "occurredAt": "2026-11-23T13:41:52Z",
      "severity": "ERROR",
      "kind": "SYSTEM",
      "message": "Node web failed: IMAGE_PULL_FAILED. No replica started.",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    },
    {
      "id": "0b01c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c01",
      "occurredAt": "2026-11-23T13:41:51Z",
      "severity": "ERROR",
      "kind": "SYSTEM",
      "message": "Failed to pull image \"ghcr.io/acme/n8n-custom:1.2.0\": unauthorized: authentication required (attempt 3 of 3)",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    },
    {
      "id": "0b02c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c02",
      "occurredAt": "2026-11-23T13:40:21Z",
      "severity": "WARNING",
      "kind": "SYSTEM",
      "message": "Failed to pull image \"ghcr.io/acme/n8n-custom:1.2.0\": unauthorized: authentication required (attempt 2 of 3); retrying",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    },
    {
      "id": "0b03c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c03",
      "occurredAt": "2026-11-23T13:39:06Z",
      "severity": "WARNING",
      "kind": "SYSTEM",
      "message": "Failed to pull image \"ghcr.io/acme/n8n-custom:1.2.0\": unauthorized: authentication required (attempt 1 of 3); retrying",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    },
    {
      "id": "0b04c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c04",
      "occurredAt": "2026-11-23T13:39:05Z",
      "severity": "INFO",
      "kind": "SYSTEM",
      "message": "No registry credential in this organization matches ghcr.io; pulling ghcr.io/acme/n8n-custom:1.2.0 anonymously",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    },
    {
      "id": "0b05c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c05",
      "occurredAt": "2026-11-23T13:39:04Z",
      "severity": "INFO",
      "kind": "SYSTEM",
      "message": "Pulling image ghcr.io/acme/n8n-custom:1.2.0 for node web",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    },
    {
      "id": "0b06c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c06",
      "occurredAt": "2026-11-23T13:39:01Z",
      "severity": "INFO",
      "kind": "SYSTEM",
      "message": "Replica scheduled for node web on general.standard.small",
      "replicaId": "c4e6a8b0-2d3f-4b5c-9d7e-1f3a5c7e9b0d",
      "node": "web",
      "structuredFields": null
    }
  ],
  "meta": {
    "nextCursor": null,
    "hasMore": false
  }
}
