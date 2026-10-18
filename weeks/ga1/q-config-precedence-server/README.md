# q-config-precedence-server

| Field     | Value |
|-----------|-------|
| Section   | weeks/ga1 |
| Marks     | 1 |
| Status    | solved <!-- todo | in-progress | solved | set-aside | cant-approach --> |
| Deploy?   | yes |
| Started   | 2026-10-18 |
| Closed    | 2026-10-18 |

## Question

Deploy a **FastAPI** service that merges four config layers — defaults, `config.development.yaml`,
`.env`, OS env (`APP_*`) — then applies CLI overrides passed as query params.

`GET /effective-config?set=key=value&set=…` → `{"port": int, "workers": int, "debug": bool, "log_level": str, "api_key": "****"}`

- Precedence (low → high): defaults → yaml → .env → OS env → `?set=` overrides.
- Coercion: port/workers int; debug bool (`true/1/yes/on`, case-insensitive); rest string.
- Alias: `NUM_WORKERS` in `.env` → `workers`. Mask `api_key` as `"****"`. CORS must allow the exam page.

Paste the deployed `/effective-config` URL.

Source: quiz JS (`exam-tds-2026-09-ga1.js`), 2026-10-08.

## Inputs / given data

The four layers are seeded from `q-config-precedence-server#<email lower>#<version>` and shown on the page. Copy them from there.

## Final answer

```
https://<your-project>.vercel.app/effective-config
```

## Status notes

Checked ✅ on 2026-10-18. Live service: keep the Vercel project `tds-ga1-config` up until the GA1 deadline.

## Files

- [prompts.md](prompts.md) — every prompt tried, in order
- [approaches.md](approaches.md) — approaches considered, chosen one and why
- [final.md](final.md) — single prompt + steps that reproduce the answer
- [deploy.md](deploy.md) — commands + guide to deploy / boot / configure
- `src/` — code · `data/` — inputs/outputs
