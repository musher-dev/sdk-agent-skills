---
type: llm
weight: 1
---

PASS if the reply says the figure comes from Musher's live cost estimate (the cost-estimate endpoint, the
`get_catalog_listing_cost_estimate` MCP tool, or the Console) rather than stating a price from memory, and notes that
storage is billed separately from compute. Any of those routes counts. FAIL if it states a specific price as fact
without saying it must be looked up live.
