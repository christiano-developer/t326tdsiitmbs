# Deploy — q-rag-colosseum-server

| Item | Value |
|------|-------|
| Platform | Vercel (Python runtime, FastAPI; `app.py` re-exports `app` from `api/index.py`; no `vercel.json`) |
| Project folder | `src/tds-ga5-rag` (folder name = project name) |
| Public URL | `https://<your-project>.vercel.app` (submit the base URL, no `/query`) |
| Storage | Upstash Redis via Vercel Storage → `KV_REST_API_URL` / `KV_REST_API_TOKEN` (query log only, optional) |

## Environment (names only — values live in the git-ignored `.env`)

| Var | Purpose |
|-----|---------|
| `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` | provider 1 (AI Pipe `https://aipipe.org/openai/v1`, `gpt-4.1-mini`) |
| `LLM2_*` | provider 2 (Gemini OpenAI-compatible endpoint, `gemini-3.1-flash-lite`) |
| `LLM3_*` | provider 3 (OpenAI direct) |
| `LLM_TIMEOUT` | total LLM budget, default 6.5 s |

Set them with [../set-q1-env.sh](../set-q1-env.sh) (reads `.env`, never prints values) which also redeploys.

## Steps

```bash
cd weeks/ga5/q-rag-colosseum-server/src/tds-ga5-rag
vercel deploy --prod --yes          # first deploy creates the project
bash ../../../set-q1-env.sh         # providers + redeploy
# Vercel dashboard → Storage → connect the Upstash DB to the project (optional, for /_recent) → redeploy
```

## Checks

- `GET /` → `{"ok": true, "passages": 50, "llm": true}`
- `GET /_selftest` → status 200 per provider (shows 429/expired keys per provider)
- `GET /_recent?n=20` → last 20 probes with answers (debugging the gauntlet)
- Exam: **Run 20-Probe Gauntlet** (free preview) → **Check** → **Save**.

## Failures seen

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/_selftest` 429 | OpenAI prepaid credit expired (balance $0) | AI Pipe first, Gemini second |
| Gauntlet 0/2, `Failed to fetch` | broken file uploaded (syntax error) → function crashed, no CORS headers | re-upload with unique name, verify md5 + `ast.parse` before deploy |
| `/_recent` shows 2 of 20 | serverless instances don't share memory | log to Upstash list `rag:log` |
