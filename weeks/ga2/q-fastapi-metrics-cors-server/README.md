# q-fastapi-metrics-cors-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Deploy a CORS-Aware Metrics API (1.5 marks)**

Build and deploy a FastAPI service with `GET /stats?values=1,2,3,…` returning `{"email", "count", "sum", "min", "max", "mean"}` (mean ±0.01) for a fresh random batch each check.

CORS: only the assigned origin (`https://dash-ufy2p7.example.com`, seeded per email) gets `Access-Control-Allow-Origin` — no `*`. Preflight `OPTIONS /stats` from it must succeed; preflights from any other origin must get no ACAO header.

Every response carries `X-Request-ID` (unique, e.g. UUID) and `X-Process-Time` (non-negative seconds).

Grader: preflight from allowed origin (expects ACAO), preflight from a random evil origin (no ACAO), GET /stats with a random batch (all fields + email + both headers). Submit the base URL.

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
