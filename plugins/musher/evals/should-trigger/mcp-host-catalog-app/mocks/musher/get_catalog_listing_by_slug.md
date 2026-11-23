---
expect:
  slug: "n8n"
---

{
  "id": "75c7ec47-c756-54d5-952f-d5a71189c8f9",
  "slug": "n8n",
  "publisherId": "00000000-0000-0000-0000-000000000001",
  "publisher": {
    "id": "00000000-0000-0000-0000-000000000001",
    "displayName": "Musher",
    "avatarUrl": null,
    "isOfficial": true,
    "slug": null
  },
  "version": 11,
  "displayName": "n8n",
  "summary": "Fair-code workflow automation with 400+ integrations and a built-in code node",
  "category": "AUTOMATION",
  "lifecycleStage": "STABLE",
  "itemType": "BLUEPRINT",
  "overview": "## What it is\nn8n is a fair-code workflow automation tool for technical teams. Build\nautomations visually on a node canvas across hundreds of SaaS, API,\nand database integrations, and drop into JavaScript in a code node\nwhenever the visual building blocks aren't enough.\n\n## When to use\n- You want to wire SaaS tools, APIs, and databases into automated\n  workflows without writing and hosting glue services.\n- You need self-hosted automation where the data and credentials stay\n  on infrastructure you control.\n- You're triggering workflows from inbound webhooks and want the\n  webhook endpoints on your own domain.\n\n## Defaults\nSingle-container deployment of `n8nio/n8n:2.46.7` with the web UI on\nport 5678 behind the platform's HTTPS edge and the platform's sign-in:\nonly people allowed into this deployment reach the editor.\nWebhooks, forms, MCP triggers, the public API (`/api`, with an n8n API\nkey) and the instance MCP server stay reachable without signing in, so\nthe services that call them keep working.\n\nThere is no setup screen. The owner account is the person who installed\nthe deployment: it signs in with their verified email and the generated\nowner password on the deployment's Installation tab. n8n re-applies that\nowner on every start and doesn't let its email or password be changed\ninside n8n, and upgrading an existing deployment replaces an owner set\nup by hand with the deployer's email and the generated password. Webhook, editor, and\nhost URLs are taken from this deployment's own public https address, so\nwebhook URLs are right the first time. The readiness probe\nwaits for `/healthz/readiness`, so first boot reports ready only after\ndatabase migrations finish. A 4 GiB persistent volume mounted at\n`/home/node/.n8n` keeps workflows, credentials, and execution history\nacross restarts.",
  "gettingStarted": "1. Open the deployment's URL and sign in to Musher.\n2. Sign in to n8n with your verified email and the **Owner password** from\n   the deployment's Installation tab. There is no setup screen.\n3. Build your first workflow on the canvas. Webhook URLs already use the\n   deployment's own address.\n\nKeep using the generated password. n8n manages the owner from the\ndeployment, so its password can't be changed inside n8n.",
  "iconFileId": "53c06ade-d065-500a-a4e3-575b1e34e94c",
  "icon": {
    "id": "53c06ade-d065-500a-a4e3-575b1e34e94c",
    "url": "https://musher-prod-media.nyc3.cdn.digitaloceanspaces.com/53/files/53c06ade-d065-500a-a4e3-575b1e34e94c/original.webp",
    "thumbnailUrl": "https://musher-prod-media.nyc3.cdn.digitaloceanspaces.com/53/files/53c06ade-d065-500a-a4e3-575b1e34e94c/thumbnail.webp",
    "largeUrl": "https://musher-prod-media.nyc3.cdn.digitaloceanspaces.com/53/files/53c06ade-d065-500a-a4e3-575b1e34e94c/large.webp",
    "width": 460,
    "height": 460
  },
  "screenshots": [],
  "tags": [
    "automation",
    "workflow",
    "integration",
    "low-code"
  ],
  "homepageURL": "https://n8n.io",
  "sourceRepositoryURL": "https://github.com/n8n-io/n8n",
  "supportURL": "https://docs.n8n.io",
  "license": "SUL-1.0 AND LicenseRef-n8n-Enterprise",
  "blueprintId": "a3a7a807-8473-5f6f-80a0-6287e805a8a3",
  "blueprintVersion": 11,
  "componentId": null,
  "componentVersion": null,
  "componentCount": 1,
  "hardwareSummary": {
    "requiresGpu": false,
    "computeTier": "STANDARD",
    "storageKind": "PERSISTENT"
  },
  "requiredParameterCount": 0,
  "effortLevel": "TRIVIAL",
  "isFeatured": false,
  "featuredRank": 0,
  "audit": {
    "status": "PUBLISHED",
    "supersededBy": null,
    "draftedAt": "2026-06-20T13:17:50.976677Z",
    "publishedAt": "2026-09-24T18:59:46.257617Z",
    "deprecatedAt": null,
    "unpublishedAt": null
  },
  "createdAt": "2026-06-20T13:17:50.976677Z",
  "updatedAt": "2026-11-19T22:40:02.155182Z"
}
