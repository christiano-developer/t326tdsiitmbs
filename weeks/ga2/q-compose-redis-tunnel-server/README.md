# q-compose-redis-tunnel-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 2 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Multi-Container App via Compose, Exposed by Tunnel (2 marks)**

Run a `docker compose` stack: `api` (FastAPI talking to redis over the compose network) + `redis` (standard image, no external port). Endpoints: `POST /hit/{key}` → atomic INCR → `{"key","count"}`; `GET /count/{key}` → current count (0 if unseen); `GET /healthz` → `{"status":"ok","redis":"up"}` after a real PING. Use Redis INCR, independent per-key counters. Expose `api` via a tunnel (`cloudflared tunnel --url http://localhost:8000` or `lt --port 8000`) and submit the tunnel base URL. Grader: healthz, a random hit sequence across two keys, counts must match exactly.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://<random-words>.trycloudflare.com (cloudflared quick tunnel; changes every run)
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
