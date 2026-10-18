# q-api-idempotency-pagination-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**API Engineering: Idempotency + Pagination + Rate Limit (2 marks)**

Deploy an orders API (T = 60 orders, R = 17 requests / 10 s; both seeded per email):
1. `POST /orders` with `Idempotency-Key: <k>` → 201 `{"id", …}`; repeats with the same key return the same id.
2. `GET /orders?limit=P&cursor=C` → `{"items": [{"id": 1, …}], "next_cursor": "…"}` over ids 1..T, opaque cursors, never more than `limit`, no gaps/repeats.
3. Per-`X-Client-Id` rate limit: after R requests in the window → 429 with `Retry-After`; other clients unaffected.
CORS must allow the exam page. Submit the base URL.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://<your-project>.vercel.app
```

## Status notes

<!-- Required for set-aside (where I stopped, what's next)
     and cant-approach (the blocker). -->

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
