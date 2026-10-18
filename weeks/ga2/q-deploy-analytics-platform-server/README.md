# q-deploy-analytics-platform-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Deploy a POST Analytics Endpoint (1.5 marks)**

Deploy stateless `POST /analytics`. Auth header `X-API-Key: <assigned key>` (seeded per email); missing/wrong → 401. Body `{"events": [{"user", "amount", "ts"}, …]}` → `{"email", "total_events", "unique_users", "revenue", "top_user"}`:
total_events = count of events; unique_users = distinct users; revenue = sum of amounts > 0; top_user = user with the highest positive-amount total (no ties). CORS must allow the exam page. Submit the `/analytics` URL.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://<your-project>.vercel.app/analytics
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
