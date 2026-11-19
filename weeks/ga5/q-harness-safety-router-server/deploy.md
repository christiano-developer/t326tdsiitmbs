# Deploy — q-harness-safety-router-server

| Item | Value |
|------|-------|
| Platform | Vercel (FastAPI; `app.py` re-exports `api/index.py`; no `vercel.json`) |
| Project folder | `src/tds-ga5-safety` |
| Endpoint | `https://<your-project>.vercel.app/classify` (exact POST route; JSON response, no redirects) |
| Storage | Upstash Redis (Vercel Storage → connect project) for batch capture |

## Environment (names only)

| Var | Purpose |
|-----|---------|
| `CAPTURE_TOKEN` | header `x-capture-token` for `GET /_capture`, `GET /_capture/{id}` |
| `KV_REST_API_URL`, `KV_REST_API_TOKEN` | injected by the Upstash integration |

## Steps

```bash
cd weeks/ga5/q-harness-safety-router-server/src/tds-ga5-safety
set -a; source ../../../../../.env; set +a
vercel deploy --prod --yes -e CAPTURE_TOKEN="$CAPTURE_TOKEN"
# Vercel dashboard → Storage → connect the Upstash DB → redeploy; GET / must show "capture": true
```

## Failures seen

| Symptom | Cause | Fix |
|---------|-------|-----|
| Capture endpoints unreachable from the chat sandbox / device VM | `vercel.app` not on their network allowlist | pull batches from the Mac terminal with `pull-q4-cases.sh` |
| 34/96 on the first Check | rules written before seeing any case | capture first, tune offline |
