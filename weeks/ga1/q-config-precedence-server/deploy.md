# Deploy guide — q-config-precedence-server

> Secrets / per-student values never go in the repo: layer-4 values are passed at deploy time.

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (FastAPI preset, Python serverless) |
| Public URL    | `https://<project>.vercel.app/effective-config` (this repo: `<your-project>.vercel.app`) |
| Repo / branch | `weeks/ga1/q-config-precedence-server/src` on `ga1` (deployed from the CLI, not Git) |
| Runtime       | Python 3.12 (Vercel default), `fastapi`, `pyyaml` |
| Required env  | `APP_WORKERS`, `APP_API_KEY` (from your question's OS-env box) |

## Prerequisites

- [ ] Vercel account; CLI installed (`vercel --version`) and logged in (`vercel whoami`)
- [ ] `uv` for local runs
- [ ] `src/config.development.yaml` and `src/app.env` filled with **your** question's layer 2 and layer 3 values

## 1. Run locally

```bash
cd src
APP_WORKERS=<n> APP_API_KEY=<key> uv run --with fastapi --with pyyaml --with uvicorn uvicorn app:app --port 8000
```

## 2. Test locally

```bash
curl -s "http://localhost:8000/effective-config" | jq
curl -s "http://localhost:8000/effective-config?set=port=9000&set=debug=false" | jq
curl -sI -H "Origin: https://exam.sanand.workers.dev" "http://localhost:8000/effective-config" | grep -i access-control
```

Expected: base = all four layers merged, overrides win, `api_key` is `"****"`, `access-control-allow-origin: *`.

## 3. Deploy

```bash
cd src
vercel link --yes --project <project-name>          # once; ignore a "Connecting GitHub repository" error
vercel deploy --prod -e APP_WORKERS=<n> -e APP_API_KEY=<key>
```

Use the **Aliased** URL it prints (`https://<project>.vercel.app`). The one-off deployment URL is behind Vercel
Authentication; the alias is public.

Dashboard-only config: none.

## 4. Test deployed URL

```bash
curl -s "https://<project>.vercel.app/effective-config?set=workers=4" | jq
```

- [x] Returns expected output
- [x] CORS allows `*`
- [x] Works from a fresh browser tab (checked from the exam page)

## 5. Keep alive / teardown

Vercel serverless needs nothing running locally. After the GA deadline: `vercel project rm <project-name>` (optional).
