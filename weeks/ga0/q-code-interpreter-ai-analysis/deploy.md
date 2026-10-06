# Deploy guide — q-code-interpreter-ai-analysis

> Secrets go in `.env` / Vercel env vars, never in git. `.env.example` lists names only.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (Python serverless function, FastAPI) |
| Public URL    | **https://tds-ga0-code-interpreter.vercel.app** (project `christiano-iitm-bs/tds-ga0-code-interpreter`); submit this, the grader appends `/code-interpreter` |
| Project root  | `weeks/ga0/q-code-interpreter-ai-analysis/src` (`main.py` entrypoint → `api/index.py`, `requirements.txt`, `.vercelignore`; **no `vercel.json`**) |
| Runtime       | Vercel's default Python (3.12) |
| Required env  | `AIPIPE_TOKEN`: **optional**, only for the AI fallback (never hit by the 60 grader tests) |

## Prerequisites

- [ ] Node / npx available (`npx --version`)
- [ ] Vercel account + CLI login: `npx vercel login` (interactive, so run it yourself as `! npx vercel login`)

## 1. Run locally

```bash
cd weeks/ga0/q-code-interpreter-ai-analysis
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn      # once
.venv/bin/uvicorn api.index:app --app-dir src --port 8000
```

## 2. Test locally (all 60 grader cases, grader's exact checks)

```bash
.venv/bin/python src/test_all.py http://127.0.0.1:8000
```

Expected: `60/60 passed` (including this student's 3: #10, #36, #43).

## 3. Deploy

```bash
cd weeks/ga0/q-code-interpreter-ai-analysis/src
npx vercel link --yes --project tds-ga0-code-interpreter   # once: name the project (else it's called "src")
npx vercel --prod --yes                                     # deploy; prints Production + Aliased URLs
```

Optional AI fallback token (dashboard alternative: Project → Settings → Environment Variables):

```bash
npx vercel env add AIPIPE_TOKEN production    # paste the token when prompted
npx vercel --prod --yes                       # redeploy so the function sees it
```

## 4. Test the deployed URL

```bash
python3 weeks/ga0/q-code-interpreter-ai-analysis/src/test_all.py https://tds-ga0-code-interpreter.vercel.app
curl -s -i -X OPTIONS https://tds-ga0-code-interpreter.vercel.app/code-interpreter \
  -H "Origin: https://exam.sanand.workers.dev" -H "Access-Control-Request-Method: POST" | grep -i access-control-allow-origin
```

- [ ] `60/60 passed`
- [ ] `access-control-allow-origin: *`
- [ ] Submit `https://tds-ga0-code-interpreter.vercel.app` in the exam and press Check

## 5. Keep alive until graded

- Vercel free tier stays up; nothing to keep running locally. Don't redeploy broken code before grading closes.

## Teardown (after grading)

```bash
npx vercel remove <project> --yes
npx vercel env rm AIPIPE_TOKEN production   # if it was set
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
| Local server kept answering after `pkill` | shutdown race | check with `lsof -ti tcp:8000`, then re-check |
| Live URL returned **404** on every path | Vercel's FastAPI preset: a `vercel.json` rewrite to `/api/index` makes FastAPI see path `/api/index` ("internal rewrites in backend framework projects route using the rewritten destination path") | delete `vercel.json`; add root `main.py` with `from api.index import app` |
| Unique deployment URL (`…-4vmvki3um-….vercel.app`) → 302/401 | Deployment Protection (Vercel Authentication) covers generated URLs | submit the **production alias** `tds-ga0-code-interpreter.vercel.app` (not protected) |
| `vercel link` → "Failed to link GitHub repository" | no GitHub login connection on Vercel | harmless; CLI deploys only (avoids redeploys on every push) |
| AIPipe 403 from Python | AIPipe blocks Python's default User-Agent | custom `User-Agent` header (already in `analyze_error_with_ai`) |
