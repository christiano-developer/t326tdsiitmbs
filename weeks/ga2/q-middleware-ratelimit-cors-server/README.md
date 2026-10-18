# q-middleware-ratelimit-cors-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Middleware Stack: Rate-Limit + CORS + Request Context (1.5 marks)**

Deploy `GET /ping` → `{"email", "request_id"}` with three middleware layers:
1. Request context: reuse inbound `X-Request-ID` or generate a UUID4; return it in the body and the `X-Request-ID` header.
2. CORS: only the assigned origin (`https://app-nbggbq.example.com`, seeded) gets ACAO, no `*`; also allow the exam page origin for verification.
3. Per-`X-Client-Id` rate limit with bucket B = 11 / 10 s (seeded) → 429; a fresh client still succeeds.
Grader: request with a supplied X-Request-ID (echoed in body + header), one without (fresh id in both), 16 requests from one client (must 429), then a different client. Submit the base URL.

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
