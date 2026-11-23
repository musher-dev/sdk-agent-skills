---
expect:
  component_id: "8c3d5e7f-9a1b-4c2d-8e4f-6a8b0c2d4e6f"
  revision: "1"
---

{
  "componentId": "8c3d5e7f-9a1b-4c2d-8e4f-6a8b0c2d4e6f",
  "revision": 1,
  "status": "PUBLISHED",
  "document": {
    "specVersion": "v2",
    "kind": "COMPONENT",
    "metadata": {
      "revision": 1,
      "description": "The acme API service, from ghcr.io/acme/api:v1.4.2."
    },
    "spec": {
      "type": "SERVICE",
      "workload": {
        "source": {
          "image": "ghcr.io/acme/api:v1.4.2"
        },
        "endpoints": {
          "http": {
            "targetPort": 8080,
            "protocol": "HTTP"
          }
        }
      }
    }
  },
  "documentSha256": "4f1c0a9e7b2d3c5a6e8f0b1d2c3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e",
  "validation": {
    "status": "INCOMPLETE",
    "validationScope": "PUBLICATION",
    "phase": "ADMISSION",
    "diagnostics": [],
    "deferred": [
      {
        "rule": "COMP-ID-001",
        "pointer": "/metadata",
        "missing": "the component's stored history"
      }
    ]
  },
  "publicationValidation": {
    "status": "INCOMPLETE",
    "validationScope": "PUBLICATION",
    "phase": "ADMISSION",
    "diagnostics": [],
    "deferred": [
      {
        "rule": "COMP-ID-001",
        "pointer": "/metadata",
        "missing": "the component's stored history"
      }
    ]
  },
  "rowVersion": 2,
  "draftedBy": "3a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
  "publishedBy": "3a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
  "statusReason": null,
  "supersededByRevision": null,
  "sourceRepository": null,
  "createdAt": "2026-11-23T14:02:11Z",
  "updatedAt": "2026-11-23T14:02:11Z",
  "publishedAt": "2026-11-23T14:02:11Z",
  "deprecatedAt": null,
  "withdrawnAt": null
}
