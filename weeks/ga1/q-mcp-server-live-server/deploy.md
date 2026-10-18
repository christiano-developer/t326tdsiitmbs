# Deploy guide — q-mcp-server-live-server

> The exam email is the code default; `EXAM_EMAIL` overrides it (e.g. for a teammate).

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (FastAPI preset, Python serverless) |
| Public URL    | `https://<project>.vercel.app/mcp` (this repo: `<your-project>.vercel.app/mcp`) |
| Repo / branch | `weeks/ga1/q-mcp-server-live-server/src` on `ga1` (deployed from the CLI) |
| Runtime       | Python 3.12, `fastapi` |
| Optional env  | `EXAM_EMAIL` (overrides the default email in code) |

## Prerequisites

- [ ] Vercel CLI installed and logged in (`vercel whoami`)
- [ ] `uv` for local runs and the test client

## 1. Run locally

```bash
cd src
EXAM_EMAIL=<your exam email> uv run --with fastapi --with uvicorn uvicorn app:app --port 8000
```

## 2. Test locally

```bash
curl -s -H 'Content-Type: application/json' localhost:8000/mcp \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq
EXAM_EMAIL=<your exam email> uv run --with mcp python test_client.py http://localhost:8000/mcp
```

Expected: `solve_challenge` listed; `correct: 5 / 5`.

## 3. Deploy

```bash
cd src
vercel link --yes --project <project-name>            # once
vercel deploy --prod
```

Submit the **Aliased** URL + `/mcp`. Dashboard equivalent of the env step: Project → Settings → Environment
Variables → `EXAM_EMAIL` (Production).

## 4. Test deployed URL

```bash
EXAM_EMAIL=<your exam email> uv run --with mcp python test_client.py https://<project>.vercel.app/mcp
```

- [x] 5 / 5 correct
- [x] Reachable without Vercel login (alias, not the one-off deployment URL)

## 5. Keep alive / teardown

Nothing to keep running locally. Don't delete the project before the deadline (live grading).
