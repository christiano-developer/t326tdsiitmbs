# Final — q-deploy-analytics-platform-server

> Goal: the answer can be reproduced from this file alone.
> Repo folder: [weeks/ga2/q-deploy-analytics-platform-server](https://github.com/christiano-developer/t326tdsiitmbs/tree/main/weeks/ga2/q-deploy-analytics-platform-server)

## How to solve (for a teammate)

The assigned values in the code (email, origins, keys, limits, layer values) are **seeded per email** — replace them with yours from the exam page.

**Approach:** Constant-time key compare against an env var, then one pass over events summing positive amounts per user.

1. Make a folder named after the Vercel project you want (e.g. `tds-ga2-analytics`) with this layout:
   ```
   tds-ga2-analytics/
     app.py              # from api.index import app
     api/__init__.py     # empty
     api/index.py        # the app below
     requirements.txt    # fastapi
   ```
2. `app.py` contains exactly: `from api.index import app  # noqa: F401`
3. `api/index.py`:

<details><summary>api/index.py (click to expand)</summary>

```python
"""Stateless POST /analytics endpoint (TDS GA2 q-deploy-analytics-platform-server).

Auth: X-API-Key must equal the API_KEY env var (set in Vercel), else 401.
Body {"events": [{"user", "amount", "ts"}]} ->
  {email, total_events, unique_users, revenue (sum of amount > 0), top_user (max positive total)}
"""
import os
import secrets

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "ROLL_NUMBER@ds.study.iitm.ac.in"

app = FastAPI()
# CORS is outermost, so 401 responses also carry CORS headers and the browser can read the status
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


@app.post("/analytics")
async def analytics(request: Request):
    expected = os.environ.get("API_KEY", "")
    given = request.headers.get("x-api-key", "")
    if not expected or not secrets.compare_digest(given, expected):
        return JSONResponse({"error": "invalid or missing X-API-Key"}, status_code=401)
    try:
        body = await request.json()
        events = body.get("events", []) if isinstance(body, dict) else []
    except Exception:
        return JSONResponse({"error": "body must be JSON {events: [...]}"}, status_code=400)
    if not isinstance(events, list):
        events = []
    events = [e for e in events if isinstance(e, dict)]
    per_user = {}
    revenue = 0.0
    for e in events:
        amt = num(e.get("amount"))
        if amt > 0:
            revenue += amt
            per_user[e.get("user")] = per_user.get(e.get("user"), 0.0) + amt
    top_user = max(per_user, key=per_user.get) if per_user else None
    tidy = lambda v: int(v) if float(v).is_integer() else round(v, 6)  # noqa: E731
    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len({e.get("user") for e in events}),
        "revenue": tidy(revenue),
        "top_user": top_user,
    }


@app.get("/")
def root():
    return {"ok": True, "endpoint": "POST /analytics (X-API-Key)"}
```

</details>

4. Deploy from inside the folder: `vercel deploy --prod --yes -e API_KEY=<your assigned key>`. **No `vercel.json`** (rewrites make every route 404).
5. Submit the **Aliased** URL from the output (`https://<project>.vercel.app/analytics`), press Check, then Save.

Gotchas: CORSMiddleware is outermost so 401s carry CORS headers; otherwise the browser sees a network error, not 401. Exclude ≤ 0 from revenue and from top_user totals. Kept out of code: read from the `API_KEY` env var (repo root `.env` → `vercel -e`).

## Final prompt

```text
Deploy a POST Analytics Endpoint (1.5 marks)
<paste the full question text with your assigned values>
Write a FastAPI app for Vercel zero-config deployment (app.py re-exporting `app` from api/index.py,
requirements.txt, no vercel.json). Return JSON errors (never a bare 500). Constant-time key compare against an env var, then one pass over events summing positive amounts per user.
Also give a pytest/TestClient script that replays exactly what the grader checks.
```

- **Tool / model used:** Claude (Opus 5.5).

## Reproduction steps (needs a clone of this repo)

```bash
cd ~/developer/t326tdsiitmbs && set -a && source .env && set +a
cd weeks/ga2/q-deploy-analytics-platform-server/src/tds-ga2-analytics
vercel deploy --prod --yes -e API_KEY="$GA2_ANALYTICS_API_KEY"
```

Source: [https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-deploy-analytics-platform-server/src/tds-ga2-analytics/api/index.py](https://github.com/christiano-developer/t326tdsiitmbs/blob/main/weeks/ga2/q-deploy-analytics-platform-server/src/tds-ga2-analytics/api/index.py)

## Expected output

Exam **Check** shows the question as correct.

## Answer submitted

```
https://<your-project>.vercel.app/analytics
```
