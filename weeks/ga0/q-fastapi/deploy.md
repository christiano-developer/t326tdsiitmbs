# Deploy guide — q-fastapi

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (FastAPI preset) |
| Public URL    | **https://tds-ga0-fastapi.vercel.app/api** (project `christiano-iitm-bs/tds-ga0-fastapi`) |
| Project root  | `weeks/ga0/q-fastapi/src` (`main.py`, `students.csv`, `requirements.txt`, `.vercelignore`; no `vercel.json`) |
| Required env  | none |

## 1. Run locally

```bash
cd weeks/ga0/q-fastapi
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn      # once
.venv/bin/uvicorn main:app --app-dir src --port 8001
```

## 2. Test locally (grader replay)

```bash
.venv/bin/python src/test_api.py http://127.0.0.1:8001/api 200
```

## 3. Deploy

```bash
cd weeks/ga0/q-fastapi/src
npx vercel link --yes --project tds-ga0-fastapi      # once ("Failed to link GitHub" is harmless)
npx vercel --prod --yes
```

## 4. Test the deployed URL

```bash
python3 weeks/ga0/q-fastapi/src/test_api.py https://tds-ga0-fastapi.vercel.app/api 100
curl -s -i "https://tds-ga0-fastapi.vercel.app/api?class=8I" -H "Origin: https://exam.sanand.workers.dev" | grep -i access-control-allow-origin
```

## 5. Keep alive until graded

Vercel stays up. Submit the **production alias** (the unique `…-a5ix3o8o2-….vercel.app` URL is behind Vercel Authentication).

## Teardown (after grading)

```bash
npx vercel remove tds-ga0-fastapi --yes
```
