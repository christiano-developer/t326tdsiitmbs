# q-observability-metrics-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1.5 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Production Observability: Metrics, Health & Structured Logs (1.5 marks)**

Deploy a FastAPI service with:
- `GET /work?n=K` → `{"email", "done": K}`; increments the request counter.
- `GET /metrics` → Prometheus text with a counter `http_requests_total` that increases on every request.
- `GET /healthz` → `{"status": "ok", "uptime_s": <non-negative float>}`.
- `GET /logs/tail?limit=N` → JSON array of the last N log entries, each with at least `level`, `ts`, `path`, `request_id`.

Grader: reads the counter, makes 3–6 `/work` calls, reads again (must rise by ≥ calls); checks healthz; checks logs have the four fields and an entry with path containing `/work`. Submit the base URL.

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
