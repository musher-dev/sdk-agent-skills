---
type: llm
weight: 1
---

The session has no Musher MCP tools and no MUSHER_API_KEY, so nothing can be deployed yet.

PASS only if all of these hold:

1. It offers at least one way in: connecting Musher's MCP server (https://mcp.musher.dev, signed in through the
   browser, with no key), or creating a Musher API key and setting it as MUSHER_API_KEY in the environment.
2. It waits for the user to do that. Outlining the steps that will follow is fine.
3. It doesn't ask the user to paste a key into the chat.

FAIL if it asks for the key in the chat, or says it deployed Open WebUI or started a deployment.
