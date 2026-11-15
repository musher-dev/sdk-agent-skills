---
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
tags: [near-miss]
---

This Postgres query is slow: SELECT * FROM orders WHERE customer_id = 42 ORDER BY created_at. How do I speed it up?
