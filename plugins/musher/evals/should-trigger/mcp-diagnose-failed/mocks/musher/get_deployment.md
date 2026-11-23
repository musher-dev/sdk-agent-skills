---
expect:
  deployment_id: "6d2f8a4c-1e3b-4c5d-9f7a-2b4c6d8e0f1a"
---

{
  "metadata": {
    "id": "6d2f8a4c-1e3b-4c5d-9f7a-2b4c6d8e0f1a",
    "organizationId": "0f4e2a6b-7c1d-4e8f-9a3b-5c6d7e8f9a0b",
    "name": "team-n8n",
    "sourceListingId": null,
    "sourceListingVersion": null,
    "sourceListingSlug": null,
    "sourceListingName": null,
    "sourceListingCategory": null,
    "createdBy": "3a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
    "createdByApiKeyId": null,
    "createdAt": "2026-11-23T13:38:05Z",
    "updatedAt": "2026-11-23T13:41:52Z",
    "rowVersion": 6
  },
  "spec": {
    "blueprintId": "9a7c5e3b-1d2f-4a6c-8e0b-3d5f7a9c1e2b",
    "blueprintVersion": 3,
    "resolutionId": "6d2f8a4c-1e3b-4c5d-9f7a-2b4c6d8e0f1a",
    "environmentId": null
  },
  "status": {
    "phase": "FAILED",
    "desiredPhase": "ACTIVE",
    "desiredReason": null,
    "desiredSetAt": "2026-11-23T13:38:05Z",
    "health": "UNHEALTHY",
    "readiness": "NOT_READY",
    "conditions": [
      {
        "type": "PROVISIONED",
        "status": "FALSE",
        "source": "DERIVED",
        "reason": "ImagePullFailed",
        "message": "Node web could not pull its image.",
        "observedGeneration": null,
        "lastTransitionAt": "2026-11-23T13:41:52Z"
      }
    ],
    "error": {
      "code": "IMAGE_PULL_FAILED",
      "origin": "USER",
      "title": "A container image could not be pulled",
      "detail": null,
      "remediation": "Check the image reference and that Musher can pull it, then retry the deployment.",
      "occurredAt": "2026-11-23T13:41:52Z",
      "isRetryable": false
    },
    "allowedActions": [
      {
        "action": "SUSPEND",
        "isAllowed": false,
        "reason": "Only an ACTIVE deployment can be suspended."
      },
      {
        "action": "RESUME",
        "isAllowed": false,
        "reason": "Only a SUSPENDED deployment can be resumed."
      },
      {
        "action": "TERMINATE",
        "isAllowed": true,
        "reason": null
      },
      {
        "action": "CANCEL",
        "isAllowed": false,
        "reason": "Only a deployment that is still provisioning can be cancelled."
      },
      {
        "action": "RETRY",
        "isAllowed": true,
        "reason": null
      }
    ],
    "progress": {
      "stage": "PULLING_IMAGE",
      "step": 4,
      "stepCount": 8,
      "isLive": false,
      "isFailed": true,
      "readyComponents": 0,
      "totalComponents": 1,
      "blockingNode": "web",
      "reason": "ImagePullFailed",
      "message": "Node web failed while pulling its image.",
      "changedAt": "2026-11-23T13:41:52Z",
      "expectedServingBy": null
    },
    "endpoints": [
      {
        "id": "e1a3c5e7-9b0d-4f2a-8c4e-6a8c0e2a4c6e",
        "nodeName": "web",
        "endpointName": "http",
        "publicHostname": null,
        "publicUrl": null,
        "publicScheme": "https",
        "servingStatus": "NOT_PUBLISHED",
        "servingStatusReason": "DeploymentFailed"
      }
    ],
    "reason": "Node web could not pull its image.",
    "draftedAt": "2026-11-23T13:38:05Z",
    "provisioningRequestedAt": "2026-11-23T13:38:06Z",
    "becameActiveAt": null,
    "failedAt": "2026-11-23T13:41:52Z",
    "suspendedAt": null,
    "deletedAt": null
  }
}
