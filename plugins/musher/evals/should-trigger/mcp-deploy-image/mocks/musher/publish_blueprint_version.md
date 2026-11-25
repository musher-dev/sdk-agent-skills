---
expect:
  blueprint_id: "2e4f6a8b-0c1d-4e3f-a5b7-c9d1e3f5a7b9"
  revision: "1"
---

{
  "blueprintId": "2e4f6a8b-0c1d-4e3f-a5b7-c9d1e3f5a7b9",
  "revision": 1,
  "status": "PUBLISHED",
  "document": {
    "specVersion": "v2",
    "kind": "BLUEPRINT",
    "metadata": {
      "slug": "api",
      "revision": 1,
      "description": "The acme API on one node."
    },
    "spec": {
      "nodes": {
        "api": {
          "componentRef": "8c3d5e7f-9a1b-4c2d-8e4f-6a8b0c2d4e6f",
          "revision": 1,
          "compute": {
            "profile": "general.standard.small"
          },
          "exposure": {
            "http": "PUBLIC"
          }
        }
      }
    }
  },
  "documentSha256": "e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3c2d1b0f8e6a5c3d2b7e9a0c1f4",
  "itemComponentRefs": [],
  "validation": {
    "status": "INCOMPLETE",
    "validationScope": "PUBLICATION",
    "phase": "ADMISSION",
    "diagnostics": [],
    "deferred": [
      {
        "rule": "BP-RESOLVE-001",
        "pointer": "/spec/nodes",
        "missing": "platform admission"
      }
    ]
  },
  "rowVersion": 2,
  "sourceListingId": null,
  "draftedBy": "3a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
  "statusReason": null,
  "createdAt": "2026-11-23T14:02:11Z",
  "updatedAt": "2026-11-23T14:02:11Z",
  "publishedAt": "2026-11-23T14:02:11Z",
  "withdrawnAt": null
}
