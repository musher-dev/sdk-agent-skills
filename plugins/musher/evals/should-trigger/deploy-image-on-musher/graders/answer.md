---
type: llm
weight: 1
---

PASS if the reply uses `musher deploy` with `--image ghcr.io/acme/api:v1.4.2` and `--port 8080` (or
the Musher API with an equivalent blueprint), runs non-interactively (mentions --json or --no-
input), and says it will report success only once the deployment is ACTIVE or healthy with a URL.
FAIL if it invents flags or claims success without checking status.
