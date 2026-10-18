# Deploy guide — q-api-idempotency-pagination-server

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (team `<your-team>`), Python FastAPI zero-config |
| Vercel project| `tds-ga2-orders` (named after the folder) |
| Public URL    | https://<your-project>.vercel.app |
| Runtime       | Python 3.12, `requirements.txt` |
| Required env  | none |

## 1. Run locally

```bash
cd weeks/ga2/q-api-idempotency-pagination-server/src/tds-ga2-orders
uv run --with fastapi --with uvicorn uvicorn app:app --port 8000
```

## 2. Deploy

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a   # loads assigned values, never committed
cd weeks/ga2/q-api-idempotency-pagination-server/src/tds-ga2-orders && pwd
vercel deploy --prod --yes
```

Use the **Aliased** URL (deployment URLs sit behind Vercel auth). Revert any `.vercel`/`.env*` lines `vercel` adds to the repo-root `.gitignore`.
List live aliases: `vercel alias ls | grep tds-ga2`.

## 3. Test deployed URL

Press **Check** on the exam page (the grader is the real test).

## 4. Keep alive until graded

Leave the project up until the GA2 deadline (and through Save).

## Teardown (after grading)

```bash
vercel project rm tds-ga2-orders
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
