# Deploy guide — q-ledger-agent-server

> `LEDGER_URL` (contains your quizSign) and `AIPIPE_TOKEN` are secrets: Vercel env vars only, never in the repo.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (FastAPI preset, Python serverless) |
| Public URL    | `https://<project>.vercel.app/` (this repo: `<your-project>.vercel.app`) |
| Repo / branch | `weeks/ga1/q-ledger-agent-server/src` on `ga1` (deployed from the CLI) |
| Runtime       | Python 3.12, `fastapi` (stdlib `urllib` for HTTP) |
| Required env  | `LEDGER_URL`, `AIPIPE_TOKEN`; optional `LLM_MODEL` (default `gpt-4.1-mini`) |

## 1. Run locally

```bash
cd src
LEDGER_URL='<questionData URL for this question>' AIPIPE_TOKEN='<token>' \
  uv run --with fastapi --with uvicorn uvicorn app:app --port 8000
uv run --with fastapi python test_executor.py      # offline logic test, no secrets needed
```

## 2. Test locally

```bash
curl -s localhost:8000/ -H 'Content-Type: application/json' -H 'X-Debug: 1' \
  -d '{"question":"What was the total revenue in USD from the North region in March 2026?"}' | jq
```

`X-Debug: 1` also returns the parsed spec.

## 3. Deploy

```bash
cd src && pwd
vercel link --yes --project <project-name>
vercel env add LEDGER_URL production      # the API link from the question (ending path=/ is fine)
vercel env add AIPIPE_TOKEN production
vercel deploy --prod
```

## 4. Test deployed URL

Compare a few answers with your own calculation from `/export` (dedup by latest `updated_at`, IST dates,
`paid` only, USD via `/rates`). Re-test after **every** redeploy.

## 5. Keep alive / teardown

Nothing runs locally. Keep the project and env vars until the GA deadline.
