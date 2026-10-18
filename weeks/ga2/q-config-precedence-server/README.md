# q-config-precedence-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga2 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

**Resolve 12-Factor Config Precedence (1 mark)**

Deploy `GET /effective-config?set=key=value&set=…` merging (low → high): defaults (`port 8000, workers 1, debug false, log_level info, api_key default-secret-000`) → `config.development.yaml` (`port 8385, debug false, log_level debug`) → `.env` (`APP_PORT=8051, APP_DEBUG=true`) → OS env (`APP_WORKERS=11, APP_API_KEY=…`) → `?set=` overrides. Layer values are seeded per email.

Coerce `port`/`workers` → int, `debug` → bool (true/1/yes/on), others → string. `NUM_WORKERS` in `.env` aliases `workers`. `api_key` always `"****"`. CORS must allow the exam page. Submit the `/effective-config` URL.

## Inputs / given data

Assigned values are seeded per email (`ROLL_NUMBER@ds.study.iitm.ac.in`) and shown on the exam page.

## Final answer

```
https://<your-project>.vercel.app/effective-config
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
