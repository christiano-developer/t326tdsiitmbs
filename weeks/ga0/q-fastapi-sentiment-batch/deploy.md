# Deploy guide — q-fastapi-sentiment-batch

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (FastAPI preset) |
| Public URL    | **https://tds-ga0-sentiment.vercel.app/sentiment** (project `christiano-iitm-bs/tds-ga0-sentiment`) |
| Project root  | `weeks/ga0/q-fastapi-sentiment-batch/src` (`main.py`, `sentiment.py`, `requirements.txt`, `.vercelignore`; no `vercel.json`) |
| Required env  | none |

## 1. Run locally

```bash
cd weeks/ga0/q-fastapi-sentiment-batch
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn      # once
.venv/bin/uvicorn main:app --app-dir src --port 8002
```

## 2. Test locally (grader replay)

```bash
.venv/bin/python src/test_api.py http://127.0.0.1:8002/sentiment 200
```

## 3. Deploy

```bash
cd weeks/ga0/q-fastapi-sentiment-batch/src
npx vercel link --yes --project tds-ga0-sentiment
npx vercel --prod --yes
```

## 4. Test the deployed URL

```bash
python3 weeks/ga0/q-fastapi-sentiment-batch/src/test_api.py https://tds-ga0-sentiment.vercel.app/sentiment 50
curl -s -i -X OPTIONS https://tds-ga0-sentiment.vercel.app/sentiment -H "Origin: https://exam.sanand.workers.dev" -H "Access-Control-Request-Method: POST" | grep -i access-control-allow-origin
```

## 5. Keep alive until graded

Vercel stays up. Submit the production alias with `/sentiment`.

## Teardown (after grading)

```bash
npx vercel remove tds-ga0-sentiment --yes
```
