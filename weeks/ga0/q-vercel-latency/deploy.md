# Deploy guide — q-vercel-latency

## Target

| Field         | Value |
|---------------|-------|
| Platform      | Vercel (FastAPI preset) |
| Public URL    | **https://tds-ga0-latency.vercel.app/** (also `/api/latency`; project `christiano-iitm-bs/tds-ga0-latency`) |
| Project root  | `weeks/ga0/q-vercel-latency/src` (`main.py`, `telemetry.json`, `requirements.txt`, `.vercelignore`; no `vercel.json`) |
| Required env  | none |

## 1. Run locally

```bash
cd weeks/ga0/q-vercel-latency
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn      # once
.venv/bin/uvicorn main:app --app-dir src --port 8003
```

## 2. Test locally (vs the grader's JS formulas; needs node)

```bash
.venv/bin/python src/test_api.py http://127.0.0.1:8003/
```

## 3. Deploy

```bash
cd weeks/ga0/q-vercel-latency/src
npx vercel link --yes --project tds-ga0-latency
npx vercel --prod --yes
```

## 4. Test the deployed URL

```bash
python3 weeks/ga0/q-vercel-latency/src/test_api.py https://tds-ga0-latency.vercel.app/
```

Real-browser check (the grader reads the ACAO header from JS):

```bash
cd weeks/ga0/q-vercel-latency/src && python3 -m http.server 8790 --bind 127.0.0.1 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --virtual-time-budget=15000 \
  --dump-dom "http://127.0.0.1:8790/browser_check.html?url=https://tds-ga0-latency.vercel.app/" | grep -o 'RESULT ok=[^<]*'
# expect: RESULT ok=true acao="*" …
```

## 5. Keep alive until graded

Vercel stays up. Submit the production alias.

## Teardown (after grading)

```bash
npx vercel remove tds-ga0-latency --yes
```

## Troubleshooting log

| Symptom | Cause | Fix |
|---------|-------|-----|
| Exam: "Enable CORS with Access-Control-Allow-Origin: *" although curl shows the header | ACAO isn't readable by cross-origin JS unless exposed | `expose_headers=["Access-Control-Allow-Origin"]` in CORSMiddleware; verify with browser_check.html |
