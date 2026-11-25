{
  "metadata": {
    "id": "7f1e3d5c-9b8a-4c6d-8e2f-4a6b8c0d2e4f",
    "organizationId": "0f4e2a6b-7c1d-4e8f-9a3b-5c6d7e8f9a0b",
    "name": "{{input.body.name}}",
    "sourceListingId": null,
    "sourceListingVersion": null,
    "sourceListingSlug": null,
    "sourceListingName": null,
    "sourceListingCategory": null,
    "createdBy": "3a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d",
    "createdByApiKeyId": null,
    "createdAt": "2026-11-23T14:02:11Z",
    "updatedAt": "2026-11-23T14:02:11Z",
    "rowVersion": 1
  },
  "spec": {
    "blueprintId": "2e4f6a8b-0c1d-4e3f-a5b7-c9d1e3f5a7b9",
    "blueprintVersion": 1,
    "resolutionId": "7f1e3d5c-9b8a-4c6d-8e2f-4a6b8c0d2e4f",
    "environmentId": null
  },
  "status": {
    "phase": "PROVISIONING",
    "desiredPhase": "ACTIVE",
    "desiredReason": null,
    "desiredSetAt": "2026-11-23T14:02:11Z",
    "health": "UNKNOWN",
    "readiness": "NOT_READY",
    "conditions": [],
    "error": null,
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
        "isAllowed": true,
        "reason": null
      },
      {
        "action": "RETRY",
        "isAllowed": false,
        "reason": "Only a FAILED deployment can be retried."
      }
    ],
    "progress": null,
    "endpoints": null,
    "reason": null,
    "draftedAt": "2026-11-23T14:02:11Z",
    "provisioningRequestedAt": "2026-11-23T14:02:11Z",
    "becameActiveAt": null,
    "failedAt": null,
    "suspendedAt": null,
    "deletedAt": null
  }
}
