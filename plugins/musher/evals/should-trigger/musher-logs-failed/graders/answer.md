---
type: llm
weight: 1
---

PASS if the reply plans to read the deployment's logs (including the SYSTEM or BUILD stream, or
musher logs) and its status/error, rather than redeploying blindly. FAIL if it only suggests
redeploying.
